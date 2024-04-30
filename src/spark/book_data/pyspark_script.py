# # Import necessary libraries
# from pyspark.sql import SparkSession
    
# # Define the SparkSQL job
# def spark_sql_job():
#     # Create SparkSession
#     spark = SparkSession.builder \
#         .appName("PostgreSQL to Elasticsearch") \
#         .config("spark.jars.packages", "org.elasticsearch:elasticsearch-hadoop:7.15.2,org.postgresql:postgresql:42.2.24") \
#         .getOrCreate()

#     # Read data from PostgreSQL
#     df = spark.read \
#         .format("jdbc") \
#         .option("url", "jdbc:postgresql://postgres_store:5432/advertise") \
#         .option("dbtable", "ad_interaction") \
#         .option("user", "test") \
#         .option("password", "test") \
#         .load()

#     # Perform SparkSQL query
#     df.createOrReplaceTempView("temp_table")
#     result_df = spark.sql("SELECT * FROM temp_table")  # Your SQL query here

#     # Write data to Elasticsearch
#     # result_df.write \
#     #     .format("org.elasticsearch.spark.sql") \
#     #     .option("es.nodes", "elasticsearch") \
#     #     .option("es.port", "9200") \
#     #     .option("es.resource", "your_index/your_type") \
#     #     .save()
#     print(result_df)
#     # Stop SparkSession
#     spark.stop()

# if __name__ == '__main__':
#     spark_sql_job()


#### version two ##################################
# def spark_sql_job():

#     from pyspark.sql import SparkSession

#     spark = SparkSession.builder\
#         .appName("PostgreSQL to Elasticsearch")\
#         .config("spark.jars", "/opt/spark/data/postgresql-42.7.3.jar")\
#         .config("spark.driver.extraClassPath", "/opt/spark/data/postgresql-42.7.3.jar")\
#         .getOrCreate()

#     df = spark.read \
#       .format("jdbc") \
#       .option("url", "jdbc:postgresql://postgres_store:5432/advertise") \
#       .option("dbtable", "car_ad") \
#       .option("user", "test") \
#       .option("password", "test") \
#       .load()
    
#     df.show()

#     # try:
#     #     df.write \
#     #       .format("org.elasticsearch.spark.sql") \
#     #       .option("es.nodes", "elasticsearch") \
#     #       .option("es.port", "9200") \
#     #       .option("es.resource", "car_ad/index") \
#     #       .save()
#     # except Exception as e:
#     #     print(f"Error writing to Elasticsearch: {e}")

#     spark.stop()

# if __name__ == '__main__':
#     spark_sql_job()



############## versoin three ################################
# def spark_sql_job():
#     from pyspark.sql import SparkSession

#     spark = SparkSession.builder\
#        .appName("PostgreSQL to Elasticsearch")\
#        .config("spark.jars", "/opt/spark/data/postgresql-42.7.3.jar")\
#        .config("spark.driver.extraClassPath", "/opt/spark/data/postgresql-42.7.3.jar")\
#        .getOrCreate()

#     df = spark.read \
#      .format("jdbc") \
#      .option("url", "jdbc:postgresql://postgres_store:5432/advertise") \
#      .option("dbtable", "ad_interaction") \
#      .option("user", "test") \
#      .option("password", "test") \
#      .load()

#     # Register DataFrame as a temporary view
#     df.createOrReplaceTempView("ad_interaction_view")

#     # Define SQL query with filtering for last 6 hours
#     sql_query = """
#     SELECT 
#         ad_id,
#         SUM(CASE WHEN type = 'false' THEN 1 ELSE 0 END) AS clicks,
#         COUNT(*) AS total_interactions,
#         ROUND(SUM(CASE WHEN type = 'false' THEN 1.0 ELSE 0 END) / COUNT(*), 2) AS click_ratio
#     FROM 
#         ad_interaction_view
#     GROUP BY 
#         ad_id
#     """

#     # WHERE 
#     #     created_at > CURRENT_TIMESTAMP() - INTERVAL '6 HOURS'
#     # Execute SQL query
#     result = spark.sql(sql_query)

#     # Show the result
#     result.show()

#     spark.stop()

# if __name__ == '__main__':
#     spark_sql_job()

