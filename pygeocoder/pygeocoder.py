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


import urllib
import urllib2
try:
	import json
except ImportError:
	import simplejson as json


VERSION = '1.0'
__all__ = ['Geocoder', 'GeocoderError']	  

class GeocoderError(Exception):
	"""Base class for errors in the :mod:`pygeocoder` module.
	
	Methods of the :class:`Geocoder` raise this when something goes wrong.
	 
	"""
	#: See http://code.google.com/apis/maps/documentation/geocoding/index.html#StatusCodes
	#: for information on the meaning of these status codes.
	G_GEO_OK			   = "OK"
	G_GEO_ZERO_RESULTS	   = "ZERO_RESULTS"
	G_GEO_OVER_QUERY_LIMIT = "OVER_QUERY_LIMIT"
	G_GEO_REQUEST_DENIED   = "REQUEST_DENIED"
	G_GEO_MISSING_QUERY	   = "INVALID_REQUEST"
	
	def __init__(self, status, url=None, response=None):
		"""Create an exception with a status and optional full response.
		
		:param status: Either a ``G_GEO_`` code or a string explaining the 
		 exception.
		:type status: int or string
		:param url: The query URL that resulted in the error, if any.
		:type url: string
		:param response: The actual response returned from Google, if any.
		:type response: dict 
		
		"""
		Exception.__init__(self, status)		# Exception is an old-school class
		self.status = status
		self.url = url
		self.response = response
		
	def __str__(self):
		"""Return a string representation of this :exc:`GeocoderError`."""
		return 'Error %s\nQuery: %s' % (self.status, self.url)
	
	def __unicode__(self):
		"""Return a unicode representation of this :exc:`GeocoderError`."""
		return unicode(self.__str__())


class Geocoder:
	"""
	A Python wrapper for Google Geocoding V3's API
	
	"""

	GEOCODE_QUERY_URL = 'http://maps.google.com/maps/api/geocode/json?'

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

	def getdata(self, params={}):
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
		encoded_params = urllib.urlencode(params)	 
		url = self.GEOCODE_QUERY_URL + encoded_params

		request = urllib2.Request(url)
		response = urllib2.urlopen(request)

		j = json.load(response)
		if j['status'] != GeocoderError.G_GEO_OK:
			raise GeocoderError(j['status'], url)
		return j['results']
		
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
			'address':	address,
			'sensor':	sensor,
			'bounds':	bounds,
			'region':	region,
			'language': language,
		}
		return self.getdata(params=params)

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
			'latlng':	"%f,%f" % (lat, lng),
			'sensor':	sensor,
			'bounds':	bounds,
			'region':	region,
			'language': language,
		}

		return self.getdata(params=params)
	
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
		return tuple(self.geocode(address)[0]['geometry']['location'].values())
	
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
		return self.reverse_geocode(lat, lng)[0]['formatted_address']

if __name__ == "__main__":
	import sys
	
	def main(argv):
		"""
		Geocodes a location given on the command line.
		
		Usage:
			pygeocoder.py "1600 amphitheatre mountain view ca" [YOUR_API_KEY]
			pygeocoder.py 37.4219720,-122.0841430 [YOUR_API_KEY]
			
		When providing a latitude and longitude on the command line, ensure
		they are separated by a comma and no space.
		
		"""

		if len(argv) < 2 or len(argv) > 4:
			print main.__doc__
			sys.exit(1)
			
		query = argv[1]
		gcoder = Geocoder(argv[2])

		try:
			result = gcoder.geocode(query)
		except GeocoderError, err:
			sys.stderr.write('%s\n%s\nResponse:\n' % (err.url, err))
			json.dump(err.response, sys.stderr, indent=4)
			sys.exit(1)
		json.dump(result, sys.stdout, indent=4)
		sys.stdout.write('\n')
		
	main(sys.argv)
	