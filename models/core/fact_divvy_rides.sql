{{ config(materialized='table') }}

with dupe_recs as(
    SELECT *
    ,row_number()over(partition by ride_id order by start_station_name) as RowNbr
    FROM {{ ref('stg_divvy_trips') }}
)


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
,start_day
,end_day
FROM dupe_recs
WHERE RowNbr = 1