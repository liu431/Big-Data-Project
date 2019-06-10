'''
CMSC 12300 / CAPP 30123
Project: Descriptive analysis Task 4
'''
import string
import csv
from mrjob.job import MRJob
import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


class FindLocUsersGoldBadges(MRJob):
    '''
    docsring here
    '''
    def mapper(self, _, line):
        '''
        docstring here
        '''
        try:
            row = csv.reader([line]).__next__()
            file = str(row[-1]).strip().lower()

        #try:
            if file == "badges":
                badge_name = str(row[2]).strip().lower()
                badge_name = ''.join([char for char in \
                                      badge_name if char != "'"])
                user_id = str(row[1]).strip().lower()
                user_id = ''.join([char for char in user_id if char != "'"])

                if badge_name == "illuminator":
                    yield user_id, badge_name

            elif file == "users":
                user_id = str(row[0]).strip()
                location = str(row[6]).strip()

                if not location or user_id == "-1":
                    location = None
                else:
                    yield user_id, location

        #except (IndexError, ValueError):
        except:
            pass


    def reducer(self, user_id, vals):
        '''
        docstring here
        '''
        try:
            val_list = set(vals)
            if len(val_list) == 2:
                val_list = list(sorted(val_list))
                yield user_id, val_list
        except (TypeError, ValueError):
            pass


if __name__ == '__main__':
    FindLocUsersGoldBadges.run()