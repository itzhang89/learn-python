from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StringType, StructType


def Inferring_the_Schema_Using_Reflection(parts):
    people = parts.map(lambda p: Row(name=p[0], age=int(p[1])))
    # Infer the schema, and register the DataFrame as a table.
    schemaPeople = spark.createDataFrame(people)
    schemaPeople.createOrReplaceTempView("people")
    # SQL can be run over DataFrames that have been registered as a table.
    teenagers = spark.sql("SELECT name FROM people WHERE age >= 13 AND age <= 19")
    teenagers.show()
    # The results of SQL queries are Dataframe objects.
    # rdd returns the content as an :class:`pyspark.RDD` of :class:`Row`.
    teenNames = teenagers.rdd.map(lambda p: "Name: " + p.name).collect()
    for name in teenNames:
        print(name)
    # Name: Justin


def Programmatically_Specifying_the_Schema(parts):
    # Each line is converted to a tuple.
    people = parts.map(lambda p: (p[0], p[1].strip()))
    # The schema is encoded in a string.
    schemaString = ["name", "age"]
    fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
    schema = StructType(fields)
    # Apply the schema to the RDD.
    schemaPeople = spark.createDataFrame(people, schema)
    # Creates a temporary view using the DataFrame
    schemaPeople.createOrReplaceTempView("people")
    # SQL can be run over DataFrames that have been registered as a table.
    results = spark.sql("SELECT name FROM people")
    results.show()
    # +-------+
    # |   name|
    # +-------+
    # |Michael|
    # |   Andy|
    # | Justin|
    # +-------+


if __name__ == '__main__':
    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL basic example") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()

    # Convert list to RDD
    data = ["Michael, 29", "Andy, 30", "Justin, 19"]
    lines = spark.sparkContext.parallelize(data)
    parts = lines.map(lambda l: l.split(","))

    # Inferring_the_Schema_Using_Reflection(parts)

    # Programmatically_Specifying_the_Schema(parts)
