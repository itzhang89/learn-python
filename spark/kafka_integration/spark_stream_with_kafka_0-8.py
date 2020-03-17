from pyspark.sql import SparkSession
from pyspark.streaming.kafka import KafkaUtils

"""
# guide link: https://spark.apache.org/docs/latest/streaming-kafka-integration.html
run script
$ /opt/spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.5 receive_message_from_kafka.py
"""

spark = SparkSession.builder.appName(name="kafka test").getOrCreate()

kafka_servers = ["192.168.1.8:9092"]
kafkaStream = KafkaUtils.createDirectStream(spark, topics=["gdelk_gkg"],
                                            kafkaParams={" bootstrap.servers": kafka_servers})

print(kafkaStream.count())
