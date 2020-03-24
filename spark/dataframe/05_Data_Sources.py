from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = SparkSession.builder.appName("05_Data_Sources").getOrCreate()

    # spark is an existing SparkSession
    data = [(None, "Michael"), (30, "Andy"), (19, "Justin")]
    df = spark.createDataFrame(data, schema=["age", "name"])

    # Generic Load/Save Functions
    df.select("name", "age").write.save("namesAndAges.parquet")

    # Manually Specifying Options
    # df = spark.read.load("examples/src/main/resources/people.json", format="json")
    df.select("name", "age").write.save("namesAndAges.parquet", format="parquet")

    # To load a CSV file you can use:
    df = spark.read.load("examples/src/main/resources/people.csv",
                         format="csv", sep=":", inferSchema="true", header="true")

    # Run SQL on files directly
    df = spark.sql("SELECT * FROM parquet.`examples/src/main/resources/users.parquet`")
