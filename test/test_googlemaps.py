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
import doctest
    
import pygeocoder
from pygeocoder import Geocoder    


def searchkey(obj, key):
    """Does BFS on JSON-like object `obj` to find a dict with a key == to `key` and 
    returns the associated value.  Returns None if it didn't find `key`."""
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
    """Unit tests for googlemaps."""

    def test_geocode(self):
        """Test googlemaps geocode() and address_to_latlng()"""

        addr = '1600 amphitheatre mountain view ca'
        gmaps = GoogleMaps(GMAPS_API_KEY)
        result = gmaps.geocode(addr)
        self.assertEqual(result['Status']['code'], 200)
        self.assertEqual(searchkey(result, 'CountryName'), 'USA')
        self.assertEqual(searchkey(result, 'PostalCodeNumber'), '94043')
        self.assertEqual(searchkey(result, 'ThoroughfareName'), '1600 Amphitheatre Pkwy')
        self.assertEqual(searchkey(result, 'LocalityName'), 'Mountain View')
        self.assertEqual(searchkey(result, 'AdministrativeAreaName'), 'CA')
        self.assertEqual(searchkey(result, 'CountryNameCode'), 'US')
        self.assertEqual(searchkey(result, 'address'), '1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA')
        lat, lng = searchkey(result, 'coordinates')[1::-1]
        self.assertAlmostEquals(lat,   37.422125, 3)
        self.assertAlmostEquals(lng, -122.084466, 3)

        (lat2, lng2) = gmaps.address_to_latlng(addr)
        self.assertAlmostEqual(lat, lat2, 3)
        self.assertAlmostEqual(lng2, lng2, 3)


    def test_reverse_geocode(self):
        """Test googlemaps reverse_geocode() and latlng_to_address()"""
        
        lat, lng = 40.714224, -73.961452
        gmaps = GoogleMaps(GMAPS_API_KEY)
        result = gmaps.reverse_geocode(lat, lng)
        self.assertEqual(result['Status']['code'], 200)
        result = result['Placemark'][0]
        self.assertEqual(searchkey(result, 'CountryName'), 'USA')
        self.assertEqual(searchkey(result, 'PostalCodeNumber'), '11211')
        self.assertEqual(searchkey(result, 'ThoroughfareName'), '277 Bedford Ave')
        self.assertEqual(searchkey(result, 'LocalityName'), 'Brooklyn')
        self.assertEqual(searchkey(result, 'AdministrativeAreaName'), 'NY')
        self.assertEqual(searchkey(result, 'CountryNameCode'), 'US')
        addr = searchkey(result, 'address')
        self.assertEqual(addr, '277 Bedford Ave, Brooklyn, NY 11211, USA')
        lat2, lng2 = searchkey(result, 'coordinates')[1::-1]
        self.assertAlmostEquals(lat, lat2, 3)
        self.assertAlmostEquals(lng, lng2, 3)
        
        addr2 = gmaps.latlng_to_address(lat, lng)
        self.assertEqual(addr, addr2)

        
if __name__ == "__main__":
    unittest.main()