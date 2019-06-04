# -*- coding: utf-8 -*-
"""
Created on Sun May 26 09:20:51 2019

@author: lliu9
"""


from mrjob.job import MRJob

class MRTopTags(MRJob):
  
  def mapper(self, _, line):
      cells=line.split(",")
      if cells[2] != "Count":
          word = cells[1]
          count = int(cells[2])
          
          yield word, count

  def combiner(self, word, count):
      yield word, sum(count)
        
  def reducer_init(self):
      self.dict = {}
  
  def reducer(self, word, count):
      self.dict[word]=sum(count)


  def reducer_final(self):
      dictlist=sorted(self.dict.items(), reverse=True, 
                            key = lambda kv: kv[1])
      for i in range(5):
          yield  dictlist[i][0], dictlist[i][1]
 
      

if __name__ == '__main__':
  MRTopTags.run()