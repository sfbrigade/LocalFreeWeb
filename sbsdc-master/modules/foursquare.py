#!/usr/bin/python
# # # # # # # # # # # # # # # # # # # # # # 
#
# project: Smart Bus Stops Done Dirt Cheap
# title: foursquare
# file: foursquare.py
# description: Local Places
# language: python
# 
# authors: Andrew Hyder
# date: 9/18/2012
# version: 1.0.0
# notes: local shit
#
# keywords: places, food, drink, art, best, where, closest, nearby, near
#
# # # # # # # # # # # # # # # # # # # # # #
import sys, urllib, simplejson, datetime, random

def fake_nl_processor(message_list):
	if 'find' in s:
		k = s.split()


phoneNum = sys.argv[1]
bus_stop_lat = sys.argv[2]
bus_stop_lng = sys.argv[3]
message_list = sys.argv[4:]
message_str = ' '.join(message_list)

def parse_message(l):
	key_list=['best', 'where', 'closest', 'nearby', 'find', 'good', 'near']
	message = ''
	for item in key_list:
		if item in l:
			i = l.index(item)
			m_list = l[i+1:]
			message = ' '.join(m_list)
		else:
			message = ' '.join(l)
	return message



def get_query(lat, lng, query):
	fq_api = 'https://api.foursquare.com/v2/venues/search'
	location = '?ll='+str(bus_stop_lat)+','+str(bus_stop_lng)
	limit = '&limit=5'
	radius = '&radius=1000'
	query = '&query='+ query
	oauth_key ='&oauth_token=EIIMHUKS2TFQALQMUBRGUZQ4QVLUEUTDR4MG0U2UZ1DLND5E&v=20120917'
	response = urllib.urlopen(fq_api+location+limit+query+radius+oauth_key)
	return response

def print_walking_directions(bus_stop_lat, bus_stop_lng, dest_lat, dest_lng):
	mq_api = 'http://open.mapquestapi.com/directions/v1/route?outFormat=json&routeType=pedestrian&timeType=1'
	from_bus_stop = '&from=' + str(bus_stop_lat) + ',' + str(bus_stop_lng)
	to_dest = '&to=' + str(dest_lat) + ',' + str(dest_lng)
	response = urllib.urlopen(mq_api+from_bus_stop+to_dest)
	for line in response:
	    response_dict = simplejson.loads(line)
	legs_list = response_dict['route']['legs']
	legs_dict = legs_list[0]
	for v in legs_dict['maneuvers']:
	    print v['narrative']

message = parse_message(message_list)
response = get_query(bus_stop_lat, bus_stop_lng, message)

for line in response:
	response_dict = simplejson.loads(line)	
	venue_count=0
	random_number=0
	
	for venue in response_dict['response']['venues']:
		venue_count+=1
		random_number=random.randint(0,venue_count-1)
	
	try:
		venue_name = response_dict['response']['venues'][random_number]['name']
		venue_lat = response_dict['response']['venues'][random_number]['location']['lat']
		venue_lng = response_dict['response']['venues'][random_number]['location']['lng']
		venue_address = response_dict['response']['venues'][random_number]['location']['address']
	except (IndexError, KeyError):
		sys.exit('No results.  Best ask someone else!')
	
	print '%s: %s' % (venue_name, venue_address)
	
	print_walking_directions(bus_stop_lat, bus_stop_lng, venue_lat, venue_lng)

	
