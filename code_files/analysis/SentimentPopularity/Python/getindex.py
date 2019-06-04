# -*- coding: utf-8 -*-
"""
Created on Sun May 26 09:59:52 2019

@author: lliu9
"""

from mrjob.job import MRJob
import csv


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
      line = csv.reader([line], quotechar='|').__next__()

            
      try:
          #locate 'questions'
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