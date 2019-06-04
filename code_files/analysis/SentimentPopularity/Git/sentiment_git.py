# -*- coding: utf-8 -*-
"""
Created on Sun May 26 12:53:12 2019

@author: lliu9
"""

from mrjob.job import MRJob
import csv
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#read in the selected indices
anskey={}
with open("index_git.txt") as f:
    for line in f:
        pair = line.split("\t")    
        try:
            anskey[pair[0][1:-1]] = float(pair[1][2:-3])
        except ValueError:
            pass
        
       
def sentiment_analyzer_scores(sentence):
    '''
    function takes in a string input
    returns the normalized sentiment score
    '''
    
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(sentence)
    
    return score["compound"]

class MRScore(MRJob):
  '''
  input: output from the filter.py file
  '''
  
  def mapper(self, _, line):
      '''
      key: month (could be modfied to day or year)
      value: tuple of sentiment score and viewcount of the question
      '''
      
      line = csv.reader([line]).__next__()
      try:
          if line[1] =='2':
              ID = line[0] 
              body = line[7]
              tt = line[4]
              try:
                  mon = tt[:7]
                  if ID in anskey :
                      senti = sentiment_analyzer_scores(body)
                      viewc = anskey[ID]
                      yield mon, (senti, viewc)
                       
              except ValueError:
                  pass
                   
      except IndexError:
          pass

      
  def reducer(self, mon, scores):
      '''
      key: month
      value: [0,(1,2)]
            0: average of the sentimenviewcount
            1: average of the viewcount
            2: counts of elements assciated with the key
      '''
      
      res = np.array(list(scores))
      listlen = len(res)
      res.reshape(listlen, 2)
      resm = np.mean(res, axis=0)
    
      yield mon, [resm[0], (resm[1], listlen)]

if __name__ == '__main__':
     MRScore.run()