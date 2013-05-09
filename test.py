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

from pygeocoder import Geocoder
from pygeolib import GeocoderResult
import json


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

MOCK_DATA = """
[
  {
    "address_components": [
      {
        "long_name": "DMV",
        "short_name": "DMV",
        "types": [
          "point_of_interest",
          "establishment"
        ]
      },
      {
        "long_name": "20725",
        "short_name": "20725",
        "types": [
          "street_number"
        ]
      },
      {
        "long_name": "Sherman Way",
        "short_name": "Sherman Way",
        "types": [
          "route"
        ]
      },
      {
        "long_name": "Winnetka",
        "short_name": "Winnetka",
        "types": [
          "neighborhood",
          "political"
        ]
      },
      {
        "long_name": "Los Angeles",
        "short_name": "Los Angeles",
        "types": [
          "locality",
          "political"
        ]
      },
      {
        "long_name": "Los Angeles",
        "short_name": "Los Angeles",
        "types": [
          "administrative_area_level_2",
          "political"
        ]
      },
      {
        "long_name": "California",
        "short_name": "CA",
        "types": [
          "administrative_area_level_1",
          "political"
        ]
      },
      {
        "long_name": "United States",
        "short_name": "US",
        "types": [
          "country",
          "political"
        ]
      },
      {
        "long_name": "91306",
        "short_name": "91306",
        "types": [
          "postal_code"
        ]
      }
    ],
    "formatted_address": "DMV, 20725 Sherman Way, Winnetka, CA 91306, USA",
    "geometry": {
      "location": {
        "lat": 34.20133510,
        "lng": -118.58479930
      },
      "location_type": "APPROXIMATE",
      "viewport": {
        "northeast": {
          "lat": 34.2105630,
          "lng": -118.56879190
        },
        "southwest": {
          "lat": 34.19210620,
          "lng": -118.60080670
        }
      }
    },
    "postcode_localities": [],
    "types": [
      "point_of_interest",
      "establishment"
    ]
  },
  {
    "address_components": [
      {
        "long_name": "Driver's License Office",
        "short_name": "DMV",
        "types": [
          "point_of_interest",
          "establishment"
        ]
      },
      {
        "long_name": "Audubon Village Shopping Center",
        "short_name": "Audubon Village Shopping Center",
        "types": [
          "establishment"
        ]
      },
      {
        "long_name": "2447",
        "short_name": "2447",
        "types": [
          "street_number"
        ]
      },
      {
        "long_name": "North Union Boulevard",
        "short_name": "N Union Blvd",
        "types": [
          "route"
        ]
      },
      {
        "long_name": "East Colorado Springs",
        "short_name": "East Colorado Springs",
        "types": [
          "neighborhood",
          "political"
        ]
      },
      {
        "long_name": "Colorado Springs",
        "short_name": "Colorado Springs",
        "types": [
          "locality",
          "political"
        ]
      },
      {
        "long_name": "El Paso",
        "short_name": "El Paso",
        "types": [
          "administrative_area_level_2",
          "political"
        ]
      },
      {
        "long_name": "Colorado",
        "short_name": "CO",
        "types": [
          "administrative_area_level_1",
          "political"
        ]
      },
      {
        "long_name": "United States",
        "short_name": "US",
        "types": [
          "country",
          "political"
        ]
      },
      {
        "long_name": "80909",
        "short_name": "80909",
        "types": [
          "postal_code"
        ]
      },
      {
        "long_name": "1107",
        "short_name": "1107",
        "types": []
      }
    ],
    "formatted_address": "Driver's License Office, Audubon Village Shopping Center, 2447 North Union Boulevard, Colorado Springs, CO 80909, USA",
    "geometry": {
      "location": {
        "lat": 38.86735470,
        "lng": -104.79270460
      },
      "location_type": "APPROXIMATE",
      "viewport": {
        "northeast": {
          "lat": 38.86870368029150,
          "lng": -104.7913556197085
        },
        "southwest": {
          "lat": 38.86600571970850,
          "lng": -104.7940535802915
        }
      }
    },
    "postcode_localities": [],
    "types": [
      "point_of_interest",
      "establishment"
    ]
  }
]
"""


class Test(unittest.TestCase):
    """
    Unit tests for googlemaps.

    """
    def test_geocoder_results(self):
        """Test GeocoderResult's indexing and iteration access"""
        results = GeocoderResult(json.loads(MOCK_DATA))

        self.assertEqual(results[1].neighborhood, "East Colorado Springs")
        self.assertEqual(results.establishment, "DMV")
        for index, result in enumerate(results):
            if index == 0:
                self.assertEqual(result.neighborhood, "Winnetka")
            elif index == 1:
                self.assertEqual(result.street_number, "2447")
            else:
                self.fail()

    def test_geocode(self):
        """Test pygeocoder geocode() and address_to_latlng()"""

        addr = '1600 amphitheatre mountain view ca'
        g = Geocoder()
        result = g.geocode(addr)

        self.assertEqual(result.country__long_name, 'United States')
        self.assertEqual(result.postal_code, '94043')
        self.assertEqual(result.street_number, '1600')
        self.assertEqual(result.route, 'Amphitheatre Parkway')
        self.assertEqual(result.locality, 'Mountain View')
        self.assertEqual(result.city, 'Mountain View')
        self.assertEqual(result.administrative_area_level_1, 'California')
        self.assertEqual(result.state, 'California')
        self.assertEqual(result.country, 'United States')
        self.assertEqual(result.formatted_address, '1600 Amphitheatre Parkway, Mountain View, CA 94043, USA')
        self.assertEqual(result.valid_address, True)
        lat, lng = result.coordinates
        self.assertAlmostEquals(lat, 37.422177, 3)
        self.assertAlmostEquals(lng, -122.083099, 3)

    def test_reverse_geocode(self):
        """
        Test pygeocoder reverse_geocode() and latlng_to_address()

        """
        lat, lng = 40.714224, -73.961452
        result = Geocoder.reverse_geocode(lat, lng)

        self.assertEqual(result.country__long_name, 'United States')
        self.assertEqual(result.postal_code, '11211')
        self.assertEqual(result.street_number, '285')
        self.assertEqual(result.route, 'Bedford Avenue')
        self.assertEqual(result.sublocality, 'Brooklyn')
        self.assertEqual(result.administrative_area_level_1, 'New York')
        self.assertEqual(result.country, 'United States')
        addr = result.formatted_address
        self.assertEqual(addr, '285 Bedford Avenue, Brooklyn, NY 11211, USA')
        lat2, lng2 = result.coordinates
        self.assertAlmostEquals(lat, lat2, 3)
        self.assertAlmostEquals(lng, lng2, 3)

        self.assertTrue(result.count > 1)
        self.assertEqual(result[1].formatted_address, 'Williamsburg, NY, USA')

        addr2 = Geocoder.latlng_to_address(lat, lng)
        self.assertEqual(addr, addr2)


if __name__ == "__main__":
    unittest.main()
