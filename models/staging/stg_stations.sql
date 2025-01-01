{{ config(materialized='view') }}

SELECT distinct start_station_name as station_name
FROM {{ source('staging','external_divvy_data')}}
union distinct
SELECT distinct end_station_name as station_name
FROM {{ source('staging','external_divvy_data')}}