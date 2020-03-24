from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = SparkSession.builder.appName("04_Aggregations").getOrCreate()

    