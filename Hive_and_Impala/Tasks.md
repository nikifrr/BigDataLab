# Task 1

```
•         Write the script with DDL for creating tables using:
1) CREATE EXTERNAL TABLE (struct_cities.json). 
NOTE: to work with json Hive needs SerDe to be added. Please copy to your external folder (/src/) json-serde-1.3-jar-with-dependencies.jar attached to the lesson materials and command ADD JAR /src/json-serde-1.3-jar-with-dependencies.jar; 
before DDL expression. Required SerDe name is 'org.openx.data.jsonserde.JsonSerDe'
2) CREATE TABLE +  LOAD DATA INPATH OVERWRITE INTO TABLE . Note that Hive consumed the data file *.csv during this step. If you look in the File Browser you will see .csv is no longer there. Copy hive script to archive. (test.csv)
3) CREATE TABLE  CLUSTERED BY (hotel_country) SORTED BY (hotel_country) INTO 32 BUCKETS . (train.csv)
4) Using CTAS (Create table as select) create table ‘test_parquet’ stored as parquet from ‘test’ table created in 1.2
The largest table should be created twice: without bucketing and using bucketing
•         Write hive script to calculate Top 3 most popular countries where booking is successful (booking = 1), make screenshots before and after script execution, copy hive script to archive.
```

## Copy json 
```
$hdfs dfs -mkdir /user/hive/warehouse/struct_cities
$hdfs dfs -put /src/struct_cities.json /user/hive/warehouse/struct_cities/struct_cities.json 
```

## Script for creating table

```
ADD JAR     hdfs:///user/hive/jars/json-serde-1.3-jar-with-dependencies.jar;
use hive_hw;

-- creata external table

drop table if exists  struct_cities 
;

create external table struct_cities 
                      ( 
                        country_code struct <
                              cities array  <
                                         struct  <
                                           code:int
                                         , city:string
                                         , timezone:
                                         , available_string2017:boolean
                                         , available_2016:boolean
                                         , available_2015:boolean
                                       >>>
                      ) 
                      
                    --  partitioned by (country_code int)
                      row format  SERDE 'org.openx.data.jsonserde.JsonSerDe'
                      location '/user/hive/warehouse/struct_cities'
                        ;
                      
-- LOAD DATA LOCAL INPATH   '/user/hive/warehouse/struct_cities/struct_cities.json' OVERWRITE INTO TABLE struct_cities;

select * from struct_cities
```