# Task 1

Deploy Cassandra cluster using Kubernetes and Docker. More details will be in "Cassandra_HELM_Setup" guide. You will need to enable Kubernetes and download binary version of Helm from https://helm.sh/ Use Cassandra container to do Homework.

When installing Cassandra using Helm I would suggest you to run `helm install bitnami/cassandra --set dbUser.password=cassandra --generate-name` instead of `helm install my-release bitnami/cassandra` since this may save you from getting some authentication errors.

Please download NOSQL_FILES.zip.

Proceed with steps 5-31 from NoSQL_Home.pdf. Please note that some steps where navigation to `home/ubuntu/…` is mentioned could be irrelevant and you’ll need to import appropriate file from NOSQL_FILES.zip to your Cassandra container instead.

**Expected Results:**
ZIP-ed folder with scripts used and screenshots with results of scripts executions.

# Connect via terminal

Add repository

```
helm repo add bitnami https://charts.bitnami.com/bitnami
```

Install Cassandra

```
helm install bitnami/cassandra --set dbUser.password=cassandra --generate-name
```

Then run terminal for docker
```
docker exec -it k8s_cassandra_cassandra-1637447437-0_default_cdadff52-be4b-4ad2-a5f3-f24dae39fba8_140 /bin/bash
```

# Tasks steps


## 5. In 'cqlsh', create a keyspace called 'killrvideo' and switch to that keyspace.
use SimpleStrategy' for the replication class 
with a replication factor of one Remember the •use' command switches keyspaces. 
NOTE: You can press the tab key within the CREATE KEYSPACE command to have 'cqlsh' autocomplete the replication 
parameters, 

Connect to cassandra shell:
```
$cqlsh -u cassandra -p $CASSANDRA_PASSWORD
Connected to cassandra at 127.0.0.1:9042
[cqlsh 6.0.0 | Cassandra 4.0.1 | CQL spec 3.4.5 | Native protocol v5]
Use HELP for help.
cassandra@cqlsh>
```


```
cassandra@cqlsh:killrvideo> CREATE KEYSPACE IF NOT EXISTS  killrvideo 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
```


## 6. Create a single table called 'videos' with the same structure as shown in table above. 'video_id' is the primary key. 

```
cassandra@cqlsh:killrvideo> USE killrvideo ;
CREATE TABLE IF NOT EXISTS videos (
    video_id timeuuid,
    added_date timestamp,
    description text,
    title text,
    user_id uuid,
    PRIMARY KEY (video_id));
```

## 7. Load the newly created table with the •videos.csv• file using the 'COPY command. 
COPY videos FROM 'videos.csv' WITH HEADER=true; 
NOTE: Notice COPY does not require column names when the target table schema and source CSV file columns match 
respectively. We will see more on table schema later. 

At first I need to upload files from local machine to one of nodes at cluster. For this run at local mashine:
```
>cd .\NoSQL\
>kubectl cp NoSQL_files cassandra-1637447437-0:/usr/
```
And then back to cqlsh.
```
cassandra@cqlsh:killrvideo>COPY videos FROM 'NoSQL_files/exercise-2/videos.csv' WITH HEADER = true ;
Using 3 child processes

Starting copy of killrvideo.videos with columns [video_id, added_date, description, title, user_id].
Processed: 430 rows; Rate:     510 rows/s; Avg. rate:     822 rows/s
430 rows imported from 1 files in 0.523 seconds (0 skipped).
```

## 8. use SELECT to verify the data loaded correctly. Include LIMIT to retrieve only the first 10 rows.

