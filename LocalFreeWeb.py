#!/usr/bin/python

#Sample response text message:
#Ask for 'free internet' at these places: 4468 Mission St (10am-4pm); 4080 Mission St (930am-1230pm); 515 Cortland Ave (1230pm-1200am)

#Sample initial text message:
#Text 913*1 to 40909 for the nearest free internet access.
#Texto 913*2 to 40909 para el internet mas proximo
#Chinese 913*3 Chinese 40909 Chinese

from flask import Flask, request, redirect
import twilio.twiml
import urllib, simplejson

if __name__ == '__main__':
    stop_id = raw_input('Enter Bus Stop ID: ')
    get_geo_url = 'http://localfreeweb.cartodb.com/api/v2/sql?q=SELECT stop_lat, stop_lon FROM stops WHERE stop_id = '
    get_geo_url += stop_id
    response = urllib.urlopen(get_geo_url)
    for line in response:
    	response_dict = simplejson.loads(line)
#    print response_dict
    geo_lat = str(response_dict['rows'][0]['stop_lat'])
    geo_long = str(response_dict['rows'][0]['stop_lon'])
    lat_long = [geo_lat,geo_long]
#    print lat_long
    
    get_closest_free_net_url = 'http://localfreeweb.cartodb.com/api/v2/sql?q=SELECT name, address, zip, phone, ST_Distance(the_geom::geography, ST_PointFromText(\'POINT('+ geo_long + ' ' + geo_lat + ')\', 4326)::geography) AS distance FROM freeweb ORDER BY distance ASC LIMIT 3'
    response = urllib.urlopen(get_closest_free_net_url)
    for line in response:
       	response_dict = simplejson.loads(line)
#    	print response_dict
        response = '\nAsk for \'free internet\' at these places:'
    for i in range(0, 3):
#    	    print str(response_dict['rows'][i]['name'])
    	    response += ' ' + str(response_dict['rows'][i]['address']) + ';'
#    	    print 'San Francisco, CA ' + str(response_dict['rows'][i]['zip'])
#    	    print 'Phone number: ' + str(response_dict['rows'][i]['phone'])
    if type(response) is str:
        print response
    	    
