from pyspark import SparkContext, SparkConf

# Initializing Spark
conf = SparkConf().setAppName("rdd_programming_guide.py").setMaster("spark://192.168.1.8:7077")
sc = SparkContext(conf=conf)

data = [1, 2, 3, 4, 5]
distData = sc.parallelize(data)