```
cassandra@cqlsh:killrvideo> select * FROM videos limit 10;

 video_id                             | added_date                      | description

    | title                                                                                             | user_id   
--------------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------+--------------------------------------
 26461a70-14bd-11e5-ad08-8438355b7e3a | 2014-05-07 00:00:00.000000+0000 |       At Comcast we are working on the future of television. Change and innovation are happening more rapidly than ever thanks to the cloud based X1 platform 
... |                                             Webinar: Building Blocks for the Future of Television | 10d5c76c-8767-4db3-8050-e19e015b524c
 2645e79c-14bd-11e5-a456-8438355b7e3a | 2011-10-21 00:00:00.000000+0000 | DataStax is the developer of DataStax Enterprise, a distributed, scalable, and highly available database platform that delivers optimal performance either on 
... |            DataStax Cassandra Tutorials - Understanding partitioning and replication in Cassandra | 10d5c76c-8767-4db3-8050-e19e015b524c
 9056808b-ca65-1bfb-9957-3bea148dfdce | 2015-03-09 00:00:02.000000+0000 |         New hire Chip (Chris Hemsworth) learns it's not easy working alongside Lucious (Kenan Thompson), Cookie (Sasheer Zamata), Jamal (Jay Pharoah), Hakeem 
... |                                                                                Empire Promo - SNL | 220077ff-be79-4f20-8603-1b9c97dbafa6
 264601a3-14bd-11e5-8c2e-8438355b7e3a | 2011-12-30 00:00:00.000000+0000 |         Tyler Hobbs - Flexibility: Python 
Clients for Apache Cassandra DataStax, the commercial leader in Apache Cassandra, along with the NYC Cassandra User 
... |                Cassandra NYC 2011: Tyler Hobbs - Flexibility: Python Clients for Apache Cassandra | 10d5c76c-8767-4db3-8050-e19e015b524c
 fe3c4045-6f37-1223-81be-250dc60cffc8 | 2015-01-16 22:46:44.000000+0000 |                           Saturday Night Live celebrates 40 years of laughs! Get more SNL on Hulu Plus: http://www.hulu.com/saturday-night-live Get more SNL: 
... |                                                      40 Years in the Making - Saturday Night Live | 539fd1b2-ff34-42c9-80cd-a34c91a772de
 2e8ecb4f-e92b-139b-8183-4df0e2a817bb | 2015-04-24 00:00:41.000000+0000 |  As new types of data sources emerge from 
cloud, mobile devices, social media and machine sensor devices, traditional databases hit the ceiling due to today's... |           Webinar: Don't leave your data in the dark - Optimize and simplify database performance | 53a8ea04-018b-44c2-a420-c059f3f57324
 2646123a-14bd-11e5-b9db-8438355b7e3a | 2012-08-20 00:00:00.000000+0000 |
                              Session: Cassandra in Action - Solving Big Data Problems Speaker: Eddie Satterly (Splunk) |                 C* 2012: Cassandra in Action - Solving Big Data Problems (Eddie Satterly, Splunk) | 10d5c76c-8767-4db3-8050-e19e015b524c
 bdb57288-e51c-1ff1-805d-c5f1e49c2c8b | 2015-01-19 08:00:00.000000+0000 |               Join Helena Edelson, Senior 
Software Engineer at DataStax as she introduces Apache Spark and Cassandra, discusses common use cases an​​d explain
s ... | Webinar | Streaming Big Data Analytics with Team Apache Spark & Spark Streaming, Kafka, Cassandra | 66b25618-683a-4603-b3c9-caa83cd789e9
 2646278f-14bd-11e5-88ea-8438355b7e3a | 2012-04-27 00:00:00.000000+0000 |   NoSQL is addressing some tough challenges that businesses have harnessing big data and consequently it's growing like a weed in the enterprise. But this is 
... |                             Webinar: Top 5 gotchas that prevent NoSQL from meeting business goals | 10d5c76c-8767-4db3-8050-e19e015b524c
 607df86e-2208-18a8-90aa-6d837c659f2f | 2015-02-09 00:00:01.000000+0000 |  Delegation allows you to use the user authentication and product subscription flow of your existing website as a replacement of the built-in flow in the API 
... |                            Delegating User Authentication and Product Subscription to a 3rd Party | 723f6f5f-3658-4449-90d0-4391d63e50a8

(10 rows)
```
## 9. Use SELECT to COUNT ( the number Of imported rows. 
It should match the number Of rows COPY reported as imported

