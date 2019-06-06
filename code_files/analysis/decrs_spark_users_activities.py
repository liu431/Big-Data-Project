'''
CMSC 12300 / CAPP 30123
Project: Descriptive analysis Task 2

'''
from pyspark.sql import SparkSession
import sys

if len(sys.argv) != 3:
  raise Exception("Exactly 2 arguments are required: <inputUri> <outputUri>")

inputUri=sys.argv[1]
outputUri=sys.argv[2]

# index = 8 = owneruserID

#sc = pyspark.SparkContext()
spark = SparkSession.builder.appName('users').getOrCreate()
df = spark.read.csv(sys.argv[1], header="true")
#distinct_users = df.select("OwnerUserId").distinct().count()
#print(distinct_users)

users = df.select("OwnerUserId").rdd.map(lambda x: (x, 1))
users_counts = users.reduceByKey(lambda count1, count2: count1 + count2)    
users_counts.saveAsTextFile(sys.argv[2])
#distinct_users.saveAsTextFile(sys.argv[2])