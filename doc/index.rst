.. googlemaps documentation master file, created by John Kleint
   2009 Sep 11.  This is a Sphinx reStructured Text file that
   mostly references the docstrings in the source code.
   You should be able to build the documentation by running
   'sphinx-build . html/'.
   
.. _sourceforge.net: http://sourceforge.net/projects/py-googlemaps
.. |projectpage| replace:: http://sourceforge.net/projects/py-googlemaps
.. _easy_install: http://pypi.python.org/pypi/setuptools
.. _PyPI: http://pypi.python.org/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _`Google Maps API key`: http://code.google.com/apis/maps/signup.html
.. _`rate limits`: http://code.google.com/apis/maps/faq.html#geocoder_limit
.. _simplejson: http://pypi.python.org/pypi/simplejson/


=================================================================
:mod:`googlemaps` -- Google Maps and Local Search APIs in Python
=================================================================

.. autoclass:: googlemaps.GoogleMaps()


:class:`GoogleMaps` methods
---------------------------

.. currentmodule:: googlemaps
.. automethod:: GoogleMaps.__init__

Geocoding
'''''''''

.. automethod:: GoogleMaps.address_to_latlng
.. automethod:: GoogleMaps.geocode

Reverse Geocoding
'''''''''''''''''

.. automethod:: GoogleMaps.latlng_to_address
.. automethod:: GoogleMaps.reverse_geocode

Directions
''''''''''

.. automethod:: GoogleMaps.directions

Local Search
''''''''''''

.. automethod:: GoogleMaps.local_search


Installation
------------

It's as easy as::
	
	sudo easy_install googlemaps

For Python versions prior to 2.6, you may also need the simplejson_ module.

Not got root?  :mod:`googlemaps` plays nice with virtualenv_.

You can also download the source from sourceforge.net_;  :file:`googlemaps.py` 
packs all this delicious functionality into a single, self-contained module 
that can be used as a script for command-line geocoding.
  
easy_install_ is available from PyPI_ if you don't have it already.


Notes
------
You will need your own `Google Maps API key`_ to use the geocoding functions
of this module.  There are `rate limits`_ to the number of requests per day
from a single IP address.  If you make too many requests, or you use an
invalid API key, or something else is wrong with your request, 
a :exc:`GoogleMapsError` will be raised containing a 
`status code <http://code.google.com/apis/maps/documentation/geocoding/#StatusCodes>`_
and brief description of the error; more information can be found at the linked
reference.

All of the data returned by this module is in `JSON <http://www.json.org/>`_-compatible 
format, making it easy to combine with other web services.


Information
-----------
:Author: John Kleint
:Version: |version|
:License: Lesser Affero General Public License v3
:Source: |projectpage|
:Python Versions: 2.3 - 2.6+

*This software comes with no warranty and is in no way associated with Google 
Inc. or the Google Maps™ mapping service.  Google does not approve or 
endorse this software.  GOOGLE is a trademark of Google Inc.*
