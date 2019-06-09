"""
CMSC 12300 / CAPP 30123
Task: Descriptive analysis (Exploring Answer Providers)

Main author: Dhruval, Sanittawan (Nikki)
"""
import csv
import googlemaps
import re
from mrjob.job import MRJob

API_KEY = # you need to fill in a Google API Key here #

class FindLocUsersGoldBadges(MRJob):
    """
    docsring here
    """
    def mapper(self, _, line):
        """
        docstring here
        """
        row = csv.reader([line]).__next__()
        file = str(row[-1]).strip().lower()

        try:
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
                    coord = None
                    country = None
                else:
                    gmaps = googlemaps.Client(key=API_KEY)
                    geocode_result = gmaps.geocode(location)
                
                    if geocode_result:
                        lat = geocode_result[0]['geometry']['location']['lat']
                        lng = geocode_result[0]['geometry']['location']['lng']
                        coord = (lat, lng)
                        address = geocode_result[0]['address_components'][-1]
                        country = address['long_name']
                    else:
                        country = None
                        coord = None
                yield user_id, (coord, country)

        except (IndexError, ValueError):
            pass


    def reducer(self, user_id, vals):
        """
        docstring here
        """
        try:
            val_list = list(vals)
            if len(val_list) == 2:
                a = val_list[0]
                b = val_list[1]
                if isinstance(a, list):
                    final = a, b
                else:
                    final = b, a
                yield user_id, final
        except (TypeError, ValueError):
            pass


if __name__ == '__main__':
    FindLocUsersGoldBadges.run()
