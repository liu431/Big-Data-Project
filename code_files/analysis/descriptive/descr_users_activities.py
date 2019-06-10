"""
CMSC 12300 / CAPP 30123
Task: Descriptive analysis (Exploring Users)

Main author: Sanittawan (Nikki)
"""
import csv

from mrjob.job import MRJob


class GetUsersActivities(MRJob):
    """
    A class for finding the number of questions or answers of
    all unique users in the data set using MapReduce framework
    """
    def mapper(self, _, line):
        """
        Maps User ID to count of a single question and/or answer

        Inputs:
            line: a single line in a CSV file

        Returns: user ID of questions and answers (separately) as key
            and count as value
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
        Combines the number of questions and/or answers a unique user
            has posted

        Inputs:
            key: (string) User ID
            counts: (int) number of questions and/or answers

        Returns: User ID as key and the number of question and answer
            separately
        """
        try:
            yield key, sum(counts)
        except (TypeError, ValueError):
            pass


    def reducer(self, key, counts):
        """
        Reduces the number of questions and/or answers a unique user
            has posted

        Inputs:
            key: (string) User ID
            counts: (int) number of questions and/or answers

        Returns: User ID as key and the number of question and answer
            separately
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