```
cassandra@cqlsh:killrvideo> SELECT COUNT(*) FROM videos;

 count
-------
   430

(1 rows)

Warnings :
Aggregation query used without partition key
```
## 10. Use SELECT to find a row where the video_id=6c4cffb9-0dc4-1d59-af24-c960b5fc3652 

```
cassandra@cqlsh:killrvideo> SELECT * FROM videos where video_id = 6c4cffb9-0dc4-1d59-af24-c960b5fc3652;

 video_id                             | added_date                      | description





                                                                             | title
                                       | user_id
--------------------------------------+---------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------+--------------------------------------
 6c4cffb9-0dc4-1d59-af24-c960b5fc3652 | 2014-11-06 01:11:50.000000+0000 | Speaker: Luke Tillman, Language Evangelist at DataStaxnnKeyboard Cat, Nyan Cat, and of course the world famous Grumpy Cat--it seems like the Internet can’t get enough cat videos. If you were building an application to let users share and consume their fill of videos, how would you go about it? In this talk, we’ll take a look at the data model for KillrVideo, a sample video sharing application similar to YouTube where users can share videos, comment, rate them, and more. You’ll learn get a practical introduction to Cassandra data modeling, querying with CQL, how the application drives the data model, and how to shift your thinking from the relational world you probably have experience with. | Cassandra Day Denver 2014: A Cassandra Data Model for Serving up Cat Videos | fd3f7889-fc0c-43db-951c-7b77710898bc

(1 rows)
```

Next we Will explore some Other 
CQL commands that will come in handy, like TRUNCATE in a later exercise, we will show you how to add/remove (non-primary key) columns. 
## 11. Let's remove the data from our table using TRUNCATE .truncate videos; 

```
cassandra@cqlsh:killrvideo> TRUNCATE TABLE videos;
```
## 12. Create a second table in the 'killrvideo' keyspace called videos_by_title_year with the structure shown in above table. 
Be sure users can query this table on both 'title' and 'added_year' by combining them into the partition key. 

```
cassandra@cqlsh:killrvideo> CREATE TABLE IF NOT EXISTS 
videos_by_title_year (
    title text,
    added_year int,
    added_date timestamp,
    description text,
    user_id uuid,
    video_id timeuuid,
    PRIMARY KEY ((title, added_year))
    );
```

## 13. Load the data from the file using the 'COPY' command 


```
cassandra@cqlsh:killrvideo> COPY videos_by_title_year  FROM '/usr/NoSQL_files/exercise-3/videos_by_title_year.csv' WITH HEADER = true ;
Detected 4 core(s)
Using 3 child processes

Starting copy of killrvideo.videos_by_title_year with columns [title, added_year, added_date, description, user_id, video_id].
Closing queues...ws; Rate:     830 rows/s; Avg. rate:     830 rows/s
Closing queues...
Closing queues...
Processed: 430 rows; Rate:     415 rows/s; Avg. rate:     695 rows/s
430 rows imported from 1 files in 0.619 seconds (0 skipped).
```

## 15. Try running queries on the table to query on a specific 'title' and 'added_year'. 

Query by both added_year and title:

```
cassandra@cqlsh:killrvideo> SELECT * FROM videos_by_title_year WHERE title = 'ASP.NET Community Standup - April 7th, 2015' and added_year = 2015 ;

 title                                       | added_year | added_date                      | description | user_id                              | video_id
---------------------------------------------+------------+---------------------------------+-------------+--------------------------------------+--------------------------------------
 ASP.NET Community Standup - April 7th, 2015 |       2015 | 2015-04-09 08:00:02.000000+0000 |        null | a284468d-d20c-4745-8e20-5125386f2025 | 872f8113-22e9-1f31-9dfd-05ae3222feb7

(1 rows)
```

