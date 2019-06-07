# Code Files
This folder contains all scripts and code used throughout the project.

## Table of Contents
- **[Analysis](analysis):** *Code used for the final Big Data analysis*
    1. **[Sentiment Popularity](analysis/SentimentPopularity):**
        - **[Python](analysis/SentimentPopularity/Python)**
        - **[SQL](analysis/SentimentPopularity/SQL)**
        - **[Javascript](analysis/SentimentPopularity/Javascript)**
        - **[Java](analysis/SentimentPopularity/Java)**
        - **[Git](analysis/SentimentPopularity/Git)**
        - **[C](analysis/SentimentPopularity/C)**
        - **[Visualization](analysis/SentimentPopularity/README.md)**
        - **[VADER sentiment analysis.ipynb](analysis/SentimentPopularity/VADER%20sentiment%20analysis.ipynb)**
        - **[adam_text_sentiment_test.py](analysis/adam_text_sentiment_test.py)**
     
    2. **Descriptive Analysis**  
        - **Exploring languages & frameworks:** Top tags
            - **[decrs_toptags.py](analysis/decrs_toptags.py)**
        - **Exploring Users:** Distribution of user activities (questions and answers)
            - **[decrs_users_activities.py](analysis/decrs_users_activities.py)** *MapReduce version*
            - **[decrs_spark_users_activities.py](analysis/decrs_spark_users_activities.py)** *Apache Spark version*
            - **[decrs_bash_users_activities.sh](analysis/decrs_bash_users_activities.sh)** *Accompanied Bash script for launching Spark cluster*
        - **Exploring Questions:** Questions that receive most number of answers 2008 to 2019
            - **[decrs_max_ans_q.py](analysis/decrs_max_ans_q.py)**
        - **Exploring Answer Providers:** Locations of users who receive ["Illuminator" badge](https://stackoverflow.com/help/badges)
            - **[decrs_users_gold_bash.sh](analysis/decrs_users_gold_bash.sh)** *Bash script for data prep before running the below code*
            - **[decrs_users_gold_ans.py](analysis/decrs_users_gold_ans.py)** *GeoPy version*<sup>1</sup>
            - **[decrs_gmap_users_gold_ans.py](analysis/decrs_gmap_users_gold_ans.py)** *Google Maps version*<sup>1</sup>
            - **[mrjob.conf](analysis/mrjob.conf)** *MRJob Dataproc configuration file*
        - **Exploring Tag Network:** Bi-grams of adjacent tags
            - **[decrs_bi_grams_tags.py](analysis/decrs_bi_grams_tags.py)**<sup>2</sup>
            - **[decrs_n_grams_tags.py](analysis/decrs_n_grams_tags.py)**<sup>2</sup>

- **[Processing](processing):** *Code used to prepare raw XML data-sets for the analysis*
    - **[First Drafts](processing/first_drafts):** *Several first drafts of processing code, each completed by a different person*
        - **[adam_process_data.py](processing/first_drafts/adam_process_data.py):**
        - **[dhruval_process_data.py](processing/first_drafts/dhruval_process_data.py):**
        - **[nikki_process_users_votes.py](processing/first_drafts/nikki_process_users_votes.py):**
    - **[cleaning_MPI.py](processing/cleaning_MPI.py):** *Final processing code using MPI*
    - **[main_process_data.py](processing/main_process_data.py):** *Final processing code (not parallelized)*
    - **[main_process_data_no_hardcoded.py](processing/main_process_data_no_hardcoded.py):** *Final processing code (not parallelized)*

<sup>1</sup> Note: The two versions of the code below are almost identical. The main difference is the package used for Geocoding.
<sup>2</sup> Note: Different bi-gram generating methods
