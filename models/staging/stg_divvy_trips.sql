{{ config(materialized='view') }}

SELECT ride_id
,rideable_type
,member_casual
,started_at
,ended_at
,start_station_name
,end_station_name
,start_lat
,start_lng
,end_lat
,end_lng
,{{ start_date_to_day(started_at) }} as start_day
,{{ end_date_to_day(ended_at) }} as end_day
FROM {{ source('staging','divvy_data_partitioned')}}
WHERE start_station_name is not null
and end_station_name is not null