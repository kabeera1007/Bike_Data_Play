{% macro start_date_to_day(started_at) -%}

    FORMAT_DATE('%A', DATE(started_at))

{%- endmacro %}


{% macro end_date_to_day(ended_at) -%}

    FORMAT_DATE('%A', DATE(ended_at))

{%- endmacro %}


{% macro test(start_lat) -%}
    start_lat + 1

{%- endmacro %}