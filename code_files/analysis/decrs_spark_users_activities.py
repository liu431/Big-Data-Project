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

spark = SparkSession.builder.appName('users').getOrCreate()
df = spark.read.csv(sys.argv[1], header="true")

tmt = df.groupby("OwnerUserId").count() \
        .orderBy('count', ascending=False)
pattern = "^\d+[^-:.]"
user_activities = tmt.filter(tmt["OwnerUserId"].rlike(pattern))
user_activities.write \
    .format('csv') \
    .options(delimiter=',') \
    .save(sys.argv[2])

spark.stop()