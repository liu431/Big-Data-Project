#!/bin/bash
#
# This script launches Google Cloud Dataproc cluster
# And submit a Spark job
# Main author: Sanittawan (Nikki)

# Note: Nikki ran out of her credits. The output in the
# bucket is not accessible unfortunately. But a copy is
# saved to the output directory on the repository.

# Testing on a small subset
gcloud dataproc clusters create sparktest \
    --project=capp3-240914  \
    --zone=us-central1-a \
    --single-node

gcloud dataproc jobs submit pyspark users_activities.py \
    --cluster=sparktest \
    -- gs://capp-3-stackoverflow/CSV_Files/Posts_sample.csv gs://capp3-nikki/output/

gsutil cat gs://capp3-nikki/output/* > test_log.txt

# Submitting a real job
gcloud dataproc clusters create sparktest2 \
    --project=capp3-240914  \
    --zone=us-central1-a \

gcloud dataproc clusters update sparktest2 \
    --num-workers 3

gcloud dataproc jobs submit pyspark users_activities.py \
    --cluster=sparktest2 \
    -- gs://capp-3-stackoverflow/CSV_Files/Posts.csv gs://capp3-nikki/real_output/

gsutil cat gs://capp3-nikki/real_output/* > test_log.txt

gsutil cp users_activities \
    gs://capp3-nikki/users_activities.txt
