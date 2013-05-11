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
Python wrapper for Google Geocoding API V3.

* **Geocoding**: convert a postal address to latitude and longitude
* **Reverse Geocoding**: find the nearest address to coordinates

"""

import requests
import functools
from pygeolib import GeocoderError, GeocoderResult
try:
    import json
except ImportError:
    import simplejson as json


VERSION = '1.2'
__all__ = ['Geocoder', 'GeocoderError', 'GeocoderResult']


# this decorator lets me use methods as both static and instance methods
class omnimethod(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return functools.partial(self.func, instance)


class Geocoder:
    """
    A Python wrapper for Google Geocoding V3's API

    """

    GEOCODE_QUERY_URL = 'https://maps.google.com/maps/api/geocode/json?'

    def __init__(self, api_key=None):
        """
        Create a new :class:`Geocoder` object using the given `api_key` and
        `referrer_url`.

        :param api_key: Google Maps Premier API key
        :type api_key: string
        :param referrer_url: URL of the website using or displaying information
         from this module.
        :type referrer_url: string

        Google Maps API Premier users can provide his key to make 100,000 requests
        a day vs the standard 2,500 requests a day without a key

        """
        self.api_key = api_key

    @omnimethod
    def get_data(self, params={}):
        """Retrieve a JSON object from a (parameterized) URL.

        :param query_url: The base URL to query
        :type query_url: string
        :param params: Dictionary mapping (string) query parameters to values
        :type params: dict
        :param headers: Dictionary giving (string) HTTP headers and values
        :type headers: dict
        :return: A `(url, json_obj)` tuple, where `url` is the final,
        parameterized, encoded URL fetched, and `json_obj` is the data
        fetched from that URL as a JSON-format object.
        :rtype: (string, dict or array)

        """

        response = requests.get(Geocoder.GEOCODE_QUERY_URL, params=params).json()

        if response['status'] != GeocoderError.G_GEO_OK:
            raise GeocoderError(response['status'], response.url)
        return response['results']

    @omnimethod
    def geocode(self, address, sensor='false', bounds='', region='', language=''):
        """
        Given a string address, return a dictionary of information about
        that location, including its latitude and longitude.

        :param address: Address of location to be geocoded.
        :type address: string
        :param sensor: ``'true'`` if the address is coming from, say, a GPS device.
        :type sensor: string
        :param bounds: The bounding box of the viewport within which to bias geocode results more prominently.
        :type bounds: string
        :param region: The region code, specified as a ccTLD ("top-level domain") two-character value for biasing
        :type region: string
        :param language: The language in which to return results.
        :type language: string
        :returns: `geocoder return value`_ dictionary
        :rtype: dict
        :raises GeocoderError: if there is something wrong with the query.

        For details on the input parameters, visit
        http://code.google.com/apis/maps/documentation/geocoding/#GeocodingRequests

        For details on the output, visit
        http://code.google.com/apis/maps/documentation/geocoding/#GeocodingResponses

        """

        params = {
            'address':  address,
            'sensor':   sensor,
            'bounds':   bounds,
            'region':   region,
            'language': language,
        }
        return GeocoderResult(Geocoder.get_data(params=params))

    @omnimethod
    def reverse_geocode(self, lat, lng, sensor='false', bounds='', region='', language=''):
        """
        Converts a (latitude, longitude) pair to an address.

        :param lat: latitude
        :type lat: float
        :param lng: longitude
        :type lng: float
        :return: `Reverse geocoder return value`_ dictionary giving closest
            address(es) to `(lat, lng)`
        :rtype: dict
        :raises GeocoderError: If the coordinates could not be reverse geocoded.

        Keyword arguments and return value are identical to those of :meth:`geocode()`.

        For details on the input parameters, visit
        http://code.google.com/apis/maps/documentation/geocoding/#GeocodingRequests

        For details on the output, visit
        http://code.google.com/apis/maps/documentation/geocoding/#ReverseGeocoding

        """
        params = {
            'latlng':   "%f,%f" % (lat, lng),
            'sensor':   sensor,
            'bounds':   bounds,
            'region':   region,
            'language': language,
        }

        return GeocoderResult(Geocoder.get_data(params=params))

    @omnimethod
    def address_to_latlng(self, address):
        """
        Given a string `address`, return a `(latitude, longitude)` pair.

        This is a simplified wrapper for :meth:`geocode()`.

        :param address: The postal address to geocode.
        :type address: string
        :return: `(latitude, longitude)` of `address`.
        :rtype: (float, float)
        :raises GoogleMapsError: If the address could not be geocoded.

        """
        location = Geocoder.geocode(address).raw[0]['geometry']['location']
        return location['lat'], location['lng']

    @omnimethod
    def latlng_to_address(self, lat, lng):
        """
        Given a latitude `lat` and longitude `lng`, return the closest address.

        This is a simplified wrapper for :meth:`reverse_geocode()`.

        :param lat: latitude
        :type lat: float
        :param lng: longitude
        :type lng: float
        :return: Closest postal address to `(lat, lng)`, if any.
        :rtype: string
        :raises GoogleMapsError: if the coordinates could not be converted
         to an address.

        """
        return Geocoder.reverse_geocode(lat, lng).raw[0]['formatted_address']

if __name__ == "__main__":
    import sys
    from optparse import OptionParser

    def main():
        """
        Geocodes a location given on the command line.

        Usage:
            pygeocoder.py "1600 amphitheatre mountain view ca" [YOUR_API_KEY]
            pygeocoder.py 37.4219720,-122.0841430 [YOUR_API_KEY]

        When providing a latitude and longitude on the command line, ensure
        they are separated by a comma and no space.

        """
        usage = "usage: %prog [options] address"
        parser = OptionParser(usage, version=VERSION)
        parser.add_option("-k", "--key", dest="key", help="Your Google Maps API key")
        (options, args) = parser.parse_args()

        if len(args) != 1:
            parser.print_usage()
            sys.exit(1)

        query = args[0]
        gcoder = Geocoder(options.key)

        try:
            result = gcoder.geocode(query)
        except GeocoderError as err:
            sys.stderr.write('%s\n%s\nResponse:\n' % (err.url, err))
            json.dump(err.response, sys.stderr, indent=4)
            sys.exit(1)

        print(result)
        print(result.coordinates)
    main()