Try to query by added_year:

```
cassandra@cqlsh:killrvideo> SELECT * FROM videos_by_title_year WHERE title = 'ASP.NET Community Standup - April 7th, 2015' and year = 2015 ;
InvalidRequest: Error from server: code=2200 [Invalid query] message="Undefined column name year in table killrvideo.videos_by_title_year"
```
Try to query by title:
```
cassandra@cqlsh:killrvideo> SELECT * FROM videos_by_title_year WHERE title = 'ASP.NET Community Standup - April 7th, 2015';
InvalidRequest: Error from server: code=2200 [Invalid query] message="Cannot execute this query as it might involve data filtering and thus may have unpredictable performance. If you want to execute this query despite the performance unpredictability, use ALLOW FILTERING"
cassandra@cqlsh:killrvideo>
```
(Errors due partition applied to both columns)

## 16. What error does Cassandra return when you tiy to query on just title or just year? Why? 
## 17. Create a table with the columns above to facilitate querying for videos by tag within a given year range returning the 
results in descending order by year. 
## 18. we wrote most of the CREATE TABLE for you. Fill in the PRIMARY KEY and CLUSTERING ORDER BY. 

```
cassandra@cqlsh:killrvideo> CREATE TABLE IF NOT EXISTS 
                                videos_by_tag_year (
                                    tag text,
                                    added_year int,
                                    video_id timeuuid,
                                    added_date timestamp,
                                    description text,
                                    title text,
                                    user_id uuid,
                                    PRIMARY KEY (tag, added_year, video_id)
                                    )
                                    WITH CLUSTERING ORDER BY (added_year DESC, video_id);
```
## 19. Load the data from the file in the provided 'exercise=4' directory using the COPY command. 
COPY videos_by_tag_year FROM WITH HEADER = true; 

```
cassandra@cqlsh:killrvideo> COPY videos_by_tag_year (tag, added_year, video_id, added_date, description, title, user_id)
                            FROM '/usr/NoSQL_files/exercise-4/videos_by_tag_year.csv' 
                            WITH HEADER = true;
Detected 4 core(s)
Using 3 child processes

Starting copy of killrvideo.videos_by_tag_year with columns [tag, added_year, video_id, added_date, description, title, user_id].
Closing queues...ws; Rate:    1314 rows/s; Avg. rate:    1314 rows/s
Closing queues...
Closing queues...
Processed: 797 rows; Rate:     657 rows/s; Avg. rate:    1126 rows/s
797 rows imported from 1 files in 0.708 seconds (0 skipped).
```

## 20. Check the number of rows in the table. 

NOTE: The number of rows should match the number of rows imported by the COPY command 
If not, you had upserts again and will need to adjust your PRIMARY KEY. Ask your instructor for help if necessary. 

```
cassandra@cqlsh:killrvideo> SELECT COUNT(*) FROM videos_by_tag_year;

 count 
-------
   797

(1 rows)

Warnings :
Aggregation query used without partition key


```
## 21. Try running queries on the table to query on a specific tag and added year. 

```
cassandra@cqlsh:killrvideo> SELECT * FROM videos_by_tag_year where tag = 'cql' AND added_year = 2014 limit 3;

 tag | added_year | video_id                             | added_date                      | description
                                         | title                                                           | user_id
-----+------------+--------------------------------------+---------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------+--------------------------------------
 cql |       2014 | b68132a3-7a41-10b3-9d9e-f60d2acf59bd | 2014-11-05 03:45:47.000000+0000 | Speaker: J.B. Langston Company: DataStax I'll give a general lay of the land for troubleshooting Cassandra. I'll show you what to look for in the logs, what ... | The Last Pickle: Lesser Known Features of Cassandra 2.0 and 2.1 | fd3f7889-fc0c-43db-951c-7b77710898bc

(1 rows)

```
## 22. Try querying for all videos with tag "cql" added before the year 2015. Notice you can do range queries on clustering columns. 

