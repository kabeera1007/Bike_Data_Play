Bike Data Play: Divvy Bike-Sharing Analysis
This project involves processing and analyzing Divvy bike-sharing data from Chicago (2020–2024). It uses a combination of tools like DBT, Airflow, Spark, Docker, and Terraform to handle data transformation, scheduling, and infrastructure management.


Workflow
This project uses the following tools and processes:

DBT: For data transformation and analysis.
Airflow: For scheduling and orchestrating tasks.
Spark: For processing large datasets.
Docker: For containerization of the project.
Terraform: For infrastructure management.
Project Structure
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
Data
This dataset contains Divvy bike-sharing trip data from 2020 to 2024. The columns are:

ride_id: Unique ID assigned to each Divvy trip.
rideable_type: Type of vehicle used.
started_at: Start date and time of the trip.
ended_at: End date and time of the trip.
start_station_name: Name of the start station.
start_station_id: Unique ID for the start station.
end_station_name: Name of the end station.
end_station_id: Unique ID for the end station.
start_lat: Latitude of the start station.
start_lng: Longitude of the start station.
end_lat: Latitude of the end station.
end_lng: Longitude of the end station.
member_casual: Whether the rider is a member or a casual user.
Link to Dataset

Data Visualizations
The visualizations for this project can be found here.


  
