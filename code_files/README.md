# Code Files
This folder contains all scripts and code used throughout the project.

## Table of Contents
- **[Analysis](analysis):** *Code used for the final Big Data analysis*
    - **[Sentiment Popularity](analysis/SentimentPopularity):** *The meat and potatoes - all the code for the sentiment analysis by language*
        - **[Python](analysis/SentimentPopularity/Python)**
        - **[SQL](analysis/SentimentPopularity/SQL)**
        - **[Javascript](analysis/SentimentPopularity/Javascript)**
        - **[Java](analysis/SentimentPopularity/Java)**
        - **[Git](analysis/SentimentPopularity/Git)**
        - **[C](analysis/SentimentPopularity/C)**
        - **[Visualization](analysis/SentimentPopularity/README.md)**
        - **[VADER sentiment analysis.ipynb](analysis/SentimentPopularity/VADER%20sentiment%20analysis.ipynb):** *Visualization code for the sentiment analysis*
        - **[adam_text_sentiment_test.py](analysis/SentimentPopularity/adam_text_sentiment_test.py):** *Alternative sentiment analysis code that was tested*
    - **[Descriptive Analysis](analysis/descriptive)**  
        - **Exploring languages & frameworks:** *Top tags*
            - **[descr_toptags.py](analysis/descriptive/descr_toptags.py)**
            - **[descr_toptag.py](analysis/descriptive/descr_toptag.py)** *Alternative version*
        - **Exploring Users:** *Distribution of user activities (questions and answers)*
            - **[descr_users_activities.py](analysis/descriptive/descr_users_activities.py)** *MapReduce version*
            - **[descr_spark_users_activities.py](analysis/descriptive/descr_spark_users_activities.py)** *Apache Spark version*
            - **[descr_bash_users_activities.sh](analysis/descriptive/descr_bash_users_activities.sh)** *Accompanied Bash script for launching Spark cluster*
        - **Exploring Questions:** *Questions that receive most number of answers 2008 to 2019*
            - **[descr_max_ans_q.py](analysis/descriptive/descr_max_ans_q.py)**
        - **Exploring Answer Providers:** *Locations of users who receive ["Illuminator" badge](https://stackoverflow.com/help/badges)*
            - **[descr_users_gold_bash.sh](analysis/descriptive/descr_users_gold_bash.sh)** *Bash script for data prep before running the below code*
            - **[descr_users_gold_ans.py](analysis/descriptive/descr_users_gold_ans.py)** *GeoPy version*<sup>1</sup>
            - **[descr_gmap_users_gold_ans.py](analysis/descriptive/descr_gmap_users_gold_ans.py)** *Google Maps version*<sup>1</sup>
            - **[descr_optimized_users_locations.py](analysis/descriptive/descr_optimized_users_locations.py)** *Improved version*
            - **[mrjob.conf](analysis/descriptive/mrjob.conf)** *MRJob Dataproc configuration file*
        - **Exploring Tag Network:** *Bi-grams of adjacent tags*
            - **[decrs_bi_grams_tags.py](analysis/descriptive/descr_bi_grams_tags.py)**<sup>2</sup>
            - **[decrs_n_grams_tags.py](analysis/descriptive/descr_n_grams_tags.py)**<sup>2</sup>

- **[Processing](processing):** *Code used to prepare raw XML data-sets for the analysis*
    - **[First Drafts](processing/first_drafts):** *Several first drafts of processing code, each completed by a different person*
        - **[adam_process_data.py](processing/first_drafts/adam_process_data.py):**
        - **[dhruval_process_data.py](processing/first_drafts/dhruval_process_data.py):**
        - **[nikki_process_users_votes.py](processing/first_drafts/nikki_process_users_votes.py):**
    - **[cleaning_MPI.py](processing/cleaning_MPI.py):** *Final processing code using MPI*
    - **[main_process_data.py](processing/main_process_data.py):** *Final processing code (not parallelized)*
    - **[main_process_data_no_hardcoded.py](processing/main_process_data_no_hardcoded.py):** *Final processing code (not parallelized)*
    - **[output_to_csv.py](processing/output_to_csv.py):** *MPI script to convert text files from analysis to CSVs*

- **[Visualizations](visualizations):** *Code used to create all the MPI descriptive statistics visualizations*
    - **[visualizations_files](visualizations/visualizations_files):** *Contains raw SVG files for all figures (see the [main visualizations folder](../visualizations) for rasterized visualizations and their descriptions*
    - **[visualizations.md](visualizations/visualizations.md):** *Markdown document displaying visualizations and their code*
    - **[visualizations.Rmd](visualizations/visualizations.Rmd):** *R Markdown document displaying visualizations and their full code*

<sup>1</sup> Note: The two versions of the code below are almost identical. The main difference is the package used for Geocoding.
    
<sup>2</sup> Note: Different bi-gram generating methods