```
cassandra@cqlsh:killrvideo> SELECT * FROM videos_by_tag_year where tag = 'cassandra' AND added_year < 2015 limit 5;

 tag       | added_year | video_id                             | added_date                      | description
                                                            | title                                                                       | user_id
-----------+------------+--------------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------+--------------------------------------
 cassandra |       2014 | a9a2c9cf-bbfa-1fbd-96bb-f3f2ce15b0a7 | 2014-11-05 03:42:42.000000+0000 |
                                    Cassandra Days 2015 LA  |      Activision Blizzard (Demonware): Deploying Cassandra for Call of Duty  | fd3f7889-fc0c-43db-951c-7b77710898bc
 cassandra |       2014 | 6c4cffb9-0dc4-1d59-af24-c960b5fc3652 | 2014-11-06 01:11:50.000000+0000 | Carlito tries to show the members of his gang how wild and crazy he can be after a new initiate is labeled the loco one.\nnWatch more Key & Peele: http://on.cc.com/1FOng7W"" | Cassandra Day Denver 2014: A Cassandra Data Model for Serving up Cat Videos | fd3f7889-fc0c-43db-951c-7b77710898bc
 cassandra |       2014 | dab20eb0-e9a3-1a47-8fc2-672b8bccfbb0 | 2014-11-05 03:44:13.000000+0000 |                                                                      Grumpy cat takes a nap on top of my niece. Check out our website: www.grumpycats.com New Tshirts at: ... |              Databricks: Apache Spark - The SDK for All Big Data Platforms  | fd3f7889-fc0c-43db-951c-7b77710898bc
 cassandra |       2014 | 1ecbd956-384c-16f0-923b-961376bb53d1 | 2014-11-05 03:40:57.000000+0000 |                          Subscribe to TRAILERS: http://bit.ly/sxaw6h Subscribe to COMING SOON: http://bit.ly/H2vZUn Like us on FACEBOOK: http://goo.gl/dHs73 Follow us on ... |  ING: Apache Cassandra at ING — Testing the Waters – Consistency Required!  | fd3f7889-fc0c-43db-951c-7b77710898bc
 cassandra |       2014 | afc64520-ec0c-15f1-a871-cc6e12177ecf | 2014-03-27 08:01:24.000000+0000 |
                                                       null |                                      Getting Started with Spark & Cassandra | b5e2274f-52b9-4462-b58a-c58d88ae8a44

(5 rows)
```
## 23. Try querying for all videos added before 2015. The query will fail. What error message does cqlsh report? Why did the query fail whereas the previous query worked? 

```
cassandra@cqlsh:killrvideo> SELECT * FROM videos_by_tag_year WHERE added_date < 2015 limit 3;
InvalidRequest: Error from server: code=2200 [Invalid query] message="Cannot execute this query as it might involve data filtering and thus may have unpredictable performance. If you want to execute this query despite the performance unpredictability, use ALLOW FILTERING"
```
`Field "Tag" is used for partition, which may locate data in datacenter at another continent, so if  not used in WHERE condirion may cause unpredictable behaviour`

## 24. At the prompt, navigate to '/home/ubuntu/labwork/udts'. Launch 'cqlsh' and switch to the 'killrvideo• keyspace. 
## 25. Run the TRUNCATE command to erase the data from the •videos' table. 

```
cassandra@cqlsh:killrvideo>TRUNCATE TABLE videos;
```
## 26. Alter the 'videos' table to add a 'tags' column, 

```
cassandra@cqlsh:killrvideo> ALTER TABLE videos ADD tags text;
```
## 27. Load the data from the 'videos.csv' file using the COPY command. COPY videos FROM 'videos.csv' WITH HEADER=true; 

