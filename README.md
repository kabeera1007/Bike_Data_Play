# Project Name: Bike Data Play - Divvy Bike-Sharing Analysis

## Description

This project involves processing and analyzing Divvy bike-sharing data from Chicago (2020–2024). It uses a combination of tools like DBT, Airflow, Spark, Docker, and Terraform to handle data transformation, scheduling, and infrastructure management.

![Workflow](URL-to-workflow-image)

## Workflow

This project integrates several tools and processes to manage the workflow:

- **DBT**: Data transformation and analysis.
- **Airflow**: Task scheduling and orchestration.
- **Spark**: Data processing.
- **Docker**: Containerization.
- **Terraform**: Infrastructure management.

## Project Structure

Here is the structure of the project:

```plaintext
- analyses/               # Contains DBT analysis scripts.
- dags/                   # Airflow DAGs for task scheduling.
- macros/                 # Custom DBT macros.
- models/                 # DBT models for data transformation.
- scripts/                # Project setup scripts.
- seeds/                  # Raw data for seeding DBT models.
- snapshots/              # DBT snapshots for table versioning.
- spark_notebooks/        # Jupyter Notebooks for Spark-based analysis.
- terraf/                 # Terraform configuration files.
- tests/                  # DBT tests for data quality.
- .gitignore              # Git ignore file for unwanted files.
- Dockerfile              # Docker configuration.
- docker-compose.yaml     # Docker Compose configuration.
- requirements.txt        # Python dependencies.

The dataset contains Divvy bike-sharing trip data from 2020 to 2024. The columns include:

ride_id: Unique ID assigned to each Divvy trip.
rideable_type: Type of vehicle used (bike or scooter).
started_at: Start date and time of the trip.
ended_at: End date and time of the trip.
start_station_name: Name of the start station.
start_station_id: Unique ID of the start station.
end_station_name: Name of the end station.
end_station_id: Unique ID of the end station.
start_lat: Latitude of the start station.
start_lng: Longitude of the start station.
end_lat: Latitude of the end station.
end_lng: Longitude of the end station.
member_casual: Whether the rider is a Divvy member or a casual user.
Link to Dataset

Installation
Prerequisites
Install Python (version X.X.X).
Install Docker (for containerization).
Install DBT (for data transformation).
Install Terraform (for infrastructure).
Install Airflow (for scheduling).

  
