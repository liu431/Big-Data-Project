# -*- coding: utf-8 -*-
"""
Created on Sun May 26 09:59:52 2019

@author: lliu9
"""

from mrjob.job import MRJob
import csv

# toptags calculated from decrs_toptags
toptags = ['javascript', 'java','c#', 
           'php', 'android', 'python', 'jquery',
           'html', 'c++', 'ios', 'css', 'mysql', 
           'sql', 'asp.net', 'ruby-on-rails']

class MRQnsTags(MRJob):
   """
   get the acceptedanswerid, date viewcount of questions with top tags
   """
  
   def mapper(self, _, line):
      '''
      read in the post file
      filter the tags
      return the key: acceptid; value: counts
      '''
      line = csv.reader([line]).__next__()
      #with open('CSV_Files_Posts.csv') as f:
      #      reader = csv.reader(f)
      #      line = [row for row in reader]
            
      try:
          if line[1] =='1':
              tags = line[14].replace('<','').split('>')
              acceptid = line[3]
              counts = line[6]

              try:
                  if "python" in tags and acceptid != '':
                       yield acceptid, counts
                       
              except ValueError:
                  pass
                   
      except IndexError:
          pass

  
   def reducer(self, index, body):
       '''
       return the key: acceptid; value: counts
       this step doesn't do any aggragation as all acceptid is unique
       '''
       try:
           yield index, body
       
       except (TypeError, ValueError):
           pass

if __name__ == '__main__':
   MRQnsTags.run()