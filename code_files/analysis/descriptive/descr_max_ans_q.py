"""
CMSC 12300 / CAPP 30123
Task: Descriptive analysis (Exploring Questions)

Main author: Sanittawan (Nikki)
"""
import csv
import re

from mrjob.job import MRJob


class GetMaxAnsQuest(MRJob):
    """
    A class for finding questions with the most
    number of answers per year from 2008 to 2019 using
    a MapReduce framework
    """
    def mapper(self, _, line):
        """
        Maps year to answer counts and title of the question

        Inputs:
            line: a single line in a CSV file

        Returns: a year as key and a tuple of answer counts and
            title
        """
        row = csv.reader([line]).__next__()

        try:
            post_type = int(row[1])
            if post_type == 1:
                create_date = row[4]
                search = re.search(r"20[01][0-9]", create_date)
                if search:
                    year = search.group()
                    title = row[13]
                    answer_counts = row[15]
                    yield year, (int(answer_counts), title)

        except (IndexError, ValueError):
            pass


    def combiner(self, year, val):
        """
        Combine counts of all unique bi-grams

        Inputs:
            year: (string) the year the question was posted
            val: (tuple) of number of answers and title

        Returns: a year and a tuple containing the maximum number of
            answer counts
        """
        try:
            max_ans = max(val)
            yield year, max_ans
        except (TypeError, ValueError):
            pass


    def reducer(self, year, val):
        """
        Reduce all counts of a unique bi-gram tag

        Inputs:
            year: (string) the year the question was posted
            val: (tuple) of number of answers and title

        Returns: a year and a tuple containing the maximum number of
            answer counts
        """
        try:
            max_ans = max(val)
            yield year, max_ans
        except (TypeError, ValueError):
            pass


if __name__ == '__main__':
    GetMaxAnsQuest.run()
