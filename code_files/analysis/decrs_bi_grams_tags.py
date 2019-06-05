'''
CMSC 12300 / CAPP 30123
Project: Descriptive analysis Task 2

'''
import string
import re
import csv
from mrjob.job import MRJob

class GetbiGramsTags(MRJob):
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
            tag_list = re.findall(r"[^><]+", tags)
            sliced_tag_list = tag_list[1:]

            for pair in zip(tag_list, sliced_tag_list):
                sorted_pair = sorted(pair)
                yield sorted_pair, 1

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
    GetbiGramsTags.run()
