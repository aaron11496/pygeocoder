#!/usr/bin/env python

# Copyright 2009 John Kleint
#
# This is free software, licensed under the Lesser Affero General 
# Public License, available in the accompanying LICENSE.txt file.


"""
Distutils setup script for googlemaps module.
"""


from distutils.core import setup
import sys

sys.path.insert(0, 'googlemaps')
import googlemaps


setup(name='googlemaps',
      version=googlemaps.VERSION,
      author='John Kleint',
      author_email='py-googlemaps-general@lists.sourceforge.net',
      url='http://sourceforge.net/projects/py-googlemaps/',
      download_url='https://sourceforge.net/projects/py-googlemaps/files/',
      description='Easy geocoding, reverse geocoding, driving directions, and local search in Python via Google.',
      long_description=googlemaps.GoogleMaps.__doc__,
      package_dir={'': 'googlemaps'},
      py_modules=['googlemaps'],
      provides=['googlemaps'],
      requires=['simplejson'],
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                   'License :: OSI Approved :: GNU Affero General Public License v3',
                   'Topic :: Internet',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Scientific/Engineering :: GIS',
                  ],
      keywords='google maps local search ajax api geocode geocoding directions navigation json',
      license='Lesser Affero General Public License v3',
     )