```
cassandra@cqlsh:killrvideo> COPY videos FROM 'usr/NoSQL_files/exercise-5/videos.csv' WITH HEADER = true ;
Detected 4 core(s)
Using 3 child processes

Starting copy of killrvideo.videos with columns [video_id, added_date, description, tags, title, user_id].
Closing queues...ws; Rate:     786 rows/s; Avg. rate:     786 rows/s
Closing queues...
Closing queues...
Processed: 430 rows; Rate:     393 rows/s; Avg. rate:     662 rows/s
430 rows imported from 1 files in 0.650 seconds (0 skipped).
```

Remember, we do not need to create the user defined type called 'video_encoding' because we did so in the previous 
exercise. However, take a look at the code below as a refresher. Do not run it again or you will get an error! 

```
CREATE TYPE video_encoding ( 
bit_rates SET<TEXT>,
encoding TEXT, 
height INT, 
width INT, 
);
```
## 28. Alter your table to add an 'encoding' column of the 'video_encoding' type. 

```
ALTER TABLE videos add encoding video_encoding;
```

# 29. Load the data from the 'videos_encoding.csv' file using the COPY command. 

```
COPY videos (video_id, encoding) FROM 'usr/NoSQL_files/exercise-5/videos_encoding.csv' WITH HEADER = true;
```

# 30. Run a query to retrieve the first 10 rows of the 'videos' table. 
Notice the altered table contains data for the new 'tags' and 'encoding' column. 

