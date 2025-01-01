import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType
from pyspark.ml.feature import Imputer
from pyspark.sql.functions import unix_timestamp
from pyspark.sql.functions import year, month, date_format, to_timestamp, dayofweek, hour
import pyspark.sql.functions as F
from pyspark.sql.functions import col, sum, desc, mean, stddev, min, max, avg, when, count
from pyspark.sql.functions import radians, sin, cos, atan2, sqrt


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
    .parquet("pyscript_clean.parquet", mode="overwrite")



