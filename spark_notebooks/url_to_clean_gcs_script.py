import pyspark 
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType
from pyspark.ml.feature import Imputer
from pyspark.sql.functions import unix_timestamp
from pyspark.sql.functions import year, month, date_format, to_timestamp, dayofweek, hour
import pyspark.sql.functions as F
from pyspark.sql.functions import col, sum, desc, mean, stddev, min, max, avg, when, count
from pyspark.sql.functions import radians, sin, cos, atan2, sqrt
import os
import subprocess
import argparse
import requests  # Import requests to check URL availability

# Function to check if a URL exists (returns True if it exists, False if it doesn't)
def check_url_exists(url):
    response = requests.head(url)
    return response.status_code == 200

# Download and extract data from URL
def download_and_extract_data(start_year, end_year):
    URL_PREFIX = "https://divvy-tripdata.s3.amazonaws.com"

    for year in range(start_year, end_year + 1):
        LOCAL_PREFIX = f"data/raw/divvy/{year}"
        for month in range(1, 13):
            fmonth = f"{month:02d}"  # Format month as two digits (01, 02, ..., 12)
            url = f"{URL_PREFIX}/{year}{fmonth}-divvy-tripdata.zip"
            local_file = f"{year}{fmonth}-divvy-tripdata.zip"
            local_path = os.path.join(LOCAL_PREFIX, local_file)

            print(f"Checking if {url} exists")
            
            # Check if the URL exists before downloading
            if check_url_exists(url):
                print(f"Downloading {url} to {local_path}")
                os.makedirs(LOCAL_PREFIX, exist_ok=True)
                subprocess.run(["wget", url, "-O", local_path], check=True)

                # Extract the ZIP file
                print(f"Extracting {local_path}")
                subprocess.run(["unzip", "-o", local_path, "-d", LOCAL_PREFIX], check=True)
            else:
                print(f"URL not found: {url}, skipping...")

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Download and process Divvy trip data.")
parser.add_argument("--start_year", type=int, required=True, help="Start year for the data download (e.g., 2021)")
parser.add_argument("--end_year", type=int, required=True, help="End year for the data download (e.g., 2024)")
args = parser.parse_args()

# Call the function to download and extract data
download_and_extract_data(args.start_year, args.end_year)

spark = SparkSession.builder \
    .master("spark://project-001.europe-west10-b.c.project-001-445912.internal:7077") \
    .appName('test') \
    .getOrCreate()

df = spark.read.csv('data/raw/divvy/*', header=True, inferSchema=True)

# Define the new schema
new_schema = StructType([ 
    StructField("ride_id", StringType(), True),
    StructField("rideable_type", StringType(), True),
    StructField("started_at", TimestampType(), True),
    StructField("ended_at", TimestampType(), True),
    StructField("start_station_name", StringType(), True),
    StructField("start_station_id", StringType(), True),
    StructField("end_station_name", StringType(), True),
    StructField("end_station_id", StringType(), True),
    StructField("start_lat", FloatType(), True),
    StructField("start_lng", FloatType(), True),
    StructField("end_lat", FloatType(), True),
    StructField("end_lng", FloatType(), True),
    StructField("member_casual", StringType(), True)
])

# Read the CSV file with the defined schema
df = spark.read.schema(new_schema).csv('data/raw/divvy/*', header=True)

# Define the Imputer
imputer = Imputer(inputCols=['end_lat', 'end_lng'], outputCols=['end_lat_imputed', 'end_lng_imputed'])
# Fit the Imputer model
imputer_model = imputer.fit(df)
# Transform the data
df = imputer_model.transform(df)
df = df.drop('end_lat', 'end_lng')

df = df.filter(
    (col("start_lat") != 0) & (col("start_lng") != 0) & (col("end_lat") != 0) & (col("end_lng") != 0)
)

df = df.withColumn(
    "ride_duration",
    (unix_timestamp("ended_at") - unix_timestamp("started_at")) / 60  # Duration in minutes
)

df = df.withColumn(
    "time_of_day",
    hour(col("started_at")).alias("hour")
)

# Convert 'started_at' to timestamp if not already
df = df.withColumn("started_at", col("started_at").cast("timestamp"))

# Create the 'day_of_week' column (1 = Sunday, 7 = Saturday in Spark)
df = df.withColumn("day_of_week", dayofweek(col("started_at")))

df = df.withColumn("day_of_week",
                                       when(col("day_of_week") == 1, "Sunday")
                                       .when(col("day_of_week") == 2, "Monday")
                                       .when(col("day_of_week") == 3, "Tuesday")
                                       .when(col("day_of_week") == 4, "Wednesday")
                                       .when(col("day_of_week") == 5, "Thursday")
                                       .when(col("day_of_week") == 6, "Friday")
                                       .when(col("day_of_week") == 7, "Saturday"))

# Drop rows where 'start_station_name' or 'end_station_id' have null values
df = df.dropna(subset=["start_station_name", "end_station_id" , "start_station_id"])

# Add partition columns (adjust the column name as needed)
df = df.withColumn('year', year('started_at'))  # Use 'started_at' as the timestamp column
df = df.withColumn('month', month('started_at'))  

data_repartitioned = df.repartition("year", "month")

# Save as Parquet with compression (Snappy) and partition by 'year' and 'month'
data_repartitioned.write.option("compression", "snappy") \
    .partitionBy("year", "month") \
    .parquet("local_to_gcs_script.parquet", mode="overwrite")
