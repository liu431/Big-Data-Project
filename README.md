# Big Data Analysis of the Developer Community 
*This project investigates the changing sentiments of posters on StackOverflow.*

## Project Information

**Class:** CAPP 30123 (Computer Science with Applications III) @ UChicago

**Group name:** HackyStacks

**Group members:** Adam Shelton, Dhruval Bhatt, Li Liu, Sanittawan Tan

**Data sets:** Stack Overflow Data

## Quick Links
- **[Project Proposal](refs_docs/CAPP3_project_proposal.pdf)**
- **[Presentation Slides](https://docs.google.com/presentation/d/1GYTZUKXJao9cUAPSVXusdpyFvTQQRsTqmrr1fUi9puU/edit?usp=sharing)**

## Table of Contents
- **[Code Files](code_files):** *Contains all scripts and code used throughout the project*
    - **[Analysis](code_files/analysis):** *Code used for the final Big Data analysis*
        - **[Sentiment Popularity](code_files/analysis/analysis/SentimentPopularity):**
            - **[Python](code_files/analysis/analysis/SentimentPopularity/Python)**
            - **[SQL](code_files/analysis/analysis/SentimentPopularity/SQL)**
            - **[Javascript](code_files/analysis/analysis/SentimentPopularity/Javascript)**
            - **[Java](code_files/analysis/analysis/SentimentPopularity/Java)**
            - **[Git](code_files/analysis/analysis/SentimentPopularity/Git)**
            - **[C](code_files/analysis/analysis/SentimentPopularity/C)**
            - **[Visualization](code_files/analysis/analysis/SentimentPopularity/README.md)**
            - **[VADER sentiment analysis.ipynb](code_files/analysis/analysis/SentimentPopularity/VADER%20sentiment%20analysis.ipynb)**
            - **[adam_text_sentiment_test.py](code_files/analysis/analysis/SentimentPopularity/adam_text_sentiment_test.py):** *Alternative sentiment anlaysis code that was tested*
        - **Descriptive Analysis**  
            - **Exploring languages & frameworks:** Top tags
                - **[descr_toptags.py](code_files/analysis/descr_toptags.py)**
                - **[descr_toptag.py](code_files/analysis/descr_toptag.py)** *Alternative version*
            - **Exploring Users:** Distribution of user activities (questions and answers)
                - **[descr_users_activities.py](code_files/analysis/descr_users_activities.py)** *MapReduce version*
                - **[descr_spark_users_activities.py](code_files/analysis/descr_spark_users_activities.py)** *Apache Spark version*
                - **[descr_bash_users_activities.sh](code_files/analysis/descr_bash_users_activities.sh)** *Accompanied Bash script for launching Spark cluster*
            - **Exploring Questions:** Questions that receive most number of answers 2008 to 2019
                - **[descr_max_ans_q.py](code_files/analysis/descr_max_ans_q.py)**
            - **Exploring Answer Providers:** Locations of users who receive ["Illuminator" badge](https://stackoverflow.com/help/badges)
                - **[descr_users_gold_bash.sh](code_files/analysis/descr_users_gold_bash.sh)** *Bash script for data prep before running the below code*
                - **[descr_users_gold_ans.py](code_files/analysis/descr_users_gold_ans.py)** *GeoPy version*<sup>1</sup>
                - **[descr_gmap_users_gold_ans.py](code_files/analysis/descr_gmap_users_gold_ans.py)** *Google Maps version*<sup>1</sup>
                - **[descr_optimized_users_locations.py](code_files/analysis/descr_optimized_users_locations.py)** *Improved version*
                - **[mrjob.conf](code_files/analysis/mrjob.conf)** *MRJob Dataproc configuration file*
            - **Exploring Tag Network:** Bi-grams of adjacent tags
                - **[decrs_bi_grams_tags.py](code_files/analysis/descr_bi_grams_tags.py)**<sup>2</sup>
                - **[decrs_n_grams_tags.py](code_files/analysis/descr_n_grams_tags.py)**<sup>2</sup>
    - **[Processing](code_files/processing):** *Code used to prepare raw XML data-sets for the analysis*
        - **[First Drafts](code_files/processing/first_drafts):** *Several first drafts of processing code, each completed by a different person*
            - **[adam_process_data.py](code_files/processing/first_drafts/adam_process_data.py):**
            - **[dhruval_process_data.py](code_files/processing/first_drafts/dhruval_process_data.py):**
            - **[nikki_process_users_votes.py](code_files/processing/first_drafts/nikki_process_users_votes.py):**
        - **[cleaning_MPI.py](code_files/processing/cleaning_MPI.py):** *Final processing code using MPI*
        - **[main_process_data.py](code_files/processing/main_process_data.py):** *Final processing code (not parallelized)*
        - **[main_process_data_no_hardcoded.py](code_files/processing/main_process_data_no_hardcoded.py):** *Final processing code (not parallelized)*
        - **[output_to_csv.py](code_files/processing/output_to_csv.py):** *MPI script to convert text files from analysis to CSVs*
    - **[Visualizations](code_files/visualizations):** *Code used to create all the MPI descriptive statistics visualizations*
        - **[visualizations_files](code_files/visualizations/visualizations_files):** *Contains raw SVG files for all figures (see the [main visualizations folder](../visualizations) for rasterized visualizations and their descriptions*
        - **[visualizations.md](code_files/visualizations/visualizations.md):** *Markdown document displaying visualizations and their code*
        - **[visualizations.Rmd](code_files/visualizations/visualizations.Rmd):** *R Markdown document displaying visualizations and their full code*
- **[Data](data):** *Contains all data files small enough to upload to GitHub*
    - **[Samples](data/samples):** *Small subsets of data files used for testing*
        - **[sample_badges.csv](data/samples/sample_badges.csv):** *500 lines of Badges.xml converted to CSV*
        - **[sample_comments.csv](data/samples/sample_comments.csv):** *500 lines of Comments.xml converted to CSV*
        - **[sample_PostHistory.csv](data/samples/sample_PostHistory.csv):** *500 lines of PostHistory.xml converted to CSV*
        - **[sample_PostLinks.csv](data/samples/sample_PostLinks.csv):** *500 lines of PostLinks.xml converted to CSV*
        - **[sample_posts.csv](data/samples/sample_posts.csv):** *500 lines of Posts.xml converted to CSV*
        - **[sample_tags.csv](data/samples/sample_tags.csv):** *500 lines of Tags.xml converted to CSV*
        - **[sample_users.csv](data/samples/sample_users.csv):** *500 lines of Users.xml converted to CSV*
        - **[sample_votes.csv](data/samples/sample_votes.csv):** *500 lines of Votes.xml converted to CSV*
- **[Meeting Minutes](minutes):** *Contains resources from weekly minutes*
     - **Whiteboard Pictures:** _Photos of drawings/diagrams from meetings_
        - **[Week 4](minutes/4_whiteboard.jpg)**
        - **[Week 6](minutes/6_whiteboard.jpg)**
        - **[Week 7](minutes/May17_whiteboard.jpg)**
        - **[Week 8](minutes/8_Whiteboard.jpg)**
    - **Notes**
        - **[Week 4](minutes/MeetingNotes_Apr26.pdf)**
- **[Output Data](output_data):**  *Contains the results from the Big Data analysis*
    - **[raw_text_files](output_data/raw_text_files):** *Contains unprocessed text files straight from the analysis scripts*
        - **[top_questions.txt](output_data/raw_text_files/top_questions.txt):** *Most popular questions by year*
        - **[top_tags.txt](output_data/raw_text_files/top_tags.txt):** *Tags by number of posts*
        - **[twograms.txt](output_data/raw_text_files/twograms.txt):** *All two-grams of tags in posts*
        - **[users_gold_badge_locations.txt](output_data/raw_text_files/users_gold_badge_locations.txt):** *The location of each user with gold*
    - **[mpi_trials.csv](output_data/mpi_trials.csv):** *Running times of different MPI configurations*
    - **[top_questions.csv](output_data/top_questions.csv):** *Most popular questions by year*
    - **[top_tags.csv](output_data/top_tags.csv):** *Tags by number of posts*
    - **[twograms.csv](output_data/twograms.csv):** *All two-grams of tags in posts*
    - **[user_ac_out](output_data/user_ac_out.csv):** *The number of posts per user*
    - **[users_gold_badge_locations.csv](output_data/users_gold_badge_locations.csv):** *The location of each user with gold*
- **[Reference Materials and Documents](refs_docs)**
    - **[Project Proposal](refs_docs/CAPP3_project_proposal.pdf)**
    - **[Server Access Guide](refs_docs/server_access.md):** *Provides instructions on how to access and use the server*
- **[Visualizations](visualizations)**: *Contains all rasterized PNGs of the visualizations*
    - **[mpi-1-1.png](visualizations/mpi-1-1.png):** *Line plot of how MPI running time decreases as more nodes are added*
    - **[mpi-2-1.png](visualizations/mpi-2-1.png):** *Bar plot of the relationship between number of hosts and running time*
    - **[mpi-cost-1.png](visualizations/mpi-cost-1.png):** *Line plot of how Google Cloud costs increase as more nodes are added*
    - **[ques-year-1.png](visualizations/ques-year-1.png):** *Bar plot of top questions for each year*
    - **[top-tags-1-png](visualizations/top-tags-1.png):** *Bar plot of the top six tags in all posts*
    - **[two-grams-1.png](visualizations/two-grams-1.png):** *Network graph of the top 150 tags*
    - **[user-act-1.png](visualizations/user-act-1.png):** *Density plot of user activity*
    - **[usr-act-tmap-1.png](visualizations/usr-act-tmap-1.png):** *Treemap of user activity*   
- **[Zenhub Workflow](zenhub_workflow)**

