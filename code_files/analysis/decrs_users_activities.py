"""
CMSC 12300 / CAPP 30123
Project: Descriptive analysis Task 2

"""
import string
import csv
from mrjob.job import MRJob


class GetUsersActivities(MRJob):
    """
    Class docstring
    """

    def mapper(self, _, line):
        """
        :param _:
        :param line:
        :return:
        """
        row = csv.reader([line]).__next__()

        try:
            user_id = row[8]
            post_type = row[1]
            if user_id and post_type:
                if post_type == '1':  # indicates a question
                    q_key = '_'.join([str(user_id), 'q'])
                    yield q_key, 1
                elif post_type == '2':  # indicates an answer
                    a_key = '_'.join([str(user_id), 'a'])
                    yield a_key, 1
        except IndexError:
            pass

    def combiner(self, key, counts):
        """
        :param key:
        :param counts:
        :return:
        """
        try:
            yield key, sum(counts)
        except (TypeError, ValueError):
            pass

    def reducer(self, key, counts):
        """
        :param key:
        :param counts:
        :return:
        """
        try:
            user_activity = key.split('_')
            if user_activity[1] == 'q':
                key = user_activity[0] + " " + "# questions asked:"
                yield key, sum(counts)
            elif user_activity[1] == 'a':
                key = user_activity[0] + " " + "# answers given:"
                yield key, sum(counts)
        except (TypeError, ValueError):
            pass


if __name__ == '__main__':
    GetUsersActivities.run()
