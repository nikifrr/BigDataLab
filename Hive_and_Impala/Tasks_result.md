# Task 1

## 1. External table for struct_cities.json

> 1) CREATE EXTERNAL TABLE (struct_cities.json). 
NOTE: to work with json Hive needs SerDe to be added. Please copy to your external folder (/src/) json-serde-1.3-jar-with-dependencies.jar attached to the lesson materials and command ADD JAR /src/json-serde-1.3-jar-with-dependencies.jar; 
before DDL expression. Required SerDe name is 'org.openx.data.jsonserde.JsonSerDe'

**Process**: Add raw json to external table --> make query to select "flat" table


### Create nested table from json

```

ADD JAR     hdfs:///user/hive/jars/json-serde-1.3-jar-with-dependencies.jar;
create database if not exists hive_hw;
use hive_hw;


drop table if exists  struct_cities ;
create external table struct_cities 
                                ( 
                                   country_code string
                                 , cities array  
                                            < struct
                                                  < code:string
                                                  , city:string
                                                  , timezone:string
                                                  , available_2017:string
                                                  , available_2016:string
                                                  , available_2015:string
                                                  >
                                            >
                                      
                                ) 
                      row format  SERDE 'org.openx.data.jsonserde.JsonSerDe'
                      location '/user/hive/warehouse/struct_cities';

```
Result table:

![screen_json](./screenshots/Raw_Json_query.png)


### Query as flat table from nested
```
select   country_code
       , code as cities_code
       , city as cities_city
       , timezone as cities_timezone
       , avalible_2017 as cities_avalible_2017
       , avalible_2016 as cities_avalible_2016
       , avalible_2015 as cities_avalible_2015
    -- , cities as raw_json_array
      
from struct_cities
lateral view inline(cities) city as code, city, timezone, avalible_2017, avalible_2016, avalible_2015;
```
Job takes ~ 11 seconds:
![lat_view](./screenshots/lateral_view_inilne-Job_Browser.png)

result:
![lat_view](./screenshots/lateral_view_inilne-Query_Result.png)


## 2. Load data inpath (test.csv)

> CREATE TABLE + LOAD DATA INPATH OVERWRITE INTO TABLE . Note that Hive consumed the data file *.csv during this step. If you look in the File Browser you will see .csv is no longer there. Copy hive script to archive. (test.csv)

```
create table test 
              ( 
               id int
              ,date_time timestamp
              ,site_name string
              ,posa_continent  int
              ,user_location_country int
              ,user_location_region int
              ,user_location_city int
              ,orig_destination_distance float
              ,user_id int
              ,is_mobile int 
              ,is_package int
              ,channel int 
              ,srch_ci date 
              ,srch_co date
              ,srch_adults_cnt int
              ,srch_children_cnt int 
              ,srch_rm_cnt int
              ,srch_destination_id int
              ,srch_destination_type_id int
              ,hotel_continent int
              ,hotel_country int
              ,hotel_market int
              )
              row format delimited fields terminated by ','
              tblproperties ("skip.header.line.count"="1");
              
              
load data inpath '/user/hive/warehouse/test/test.csv' overwrite
into table test;
```

![inpath](./screenshots/load_inpath_Hive-Query.png)

## 3. Clustering train.csv
> 3) CREATE TABLE  CLUSTERED BY (hotel_country) SORTED BY (hotel_country) INTO 32 BUCKETS . (train.csv)


-- 3) CREATE TABLE  CLUSTERED BY (hotel_country) SORTED BY (hotel_country) INTO 32 BUCKETS . (train.csv)

drop table if exists train;

```
create external table train
                        (
                        date_time timestamp
                        ,site_name int
                        ,posa_continent int
                        ,user_location_country int
                        ,user_location_region int
                        ,user_location_city int
                        ,orig_destination_distance float
                        ,user_id int
                        ,is_mobile int
                        ,is_package int
                        ,channel int 
                        ,srch_ci date
                        ,srch_co date
                        ,srch_adults_cnt int
                        ,srch_children_cnt int
                        ,srch_rm_cnt int 
                        ,srch_destination_id int 
                        ,srch_destination_type_id int
                        ,is_booking int
                        ,cnt int
                        ,hotel_continent int
                        ,hotel_country int
                        ,hotel_market int
                        ,hotel_cluster int
                        )
            clustered by (hotel_country) sorted by (hotel_country) into 32 buckets
            row format delimited fields terminated by ','
            location '/user/hive/warehouse/train'
            tblproperties ("skip.header.line.count"="1");
                        
```

Result:

![](./screenshots/train_external_table_Hive-Query.png)


### 4. CTAS
> Using CTAS (Create table as select) create table ‘test_parquet’ stored as parquet from ‘test’ table created in 1.2 The largest table should be created twice: without bucketing and using bucketing • Write hive script to calculate Top 3 most popular countries where booking is successful (booking = 1), make screenshots before and after script execution, copy hive script to archive.

Hive  catch error (code 2) (needs memory/optimization)
Task done in Impala.

Without bucketing:

```
create table test_parquet
stored as parquet
as   
select *  from test;
```

With bucketing:


![CTAS](./screenshots/CTAS_parquet_Impala-Query.png) 


### 5. Top 3 countries

TODO: try window function

> Write hive script to calculate Top 3 most popular countries where booking is successful (booking = 1), make screenshots before and after script execution, copy hive script to archive.

Query for Hive (not support ordering by count(*), need subquery ):

```
select * from
  (
   select hotel_country,  count(*) as cnt from train 
   where is_booking = 1
   group by hotel_country
  ) t
order by cnt desc limit 3;
```

Query for Impala (30x faster, suport count(*) in order by clause):
```
select hotel_country,  count(*) as cnt from train 
where is_booking = 1
group by hotel_country
order by count(*) desc limit 3;
```
Result (Hive):

![s](./screenshots/hive_top_3_country.png)


# Task 3 

> Write hive script to calculate top 3 most popular hotels (treat hotel as composite key of continent, country and market) which were not booked. Most popular means most searches in dataset. Not booked means column booked = 0, make screenshots before and after script execution, copy hive script to archive.




Result (Hive):

```
select * from
  (
   select hotel_continent, hotel_country, hotel_market,  count(*) as cnt from train 
   where is_booking = 1
   group by hotel_continent, hotel_country, hotel_market
  ) t
order by cnt desc limit 3;
```
Impala:

```
select hotel_continent, hotel_country, hotel_market,  count(*) as cnt from train 
where is_booking = 1
group by hotel_continent, hotel_country, hotel_market
order by count(*) desc limit 3;
```


Result (Hive):
![top3](./screenshots/hive_top_3_hotel.png)
Result (Impala):
![top3](./screenshots/impala_top_3_hotel.png)



