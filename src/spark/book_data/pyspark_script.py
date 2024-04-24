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
def spark_sql_job():
    from pyspark.sql import SparkSession

    spark = SparkSession.builder\
       .appName("PostgreSQL to Elasticsearch")\
       .config("spark.jars", "/opt/spark/data/postgresql-42.7.3.jar")\
       .config("spark.driver.extraClassPath", "/opt/spark/data/postgresql-42.7.3.jar")\
       .getOrCreate()

    df = spark.read \
     .format("jdbc") \
     .option("url", "jdbc:postgresql://postgres_store:5432/advertise") \
     .option("dbtable", "ad_interaction") \
     .option("user", "test") \
     .option("password", "test") \
     .load()

    # Register DataFrame as a temporary view
    df.createOrReplaceTempView("ad_interaction_view")

    # Define SQL query with filtering for last 6 hours
    sql_query = """
    SELECT 
        ad_id,
        SUM(CASE WHEN type = 'false' THEN 1 ELSE 0 END) AS clicks,
        COUNT(*) AS total_interactions,
        ROUND(SUM(CASE WHEN type = 'false' THEN 1.0 ELSE 0 END) / COUNT(*), 2) AS click_ratio
    FROM 
        ad_interaction_view
    WHERE 
        created_at > CURRENT_TIMESTAMP() - INTERVAL 6 HOURS
    GROUP BY 
        ad_id
    """

    # Execute SQL query
    result = spark.sql(sql_query)

    # Show the result
    result.show()

    spark.stop()

if __name__ == '__main__':
    spark_sql_job()

