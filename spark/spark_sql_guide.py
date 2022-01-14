from pyspark.sql import SparkSession

# Starting Point: SparkSession
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .master("local") \
    .getOrCreate()

# spark is an existing SparkSession
df = spark.read.json("examples/src/main/resources/people.json")
# Displays the content of the DataFrame to stdout
df.show()
# +----+-------+
# | age|   name|
# +----+-------+
# |null|Michael|
# |  30|   Andy|
# |  19| Justin|
# +----+-------+
