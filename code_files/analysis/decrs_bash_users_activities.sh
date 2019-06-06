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