src/airflow/include/pyspark_script.py# Import necessary libraries
from pyspark.sql import SparkSession
    
# Define the SparkSQL job
def spark_sql_job():
    # Create SparkSession
    spark = SparkSession.builder \
        .appName("PostgreSQL to Elasticsearch") \
        .config("spark.jars.packages", "org.elasticsearch:elasticsearch-hadoop:7.15.2,org.postgresql:postgresql:42.2.24") \
        .getOrCreate()

    # Read data from PostgreSQL
    df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres_store:5432/advertise") \
        .option("dbtable", "ad_interaction") \
        .option("user", "test") \
        .option("password", "test") \
        .load()

    # Perform SparkSQL query
    df.createOrReplaceTempView("temp_table")
    result_df = spark.sql("SELECT * FROM temp_table")  # Your SQL query here

    # Write data to Elasticsearch
    # result_df.write \
    #     .format("org.elasticsearch.spark.sql") \
    #     .option("es.nodes", "elasticsearch") \
    #     .option("es.port", "9200") \
    #     .option("es.resource", "your_index/your_type") \
    #     .save()
    print(result_df)
    # Stop SparkSession
    spark.stop()

if __name__ == '__main__':
    spark_sql_job()