#!/usr/bin/env python
#
# Xiao Yu - Montreal - 2010
# Based on googlemaps by John Kleint
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""
Unit tests for pygeocoder.

"""

import unittest

from pygeocoder import Geocoder, GeocoderResult


def searchkey(obj, key):
    """
    Does BFS on JSON-like object `obj` to find a dict with a key == to `key`
    and returns the associated value.  Returns None if it didn't find `key`.

    """
    queue = [obj]
    while queue:
        item = queue.pop(0)
        if type(item) is list:
            queue.extend(item)
        elif type(item) is dict:
            for k in item:
                if k == key:
                    return item[k]
                else:
                    queue.append(item[k])
    return None


class Test(unittest.TestCase):
    """
    Unit tests for googlemaps.

    """
    def test_geocode(self):
        """Test pygeocoder geocode() and address_to_latlng()"""

        addr = '1600 amphitheatre mountain view ca'
        g = Geocoder()
        result = g.geocode(addr)

        self.assertEqual(result.country__long_name, 'United States')
        self.assertEqual(result.postal_code, '94043')
        self.assertEqual(result.street_number, '1600')
        self.assertEqual(result.route, 'Amphitheatre Pkwy')
        self.assertEqual(result.locality, 'Mountain View')
        self.assertEqual(result.administrative_area_level_1, 'CA')
        self.assertEqual(result.country, 'US')
        self.assertEqual(result.formatted_address, '1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA')
        lat, lng = result.coordinates
        self.assertAlmostEquals(lat, 37.422125, 3)
        self.assertAlmostEquals(lng, -122.085984, 3)

        (lat2, lng2) = g.address_to_latlng(addr)
        self.assertAlmostEqual(lat, lat2, 3)
        self.assertAlmostEqual(lng, lng2, 3)

    def test_reverse_geocode(self):
        """
        Test pygeocoder reverse_geocode() and latlng_to_address()

        """
        lat, lng = 40.714224, -73.961452
        g = Geocoder()
        result = g.reverse_geocode(lat, lng)

        self.assertEqual(result.country__long_name, 'United States')
        self.assertEqual(result.postal_code, '11211')
        self.assertEqual(result.street_number, '279-281')
        self.assertEqual(result.route, 'Bedford Ave')
        self.assertEqual(result.sublocality, 'Brooklyn')
        self.assertEqual(result.locality, 'New York')
        self.assertEqual(result.administrative_area_level_1, 'NY')
        self.assertEqual(result.country, 'US')
        addr = result.formatted_address
        self.assertEqual(addr, '279-281 Bedford Ave, Brooklyn, NY 11211, USA')
        lat2, lng2 = result.coordinates
        self.assertAlmostEquals(lat, lat2, 3)
        self.assertAlmostEquals(lng, lng2, 3)

        addr2 = g.latlng_to_address(lat, lng)
        self.assertEqual(addr, addr2)


if __name__ == "__main__":
    unittest.main()
