# -*- coding: utf-8 -*-
"""
Created on Sun May 26 12:53:12 2019

@author: lliu9
"""

from mrjob.job import MRJob
import csv
import datetime
import numpy as np

#from datetime import date

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

anskey={}
with open("out.txt") as f:
    for line in f:
        pair = line.split("\t")      
        anskey[pair[0][1:-1]] = int(pair[1][2:-3])
        
        
def sentiment_analyzer_scores(sentence):
    '''
    function takes in a string input
    returns the normalized sentiment score
    '''
    score = analyser.polarity_scores(sentence)
    return score["compound"]

class MRScore(MRJob):
  '''
  input: output from the filter.py file
  '''
  
  def mapper(self, _, line):

      line = csv.reader([line]).__next__()
      try:
          if line[1] =='2':
              ID = line[0] 
              body = line[7]
              #tt = line[4].split("-")
              tt = line[4]
              try:
                  #date = datetime.date(int(tt[0]),int(tt[1]),int(tt[2].split("T")[0]))
                  day = tt[:10]
                  if ID in anskey :
                      senti = sentiment_analyzer_scores(body)
                      viewc = anskey[ID]
                      yield day, (senti, viewc)
                       
              except ValueError:
                  pass
                   
      except IndexError:
          pass

      
  def reducer(self, day, scores):
      
      res = np.array(list(scores))
      listlen = len(res)
      res.reshape(listlen, 2)
      resm = np.mean(res, axis=0)
    
      yield day, (resm[0], resm[1])

if __name__ == '__main__':
  MRScore.run()