from pyspark import Row
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

if __name__ == '__main__':
    spark = SparkSession.builder.appName("04_Aggregations").getOrCreate()

    # spark is an existing SparkSession
    data = [Row(
        '913294058	20190320	201903	2019	2019.2192	ESP	SPAIN	ESP								AUT	AUSTRIAN	AUT								1	010	010	01	1	0.0	7	1	7	0.8130081300813	4	Barcelona, Comunidad Autonoma de Cataluna, Spain	SP	SP56	25806	41.3833	2.18333	-372490	4	Barcelona, Comunidad Autonoma de Cataluna, Spain	SP	SP56	25806	41.3833	2.18333	-372490	4	Barcelona, Comunidad Autonoma de Cataluna, Spain	SP	SP56	25806	41.3833	2.18333	-372490	20200319064500	https://www.managingmadrid.com/2020/3/19/21186249/report-real-madrid-and-barcelona-are-interested-in-signing-david-alaba'),
        Row(
            '913294059	20200218	202002	2020	2020.1315	BUS	INDUSTRY						BUS			AUS	AUSTRALIAN	AUS								1	010	010	01	1	0.0	10	1	10	-2.33812949640287	4	Sydney, New South Wales, Australia	AS	AS02	154637	-33.8833	151.217	-1603135	4	Sydney, New South Wales, Australia	AS	AS02	154637	-33.8833	151.217	-1603135	4	Sydney, New South Wales, Australia	AS	AS02	154637	-33.8833	151.217	-1603135	20200319064500	https://www.stuff.co.nz/national/health/coronavirus/120426027/coronavirus-australia-follows-new-zealand-in-closing-border-to-nonresidents'),
        Row(
            '913294060	20200218	202002	2020	2020.1315	BUS	INDUSTRY						BUS			AUS	AUSTRALIAN	AUS								1	160	160	16	4	-4.0	10	1	10	-2.33812949640287	4	Sydney, New South Wales, Australia	AS	AS02	154637	-33.8833	151.217	-1603135	4	Sydney, New South Wales, Australia	AS	AS02	154637	-33.8833	151.217	-1603135	4	Sydney, New South Wales, Australia	AS	AS02	154637	-33.8833	151.217	-1603135	20200319064500	https://www.stuff.co.nz/national/health/coronavirus/120426027/coronavirus-australia-follows-new-zealand-in-closing-border-to-nonresidents')]
    df = spark.createDataFrame(data, schema=["value"])

    # data = ["Michael, 29", "Andy, 30", "Justin, 19"]
    # lines = spark.sparkContext.parallelize(data)
    # parts = lines.map(lambda l: l.split(","))

    # spark is an existing SparkSession
    # data = [(None, "Michael"), (30, "Andy"), (19, "Justin")]
    # df = spark.createDataFrame(data, schema=["age", "name"])

    # editDf = df.withColumn("value", F.split("value", "\t"))
    editDf = df.withColumn("export", F.split("value", "\t")) \
        .select(F.col("export"))

    editDf.show()

    editDf.printSchema()
