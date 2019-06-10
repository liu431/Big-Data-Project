"""
CMSC 12300 / CAPP 30123
Task: Descriptive analysis (Exploring Tag Network)

Main author: Sanittawan (Nikki)
"""
import csv
import re

from mrjob.job import MRJob


class GetbiGramsTags(MRJob):
    """
    Class for generating tag bi-grams using
    MapReduce framework
    """
    def mapper(self, _, line):
        """
        Maps generated bi-grams with count

        Inputs:
            line: a single line in a CSV file

        Returns: a sorted bi-grams as key
            and count as value
        """
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
        """
        Combine counts of all unique bi-grams

        Inputs:
            tag: (tuple) of tag bi-gram
            counts: (int) of count

        Returns: a sorted bi-grams as key
            and intermediate sum of counts
        """
        try:
            yield tag, sum(counts)
        except (TypeError, ValueError):
            pass


    def reducer(self, tag, counts):
        """
        Reduce all counts of a unique bi-gram tag

        Inputs:
            tag: (tuple) of tag bi-gram
            counts: (int) of count

        Returns: a sorted bi-grams as key
            and count as value
        """
        try:
            yield tag, sum(counts)
        except (TypeError, ValueError):
            pass


if __name__ == '__main__':
    GetbiGramsTags.run()
