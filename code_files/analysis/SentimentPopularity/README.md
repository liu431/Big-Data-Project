
Find the average sentiment and viewcounts of accepted answers associated with questions with top tags

# toptags calculated from decrs_toptags
toptags = ['javascript', 'java','c#', 'php', 'android', 'python', 'jquery', 'html', 'c++', 'ios', 'css', 'mysql', 
           'sql', 'asp.net', 'ruby-on-rails']
           
           
Example: "python"

Step0:
To solve the newline issue in Unix: dos2unix CSV_Files_Posts.csv

Step1:

Command: python getindex.py <CSV_Files_Posts_sample.csv> index.txt

Input: CSV_Files_Posts_sample.csv (should be in the same folder with getindex.py)

Output: key: acceptedanswerid, value: viewcount

File: index.txt


Step2:

Command: python sentiment.py <CSV_Files_Posts_sample.csv> results.txt

Input: CSV_Files_Posts_sample.csv and index.txt (should be in the same folder with sentiment.py)

Output: key: date, value: average sentiment and viewcount

File: results.txt


Step3: TimeSeriesPlot.ipynb
Functions: time series plotting and statistical analysis

Output: Sentiment and Popularity for Python.png
