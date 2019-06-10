"""
CMSC 12300 / CAPP 30123
Task: Descriptive analysis (Exploring Users)

Main author: Sanittawan (Nikki)

Note: This snippet of code seems to run just fine without
    the main function, so I do not intend to make changes to it

Objective: To find the total number of questions and answers
    posted by a unique user ID in the data set
"""
import sys

from pyspark.sql import SparkSession

# Reference: Error catcher copied from https://cloud.google.com/
# dataproc/docs/tutorials/gcs-connector-spark-tutorial
if len(sys.argv) != 3:
  raise Exception("Exactly 2 arguments are required: <inputUri> <outputUri>")

inputUri=sys.argv[1]
outputUri=sys.argv[2]

# The code below refers to the Spark 2.4.3 documentation
# and https://www.analyticsvidhya.com/blog/2016/10/
# spark-dataframe-and-operations/
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