############# versin 4 ################################

# def spark_sql_job():
#     from pyspark.sql import SparkSession

#     spark = SparkSession.builder\
#        .appName("PostgreSQL to Elasticsearch")\
#        .config("spark.jars", "/opt/spark/data/postgresql-42.7.3.jar")\
#        .config("spark.driver.extraClassPath", "/opt/spark/data/postgresql-42.7.3.jar")\
#        .getOrCreate()

#     df_ad_interaction = spark.read \
#         .format("jdbc") \
#         .option("url", "jdbc:postgresql://postgres_store:5432/advertise") \
#         .option("dbtable", "ad_interaction") \
#         .option("user", "test") \
#         .option("password", "test") \
#         .load()

#     df_another_table = spark.read \
#         .format("jdbc") \
#         .option("url", "jdbc:postgresql://postgres_store:5432/advertise") \
#         .option("dbtable", "car_ad") \
#         .option("user", "test") \
#         .option("password", "test") \
#         .load()

#     # Register DataFrames as temporary views
#     df_ad_interaction.createOrReplaceTempView("ad_interaction")
#     df_another_table.createOrReplaceTempView("another_table")

#     # Define SQL query to compute click ratio
#     click_ratio_query = """
#     SELECT 
#         ad_id,
#         SUM(CASE WHEN type = 'false' THEN 1 ELSE 0 END) AS clicks,
#         COUNT(*) AS total_interactions,
#         ROUND(SUM(CASE WHEN type = 'false' THEN 1.0 ELSE 0 END) / COUNT(*), 2) AS click_ratio
#     FROM 
#         ad_interaction
#     GROUP BY 
#         ad_id
#     """

#     # Execute SQL query to compute click ratio
#     click_ratio_df = spark.sql(click_ratio_query)

#     click_ratio_df.createOrReplaceTempView("click_ratio_view")

#     # Define SQL query to perform join with another table
#     join_query = """
#     SELECT 
#         c.ad_id,
#         c.clicks,
#         c.total_interactions,
#         c.click_ratio,
#         a.*
#     FROM 
#         click_ratio_view c
#     JOIN 
#         car_ad a
#     ON 
#         c.ad_id = a.id
#     """

#     # Execute SQL query to perform join
#     result = spark.sql(join_query)

#     # Show the result
#     result.show()

#     # Insert the result into Elasticsearch
#     # result.write.format("org.elasticsearch.spark.sql") \
#     #     .option("es.resource", "advert/your_type") \
#     #     .option("es.nodes", "elasticsearch") \
#     #     .save()

#     spark.stop()

# if __name__ == '__main__':
#     spark_sql_job()


############## version 5 ##############################
from elasticsearch import Elasticsearch, helpers
from pyspark.sql import SparkSession

def spark_sql_job():
    # Initialize Spark
    spark = SparkSession.builder \
        .appName("PostgreSQL to Elasticsearch") \
        .config("spark.jars", "/opt/spark/data/postgresql-42.7.3.jar") \
        .config("spark.driver.extraClassPath", "/opt/spark/data/postgresql-42.7.3.jar") \
        .getOrCreate()

    # Read data from PostgreSQL
    df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres_store:5432/advertise") \
        .option("dbtable", "ad_interaction") \
        .option("user", "test") \
        .option("password", "test") \
        .load()

    # Perform any transformations, aggregations here
    df.createOrReplaceTempView("interactions")
    result_df = spark.sql("SELECT ad_id, COUNT(*) AS interactions FROM interactions GROUP BY ad_id")

    # Collect data to Python list of dictionaries (suitable for small datasets)
    results = result_df.collect()

    # Initialize Elasticsearch client
    es = Elasticsearch(["http://localhost:9200"])

    # Prepare bulk data
    def generate_data():
        for row in results:
            yield {
                "_index": "ad_interactions",
                "_id": row["ad_id"],  # Optional: Use if you have a unique identifier
                "_source": {
                    "ad_id": row["ad_id"],
                    "interactions": row["interactions"]
                }
            }

    # Perform bulk insert
    helpers.bulk(es, generate_data())

    spark.stop()

if __name__ == '__main__':
    spark_sql_job()
