#!/usr/bin/env python

# Copyright 2009 John Kleint
#
# This is free software, licensed under the Lesser Affero General 
# Public License, available in the accompanying LICENSE.txt file.


"""
Unit tests for googlemaps.

"""


import unittest
import doctest
    
import googlemaps
from googlemaps import GoogleMaps    

    
# You might need an actual key to run the tests.
GMAPS_API_KEY = open('gmaps-api-key.txt').readline().strip() 


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
        

    def test_local_search(self):
        """Test googlemaps local_search()."""
        gmaps = GoogleMaps(GMAPS_API_KEY, referrer_url='http://www.google.com/')
        local = gmaps.local_search('sushi san francisco, ca')
        result = local['responseData']['results'][0]
        self.assertEqual(result['titleNoFormatting'], 'Sushi Groove')
        
        results = gmaps.local_search('Starbucks Los Angeles, CA', numresults=GoogleMaps.MAX_LOCAL_RESULTS)
        self.assertEqual(results['responseStatus'], googlemaps.STATUS_OK)
        self.assertNotEqual(results['responseData'], None)
        self.assertNotEqual(results['responseData']['cursor'], None)
        results = results['responseData']['results']
        self.assertEqual(len(results), GoogleMaps.MAX_LOCAL_RESULTS)
        for result in results:
            self.assertEqual(result['GsearchResultClass'], 'GlocalSearch')
            self.assert_(result['titleNoFormatting'].lower().find('starbucks') >= 0)
            self.assertEqual(result['region'], 'CA')
        

    def test_directions(self):
        """Test googlemaps directions()"""
        
        gmaps = GoogleMaps(GMAPS_API_KEY)
        results = gmaps.directions('Constitution Ave NW & 10th St NW, Washington, DC',
                                   'Independence and 6th SW, Washington, DC 20024, USA')
        self.assertEqual(results['Status']['code'], googlemaps.STATUS_OK)
        self.assert_(results['Directions']['Duration']['seconds'] in range(100, 130))
        self.assert_(results['Directions']['Distance']['meters'] in range(1000, 1050))
        routes = results['Directions']['Routes']
        self.assert_(len(routes) >= 1)
        self.assertEqual(routes[0]['Duration'], results['Directions']['Duration'])
        self.assertEqual(routes[0]['Distance'], results['Directions']['Distance'])
        self.assert_(routes[0]['Steps'][0]['descriptionHtml'].find('Constitution Ave') >= 0)
        self.assert_(routes[0]['Steps'][1]['descriptionHtml'].find('7th St') >= 0)
        self.assert_(routes[0]['Steps'][2]['descriptionHtml'].find('Independence Ave') >= 0)
        
    def test_doctests(self):
        """Run googlemaps doctests"""
        doctest.testmod(googlemaps, extraglobs={'api_key': GMAPS_API_KEY})

        
if __name__ == "__main__":
    unittest.main()