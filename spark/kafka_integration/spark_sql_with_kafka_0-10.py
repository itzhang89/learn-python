from pyspark.sql import SparkSession

"""
# guide link: https://spark.apache.org/docs/2.4.4/structured-streaming-kafka-integration.html
run script
$ /opt/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5 spark_sql_with_kafka_0-10.py
"""

spark = SparkSession.builder.appName(name="kafka test").getOrCreate()

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "192.168.1.8:9092") \
    .option("subscribe", "gdelk_gkg") \
    .load()

df.limit(10).show
