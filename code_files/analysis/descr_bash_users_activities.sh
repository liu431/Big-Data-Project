#!/bin/bash

gcloud dataproc clusters create sparktest \
    --project=capp3-240914  \
    --zone=us-central1-a \
    --single-node

gsutil cp gs://pub/shakespeare/rose.txt \
    gs://capp3-nikki/rose.txt


gcloud dataproc jobs submit pyspark word-count.py \
    --cluster=sparktest \
    -- gs://capp3-nikki/rose.txt gs://capp3-nikki/output/

gsutil cat gs://capp3-nikki/output/*


# Test Spark 1
gcloud dataproc jobs submit pyspark users_activities.py \
    --cluster=sparktest \
    -- gs://capp-3-stackoverflow/CSV_Files/Posts_sample.csv gs://capp3-nikki/output/

gsutil cat gs://capp3-nikki/output/* > test_log.txt

gcloud dataproc clusters create sparktest2 \
    --project=capp3-240914  \
    --zone=us-central1-a \

gcloud dataproc clusters update sparktest2 \
    --num-workers 3

gcloud dataproc jobs submit pyspark users_activities.py \
    --cluster=sparktest \
    -- gs://capp-3-stackoverflow/CSV_Files/Posts.csv gs://capp3-nikki/real_output/

gsutil cat gs://capp3-nikki/real_output/* > test_log.txt

gsutil cp users_activities \
    gs://capp3-nikki/users_activities.txt

