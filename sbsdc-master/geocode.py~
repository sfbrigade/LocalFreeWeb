#!/usr/bin/python
# # # # # # # # # # # # # # # # # # # # # # 
#
# project: Smart Bus Stops Done Dirt Cheap
# file: geocode.py
# description: Geolocation functions for SBSDC
# language: python
# 
# authors: Anders Finn (anders@visiblethinking.com), Andrew Hyder (hyd415@gmail.com)
# date: 9/9/2012
# version: 1.0.2
# notes:
#
# # # # # # # # # # # # # # # # # # # # # # 

import urllib, simplejson

# sub that does lookup of geolocation and retuns lat, long
def get_location(stop_id):
    get_geo_url = 'http://ondrae.cartodb.com/api/v2/sql?q=SELECT%20latitude,%20longitude%20FROM%20sf_bus_stops%20WHERE%20stopid%20=%20'
    get_geo_url = get_geo_url + str(stop_id)
    response = urllib.urlopen(get_geo_url)
    for line in response:
    	response_dict = simplejson.loads(line)
    geo_lat = str(response_dict['rows'][0]['latitude'])
    geo_long = str(response_dict['rows'][0]['longitude'])
    lat_long = [geo_lat,geo_long]
    return lat_long
