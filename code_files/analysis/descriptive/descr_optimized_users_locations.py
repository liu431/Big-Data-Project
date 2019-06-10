"""
CMSC 12300 / CAPP 30123
Task: Descriptive analysis (Exploring Users)

Main author: Dhruval and Sanittawan (Nikki)
"""

import csv
import string
import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from mrjob.job import MRJob


class FindLocUsersGoldBadges(MRJob):
    """
    A class for finding the location of users with 
    gold badge in answers, called illuminator.
    """
    def mapper_badge_location(self, _, line):
        """
        Maps User ID to badges and  user id to user locations.
        Inputs:
            line: a single line in a CSV file
        Returns: 
            user id: badges or user id and location
            (depending on the file source)
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
                    yield user_id, location

        except (IndexError, ValueError):
            pass

    def reducer_userid(self, user_id, vals):
        """
        Reduces to badges and location for a given userid
        Inputs:
            key: (string) User ID
            vals: (int) tuple of location and/or badge
        Returns: User ID as key and a list of location and badge as value
        """
        try:
            val_list = set(vals)
            if len(val_list) == 2:
                val_list = list(sorted(val_list))
                yield user_id, val_list
        except (TypeError, ValueError):
            pass

    def convert_location(self, user_id, val_list):
        """
        Second step: convert location to coordinates and standard country name
        Inputs:
            key: (string) User ID
            vals: (int) tuple of location and badge
        Returns: User ID as key and a list of location and badge as value
        """
        if val_list[0] == "illuminator":
            location = val_list[1]
            badge = val_list[0]
        else: 
            location = val_list[0]
            badge = val_list[1]

        if not location:
            location = None
            coord = None
        else:
            try:
                geolocator=Nominatim(timeout=3)
                raw_location = geolocator.geocode(location)
            
                if raw_location:
                    coord = (raw_location.latitude,
                             raw_location.longitude)
                    address = geolocator.reverse(
                                            [raw_location.latitude,
                                             raw_location.longitude],
                                             language='en')
                    country = address.address.split()[-1]
                else:
                    country = None
                    coord = None                  
            except:
                pass

            yield user_id, ((coord, country), badge)

    def steps(self):
        """
        Multistep MRJob
        """
        return [
            MRStep(mapper=self.mapper_badge_location,
                   reducer=self.reducer_userid),
            MRStep(mapper=self.convert_location)
        ]


if __name__ == '__main__':
    FindLocUsersGoldBadges.run()
