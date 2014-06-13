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
import requests
import json

from collections import OrderedDict
from pygeocoder import Geocoder
from pygeolib import GeocoderResult, GeocoderError


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
        """Test pygeocoder geocode()"""

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
        self.assertAlmostEqual(lat, 37.4228576, 2)
        self.assertAlmostEqual(lng, -122.0850647, 2)

    def test_geocode_with_components(self):
        """Test pygeocoder geocode()"""

        addr = 'East London'
        components = 'country:ZA'
        g = Geocoder()

        bare_result = g.geocode(addr)
        self.assertEqual(bare_result.city, 'London')
        self.assertEqual(bare_result.country, 'United Kingdom')

        za_result = g.geocode(addr, components=components)
        self.assertEqual(za_result.city, 'East London')
        self.assertEqual(za_result.country, 'South Africa')

    def test_reverse_geocode(self):
        """
        Test pygeocoder reverse_geocode()

        """
        lat, lng = 38.8978378, -77.036545
        result = Geocoder.reverse_geocode(lat, lng)

        self.assertEqual(result.country__short_name, 'US')
        self.assertEqual(result.postal_code, '20500')
        self.assertEqual(result.street_number, '1600')
        self.assertEqual(result.route, 'Pennsylvania Avenue Northwest')
        self.assertEqual(result.administrative_area_level_1, 'District of Columbia')
        self.assertEqual(result.city, 'Washington')
        self.assertEqual(result.state, 'District of Columbia')
        self.assertEqual(result.state__short_name, 'DC')
        self.assertEqual(result.country, 'United States')
        addr = result.formatted_address
        self.assertEqual(addr, "1600 Pennsylvania Avenue Northwest, President's Park, Washington, DC 20500, USA")
        lat2, lng2 = result.coordinates
        self.assertAlmostEqual(lat, lat2, 3)
        self.assertAlmostEqual(lng, lng2, 3)
        self.assertAlmostEqual(lat, result.latitude, 3)
        self.assertAlmostEqual(lng, result.longitude, 3)
        self.assertTrue(result.count > 1)

    def test_simple_auth(self):
        """Test Simple API access. May be flacky is too many people test with the test key"""

        addr = '1600 amphitheatre mountain view ca'
        api_key = 'AIzaSyBUnYj-u24fsbWdftSwbos7XcyQVqiuSao'  # a throwaway test key
        g = Geocoder(api_key=api_key)
        result = g.geocode(addr)

        self.assertEqual(result.state, 'California')
        self.assertEqual(result.country, 'United States')

    def test_business_auth(self):
        """Test Business API access.

        This query fails on purpose, but we inspect and verify the signed URL is correct."""

        # Create the query parameters to sign. The order matters.
        params_to_sign = OrderedDict()
        params_to_sign['address'] = '1600 amphitheatre mountain view ca'
        params_to_sign['components'] = ''
        params_to_sign['bounds'] = ''
        params_to_sign['region'] = ''
        params_to_sign['language'] = ''
        params_to_sign['sensor'] = 'false'

        request_to_sign = requests.Request(
            'GET',
            url=Geocoder.GEOCODE_QUERY_URL,
            params=params_to_sign,
            headers={
                'User-Agent': Geocoder.USER_AGENT
            })
        client_id = 'gme-businessname'
        crypto_key = 'vNIXE0xscrmjlyV-12Nj_BvUPaw='
        g = Geocoder(client_id=client_id, private_key=crypto_key)
        signed_request = g.add_signature(request_to_sign)
        self.assertRegexpMatches(signed_request.url, r'&signature=[a-zA-Z0-9-=]+$', 'Signature must be at end of URL.')
        self.assertRegexpMatches(signed_request.url, r'&client=gme-businessname', 'URL must containg client id.')
        # Verified against https://m4b-url-signer.appspot.com/
        self.assertRegexpMatches(signed_request.url, r'&signature=7bVsUv6kyRHlG0DBAIhKHfX-96M=', 'Incorrect signature')


if __name__ == "__main__":
    unittest.main()
