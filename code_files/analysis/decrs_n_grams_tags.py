'''
CMSC 12300 / CAPP 30123
Project: Descriptive analysis Task 2

'''
import string
import csv
from mrjob.job import MRJob

class GetnGramsTags(MRJob):
    '''
    docsring here
    '''
    def mapper(self, _, line):
        '''
        docstring here
        '''
        row = csv.reader([line]).__next__()

        try:
            tags = row[14]
            tag_list = tags.split("><")
            tag_list[0] = tag_list[0][1:]
            tag_list[-1] = tag_list[-1][:-1]

            for i in range(0, len(tag_list) - 2 + 1):
                sorted_tags = sorted(tag_list[i: i + 2])
                yield sorted_tags, 1

        except IndexError:
            pass


    def combiner(self, tag, counts):
        '''
        docstring here
        '''
        try:
            yield tag, sum(counts)
        except (TypeError, ValueError):
            pass

    def reducer(self, tag, counts):
        '''
        docstring here
        '''
        try:
            yield tag, sum(counts)
        except (TypeError, ValueError):
            pass


if __name__ == '__main__':
    GetnGramsTags.run()
