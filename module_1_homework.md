## Question 1. Understanding docker first run

docker run -it --entrypoint=bash python:3.12.8

pip list

Package Version 

Answer : pip     24.3.1

## Question 2. Understanding Docker networking and docker-compose
Answer : postgres:5432

## Question 3. Trip Segmentation Count
Answer : 104802 ; 198924 ; 109603 ; 27678 ; 35189

SELECT 
	CASE
		WHEN trip_distance <= 1 THEN 'Up to 1 mile'
		WHEN trip_distance > 1 AND trip_distance <= 3 THEN 'In between 1 and 3 miles'
		WHEN trip_distance > 3 AND trip_distance <= 7 THEN 'In between 3 and 7 miles'
		WHEN trip_distance > 7 AND trip_distance <= 10 THEN 'In between 7 and 10 miles'
   		ELSE 'Over 10 miles'
	END AS distance,
	count(*) AS trip_count
FROM
    green_taxi_trips t
WHERE
    lpep_dropoff_datetime >= '2019-10-01 00:00:00'
    AND lpep_dropoff_datetime < '2019-11-01 00:00:00'
GROUP BY
    distance
ORDER BY
    trip_count DESC;

## Question 4. Longest trip for each day
Answer : 2019-10-11

SELECT
    DATE(lpep_pickup_datetime) AS "day",
    max(trip_distance) AS max_trip_distance
FROM
    green_taxi_trips t
WHERE
    lpep_pickup_datetime >= '2019-10-01 00:00:00'
    AND lpep_pickup_datetime < '2019-10-31 00:00:00'
GROUP BY
    DATE(lpep_pickup_datetime)
ORDER BY
    max_trip_distance DESC;

## Question 5. Three biggest pickup zones
Answer : East Harlem North, East Harlem South, Morningside Height

SELECT
    concat(zpu."Borough", ' / ', zpu."Zone") AS zone,
    sum(total_amount) AS total_amount
FROM
    green_taxi_trips g
JOIN 
    zones zpu ON g."PULocationID" = zpu."LocationID"
JOIN 
    zones zdo ON g."DOLocationID" = zdo."LocationID"
WHERE
    date(lpep_pickup_datetime) = '2019-10-18'
GROUP BY
	concat(zpu."Borough", ' / ', zpu."Zone")
ORDER BY
    total_amount DESC;

## Question 6. Largest tip

Answer : Upper East Side North

SELECT
    concat(zdo."Borough", ' / ', zdo."Zone") AS zone,
    SUM(tip_amount) AS total_tip_amount
FROM
    green_taxi_trips g
JOIN 
    zones zpu ON g."PULocationID" = zpu."LocationID"
JOIN 
    zones zdo ON g."DOLocationID" = zdo."LocationID"
WHERE
	zpu."Zone" = 'East Harlem North'
GROUP BY
	concat(zdo."Borough", ' / ', zdo."Zone")
ORDER BY
    total_tip_amount DESC;

## Question 7. Terraform Workflow



