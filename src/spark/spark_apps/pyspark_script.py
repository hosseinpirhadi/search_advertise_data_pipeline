
def spark_sql_job():
    from pyspark.sql import SparkSession
    from elasticsearch import Elasticsearch
    from elasticsearch.helpers import bulk

    spark = SparkSession.builder\
       .appName("PostgreSQL to Elasticsearch")\
       .config("spark.jars", "/opt/spark/data/postgresql-42.7.3.jar")\
       .config("spark.driver.extraClassPath", "/opt/spark/data/postgresql-42.7.3.jar")\
       .getOrCreate()

    df_ad_interaction = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres_store:5432/advertise") \
        .option("dbtable", "ad_interaction") \
        .option("user", "test") \
        .option("password", "test") \
        .load()

    df_another_table = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres_store:5432/advertise") \
        .option("dbtable", "car_ad") \
        .option("user", "test") \
        .option("password", "test") \
        .load()

    # Register DataFrames as temporary views
    df_ad_interaction.createOrReplaceTempView("ad_interaction")
    df_another_table.createOrReplaceTempView("car_ad")

    # Define SQL query to compute click ratio
    click_ratio_query = """
    SELECT 
        ad_id,
        SUM(CASE WHEN type = 'false' THEN 1 ELSE 0 END) AS clicks,
        COUNT(*) AS total_interactions,
        ROUND(SUM(CASE WHEN type = 'false' THEN 1.0 ELSE 0 END) / COUNT(*), 2) AS click_ratio
    FROM 
        ad_interaction
    GROUP BY 
        ad_id
    """

    # Execute SQL query to compute click ratio
    click_ratio_df = spark.sql(click_ratio_query)

    click_ratio_df.createOrReplaceTempView("click_ratio_view")

    # Define SQL query to perform join with another table
    join_query = """
    SELECT 
        c.ad_id,
        c.clicks,
        c.total_interactions,
        c.click_ratio,
        a.*
    FROM 
        click_ratio_view c
    JOIN 
        car_ad a
    ON 
        c.ad_id = a.id
    """

    # Execute SQL query to perform join
    result = spark.sql(join_query)

    # Show the result
    result.show()

    result_list = result.collect()

    result_pandas = result.toPandas()

    # Convert Pandas DataFrame to list of dictionaries
    result_data = result_pandas.to_dict(orient='records')

    def insert_into_elasticsearch(data):
        es = Elasticsearch(['http://elasticsearch:9200'])

        for row in data:
            es.index(index='advert', body=row)

    # Insert data into Elasticsearch
    insert_into_elasticsearch(result_data)
    
    spark.stop()

if __name__ == '__main__':
    spark_sql_job()
