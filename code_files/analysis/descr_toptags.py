# -*- coding: utf-8 -*-
'''
Using MapReduce to find the top count for tags
'''

import heapq
from mrjob.job import MRJob

TOP_K = 15

class MRTopTags(MRJob):

    '''
    MRJob to find the top 10 staff visited.
    key - name - lastname, firstname
    value - number of visits
    '''

    def mapper(self, _, line):
        row = line.split(',')
        if row[2] != 'Count':    
            tag_name = row[1]
            count = int(row[2])

            yield (tag_name, count), None

    def reducer_init(self):
        self.h = []

    def reducer(self, key, _):
        tag = key[0]
        count = key[1]

        if len(self.h) < TOP_K:
            heapq.heappush(self.h, (count, tag))
        else:
            if (count, tag) > self.h[0]:
                spillover = heapq.heapreplace(self.h, (count, tag))

    def reducer_final(self):
        self.h.sort(reverse=True)
        for entry in self.h:
            yield entry

if __name__ == '__main__':
    MRTopTags.run()