```
cassandra@cqlsh:killrvideo> SELECT * FROM videos limit 10;

 video_id                             | added_date                      | description
                                                        | encoding                                                                                           | tags
                 | title                                                                                             | user_id
--------------------------------------+---------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------+---------------------------------------+---------------------------------------------------------------------------------------------------+--------------------------------------
 26461a70-14bd-11e5-ad08-8438355b7e3a | 2014-05-07 00:00:00.000000+0000 |       At Comcast we are working on the future of television. Change and innovation are happening more rapidly than ever thanks to the cloud based X1 platform ... | {bit_rates: {'3000 Kbps', '4500 Kbps', '6000 Kbps'}, encoding: '1080p', height: 1080, width: 1920} |               {'webinar','cassandra'} |                                             Webinar: Building Blocks for the Future of Television | 10d5c76c-8767-4db3-8050-e19e015b524c
 2645e79c-14bd-11e5-a456-8438355b7e3a | 2011-10-21 00:00:00.000000+0000 | DataStax is the developer of DataStax Enterprise, a distributed, scalable, and highly available database platform that delivers optimal performance either on ... | {bit_rates: {'3000 Kbps', '4500 Kbps', '6000 Kbps'}, encoding: '1080p', height: 1080, width: 1920} |              {'cassandra','tutorial'} |            DataStax Cassandra Tutorials - Understanding partitioning and replication in Cassandra | 10d5c76c-8767-4db3-8050-e19e015b524c
 9056808b-ca65-1bfb-9957-3bea148dfdce | 2015-03-09 00:00:02.000000+0000 |         New hire Chip (Chris Hemsworth) learns it's not easy working alongside Lucious (Kenan Thompson), Cookie (Sasheer Zamata), Jamal (Jay Pharoah), Hakeem ... | {bit_rates: {'3000 Kbps', '4500 Kbps', '6000 Kbps'}, encoding: '1080p', height: 1080, width: 1920} |
         {'snl'} |                                                                                Empire Promo - SNL | 220077ff-be79-4f20-8603-1b9c97dbafa6
 264601a3-14bd-11e5-8c2e-8438355b7e3a | 2011-12-30 00:00:00.000000+0000 |         Tyler Hobbs - Flexibility: Python Clients for Apache Cassandra DataStax, the commercial leader in 
Apache Cassandra, along with the NYC Cassandra User ... | {bit_rates: {'3000 Kbps', '4500 Kbps', '6000 Kbps'}, encoding: '1080p', height: 1080, width: 1920} |                {'cassandra','python'} |                Cassandra NYC 2011: Tyler Hobbs - Flexibility: Python Clients for Apache Cassandra | 10d5c76c-8767-4db3-8050-e19e015b524c
 fe3c4045-6f37-1223-81be-250dc60cffc8 | 2015-01-16 22:46:44.000000+0000 |                           Saturday Night Live celebrates 40 years of laughs! Get more SNL on Hulu Plus: http://www.hulu.com/saturday-night-live Get more SNL: ... | {bit_rates: {'3000 Kbps', '4500 Kbps', '6000 Kbps'}, encoding: '1080p', height: 1080, width: 1920} |        {'saturday night live', 'snl'} |                                                      40 Years in the Making - Saturday Night Live | 539fd1b2-ff34-42c9-80cd-a34c91a772de
 2e8ecb4f-e92b-139b-8183-4df0e2a817bb | 2015-04-24 00:00:41.000000+0000 |  As new types of data sources emerge from cloud, mobile devices, social media and machine sensor devices, 
traditional databases hit the ceiling due to today's... | {bit_rates: {'3000 Kbps', '4500 Kbps', '6000 Kbps'}, encoding: '1080p', height: 1080, width: 1920} |                 {'cloud', 'database'} |           Webinar: Don't leave your data in the dark - Optimize and simplify database performance | 53a8ea04-018b-44c2-a420-c059f3f57324
 2646123a-14bd-11e5-b9db-8438355b7e3a | 2012-08-20 00:00:00.000000+0000 |                                                                         Session: Cassandra in Action - Solving Big Data Problems Speaker: Eddie Satterly (Splunk) | {bit_rates: {'3000 Kbps', '4500 Kbps', '6000 Kbps'}, encoding: '1080p', height: 1080, width: 1920} |              {'cassandra','big data'} |                 C* 2012: Cassandra in Action - Solving Big Data Problems (Eddie Satterly, Splunk) | 10d5c76c-8767-4db3-8050-e19e015b524c
 bdb57288-e51c-1ff1-805d-c5f1e49c2c8b | 2015-01-19 08:00:00.000000+0000 |               Join Helena Edelson, Senior Software Engineer at DataStax as she introduces Apache Spark and Cassandra, discusses common use cases an​​d explains ... | {bit_rates: {'3000 Kbps', '4500 Kbps', '6000 Kbps'}, encoding: '1080p', height: 1080, width: 1920} | {'big data', 'cassa
ndra', 'datastax'} | Webinar | Streaming Big Data Analytics with Team Apache Spark & Spark Streaming, Kafka, Cassandra | 66b25618-683a-4603-b3c9-caa83cd789e9
 2646278f-14bd-11e5-88ea-8438355b7e3a | 2012-04-27 00:00:00.000000+0000 |   NoSQL is addressing some tough challenges that businesses have harnessing big data and consequently it's growing like a weed in the enterprise. But this is ... | {bit_rates: {'3000 Kbps', '4500 Kbps', '6000 Kbps'}, encoding: '1080p', height: 1080, width: 1920} |                   {'webinar','nosql'} |                             Webinar: Top 5 gotchas that prevent NoSQL from meeting business goals | 10d5c76c-8767-4db3-8050-e19e015b524c
 607df86e-2208-18a8-90aa-6d837c659f2f | 2015-02-09 00:00:01.000000+0000 |  Delegation allows you to use the user authentication and product subscription flow of your existing website as a replacement of the built-in flow in the API ... | {bit_rates: {'3000 Kbps', '4500 Kbps', '6000 Kbps'}, encoding: '1080p', height: 1080, width: 1920} |
         {'cat'} |                            Delegating User Authentication and Product Subscription to a 3rd Party | 723f6f5f-3658-4449-90d0-4391d63e50a8

(10 rows)

```

# 31. Exit cqlsh 


