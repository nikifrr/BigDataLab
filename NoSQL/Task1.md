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


5. In 'cqlsh', create a keyspace called 'killrvideo' and switch to that keyspace. use SimpleStrategy' for the replication class 
with a replication factor of one Remember the •use' command switches keyspaces. 
NOTE: You can press the tab key within the CREATE KEYSPACE command to have 'cqlsh' autocomplete the replication 
parameters, 

```
CREATE KEYSPACE IF NOT EXISTS  killrvideo 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
```


6. Create a single table called 'videos' with the same structure as shown in table above. 'video_id' is the primary key. 

```
USE killrvideo ;
CREATE TABLE IF NOT EXISTS videos (
    video_id timeuuid,
    added_date timestamp,
    description text,
    title text,
    user_id uuid,
    PRIMARY KEY (video_id));
```

7. Load the newly created table with the •videos.csv• file using the 'COPY command. 
COPY videos FROM 'videos.csv' WITH HEADER=true; 
NOTE: Notice COPY does not require column names when the target table schema and source CSV file columns match 
respectively. We will see more on table schema later. 
8. use SELECT to verify the data loaded correctly. Include LIMIT to retrieve only the first 10 ronrs. 
9. Use SELECT to COUN T ( the number Of imported rows. It should match the number Of rows COPY reported as imported 
I O. Use SELECT to find a row where the video_id Next we Will explore some Other 
CQL commands that will come in handy, like TRUNCATE in a later exercise, we will show you how to add/remove (non- 
primary key) columns. 
ll. Let's remove the data from our table using TRUNCATE .truncate videos; 
12. Create a second table in the 'killrvideo' keyspace called with the structure shown in above table. 
Be sure users can query this table on both 'title' and •added_year• by combining them into the partition key. 
13. Load the data from the file using the • COPY' command 
14. COPY FROM WITH HEADER=true; 
15. Try running queries on the table to query on a specific 'title' and 'added_year'. 
16. What error does Cassandra return when you tiy to query on just title or just year? Why? 
17. Create a table with the columns above to facilitate querying for videos by tag within a given year range returning the 
results in descending order by year. 
18. we wrote most of the CREATE TABLE for you. Fill in the PRIMARY KEY and CLUSTERING ORDER BY. 
19. Load the data from the file in the provided 'exercise=4' directory using the COPY command. 
COPY videos_by_tag_year FROM WITH HEADER:true; 
20. Check the number of rows in the table. 
NOTE: The number of rows should match the number of rows imported by the COPY command 
If not, you had upserts again and will need to adjust your PRIMARY KEY. Ask your instructor for help if necessary. 
21. Try running queries on the table to query on a specific tag and added year. 
22. Try querying for all videos with tag "cql" added before the year 2015. Notice you can do range queries on clustering 
columns. 
23. Try querying for all videos added before 2015. The query will fail. What error message does cqlsh report? Why did the 
query fail whereas the previous query worked? 
24. At the prompt, navigate to '/home/ubuntu/labwork/udts'. Launch 'cqlsh' and switch to the 'killrvideo• keyspace. 
25. Run the TRUNCATE command to erase the data from the •videos' table. 
26. Alter the 'videos' table to add a 'tags' column, 
27. Load the data from the 'videos.csv' file using the COPY command. COPY videos FROM 'videos.csv' WITH HEADER=true; 
Remember, we do not need to create the user defined type called 'video_encoding because we did so in the previous 
exercise. However, take a look at the code below as a refresher. Do not run it again or you will get an error! 
28. Alter your table to add an 'encoding' column of the •video_encoding' type. 
29. Load the data from the 'videos_encoding.csv' file using the COPY command. 
COPY videos (video_id, encoding) FROM •videos_encoding.csv• WITH HEADER2true; 
30. Run a query to retrieve the first 10 rows of the 'videos' table. Notice the altered table contains data for the new 'tags' 
and 'encoding' column. 
31. Exit cqlsh 


