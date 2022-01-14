from pyspark import SparkContext, SparkConf

# Initializing Spark
conf = SparkConf().setAppName("rdd_programming_guide.py")
sc = SparkContext(conf=conf)

data = [1, 2, 3, 4, 5]
distData = sc.parallelize(data)