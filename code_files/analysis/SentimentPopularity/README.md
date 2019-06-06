## Changes of sentiments and popularity of programming languages

### Results & Visualization

<details>
<summary>Python</summary>
<br>
           
![alt text](https://github.com/liu431/Big-Data-Project/blob/master/code_files/analysis/SentimentPopularity/Python/python.png)
</details>

<details>
<summary>SQL</summary>
<br>
           
![alt text](https://github.com/liu431/Big-Data-Project/blob/master/code_files/analysis/SentimentPopularity/SQL/sql.png)
</details>

<details>
<summary>Javascript</summary>
<br>
           
![alt text](https://github.com/liu431/Big-Data-Project/blob/master/code_files/analysis/SentimentPopularity/Javascript/javascript.png)
</details>



#### Top programming languages
<details>
<summary>toptags calculated from decrs_toptags</summary>
<br>
           
```
['javascript', 'java','c#', 'php', 'android', 'python', 'jquery', 'html', 'c++', 'ios', 'css', 'mysql', 
    'sql', 'asp.net', 'ruby-on-rails']
```
</details>

      
      
### Implementation         
##### Example: "python"


<details>
<summary>Step 0: Data preparation</summary>
<br>
To solve the newline issue in Unix: 
           
```dos2unix CSV_Files_Posts.csv```
</details>
           
           
<details>
<summary>Step 1: Get index</summary>
<br>
Command: 
           
```python getindex.py <CSV_Files_Posts_sample.csv> index.txt```

Input: CSV_Files_Posts_sample.csv (should be in the same folder with getindex.py)

Output: (key, value) = (acceptedanswerid, viewcount)

File: index.txt

</details>


<details>
<summary>Step 2: Sentiment and Popularity</summary>
<br>
           
Command: 

```python sentiment.py <CSV_Files_Posts_sample.csv> results.txt```

Input: CSV_Files_Posts_sample.csv and index.txt (should be in the same folder with sentiment.py)

Output: (key, value): (date,  (average sentiment, viewcount, accepted answers))

File: results.txt

</details>

<details>
<summary>Step 3: Time Series Plot</summary>
<br>

Functions: time series plotting and statistical analysis

File: TimeSeriesPlot.ipynb

Input: results.txt

Output: Python.png
</details>
           

