'''
Using MapReduce to find the top count for tags

Main Author: Dhruval Bhatt
'''

import heapq
from mrjob.job import MRJob

TOP_K = 15

class MRTopTags(MRJob):
    """
    MRJob to find the top 15 tags with highest count
    """
    def mapper(self, _, line):
        """
        Maps tag name with total count
        Inputs:
            line: a single line in a CSV file
        Returns: tag name and count as keys and no values
        """
        row = line.split(',')
        if row[2] != 'Count':    
            tag_name = row[1]
            count = int(row[2])

            yield (tag_name, count), None

    def reducer_init(self):
        """
        Initializes Heap Structure
        """
        self.h = []

    def reducer(self, key, _):
        """
        Populates top k tag names based on count
        Inputs:
            key: (tuple) tag name, count
            _: None
        Returns: None
        """
        tag = key[0]
        count = key[1]

        if len(self.h) < TOP_K:
            heapq.heappush(self.h, (count, tag))
        else:
            if (count, tag) > self.h[0]:
                spillover = heapq.heapreplace(self.h, (count, tag))

    def reducer_final(self):
        """
        Yields top k sorted tag name and count
        Inputs: None
        Returns: count, tag name
        """
        self.h.sort(reverse=True)
        for entry in self.h:
            yield entry

if __name__ == '__main__':
    MRTopTags.run()