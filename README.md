This project involves processing and analyzing Divvy bike-sharing Chicago data.
It uses a combination of tools like DBT, Airflow, Spark, Docker, and Terraform to handle data transformation, scheduling, and infrastructure management.

workflow: 

Project Structure: 
  analyses: Contains DBT analysis scripts.
  dags: Airflow DAGs for scheduling jobs.
  macros: Custom DBT macros.
  models: DBT models for data transformations.
  scripts: Contains project setup scripts.
  seeds: Raw data files for seeding DBT models.
  snapshots: DBT snapshots for versioning tables.
  spark_notebooks: Jupyter Notebooks for Spark-based analysis.
  terraf: Terraform configuration files for infrastructure.
  tests: DBT tests for data quality.
  .gitignore: Specifies files to ignore in Git.
  Dockerfile: Docker configuration for the project.
  docker-compose.yaml: Docker Compose file for container orchestration.
  requirements.txt: Python dependencies for the project.

Data : divvy chicago bike data(2020-2024)
Columns:
  ride_id - Unique ID Assigned to Each Divvy Trip
  rideable_type - Type of Vehicle Used
  started_at - Start of Trip Date and Time
  ended_at - End of Trip Date and Time
  start_station_name - Name Assigned to Station the Trip Started at
  start_station_id - Unique Identification Number of Station the Trip Started at
  end_station_name - Name Assigned to Station the Trip Ended at
  end_station_id - Unique Identification Number of Station the Trip Ended at
  start_lat - Latitude of the Start Station
  start_lng - Longitude of the Start Station
  end_lat - Latitude of the End Station
  end_lng - Longitude of the End Station
  member_casual - Field with Two Values Indicating Whether the Rider has a Divvy Membership or Paid with Credit Card


Data Visualizations for this project can be found here

  
