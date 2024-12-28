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
,date_diff(ended_at, started_at, MINUTE) as duration_mnts
,date_diff(ended_at, started_at, HOUR) as duration_hrs
,start_day
,end_day
FROM {{ ref('stg_divvy_trips')}}
WHERE start_station_name is not null
and end_station_name is not null
and date_diff(ended_at, started_at, HOUR) > 18