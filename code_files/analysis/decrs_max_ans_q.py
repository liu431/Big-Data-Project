"""
CMSC 12300 / CAPP 30123
Project: Descriptive analysis Task 2

Sanittawan Tan
"""
import string
import csv
from mrjob.job import MRJob
import re

class GetMaxAnsQuest(MRJob):
    """
    docsring here
    """
    def mapper(self, _, line):
        """
        :param _:
        :param line:
        :return:
        """
        row = csv.reader([line]).__next__()

        try:
            post_type = int(row[1])
            if post_type == 1:
                create_date = row[4]
                search = re.search(r"\d{4}", create_date)
                if search:
                    year = search.group()
                    title = row[13]
                    answer_counts = row[15]
                    yield year, (int(answer_counts), title)

        except (IndexError, ValueError):
            pass


    def combiner(self, year, val):
        """
        :param _:
        :param line:
        :return:
        """
        try:
            max_ans = max(val)
            yield year, max_ans
        except (TypeError, ValueError):
            pass

    def reducer(self, year, val):
        """
        :param _:
        :param line:
        :return:
        """
        try:
            max_ans = max(val)
            yield year, max_ans
        except (TypeError, ValueError):
            pass


if __name__ == '__main__':
    GetMaxAnsQuest.run()
