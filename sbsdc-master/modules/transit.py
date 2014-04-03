#!/usr/bin/python
# # # # # # # # # # # # # # # # # # # # # # 
#
# project: Smart Bus Stops Done Dirt Cheap
# title: transit
# file: transit.py
# description: Transit Directions module for SBSDC
# language: python
# 
# authors: Andrew Hyder
# date: 10/15/2012
# version: 1.0.0
# notes: Gives transit directions
#
# keywords: transit, bus, directions, how, train, muni, subway, bart, rail
#
# # # # # # # # # # # # # # # # # # # # # #

import sys, urllib, simplejson

phoneNum = sys.argv[1]
bus_stop_lat = sys.argv[2]
bus_stop_lng = sys.argv[3]
message_string = sys.argv[4]
message_list = message_string.split(' ')

def parse_destination(message_list):
	# take out bus id and from
	for word in message_list:
		try:
			number = int(word)
			message_list.remove(word)
			if word == 'from':
				message_list.remove('from')
		except:
			pass
	message_str = ' '.join(message_list)
	destination = message_str
	transit_words = ['transit','bus','train','rail','bart','muni','subway']
	for transit_word in transit_words:
		if transit_word in message_list:
			i = message_list.index(transit_word)
			dest_list = message_list[i+1:]
			destination = ''
			destination = ' '.join(dest_list)
	if 'to' in message_list:
		i = message_list.index('to')
		dest_list = message_list[i+1:]
		destination = ''
		destination = ' '.join(dest_list)

	return destination

def get_destination_lat_lon(bus_stop_lat,bus_stop_lng,destination):
	fq_api = 'https://api.foursquare.com/v2/venues/search'
	location = '?ll='+str(bus_stop_lat)+','+str(bus_stop_lng)
	limit = '&limit=1'
	query = '&query='+destination
	oauth_key ='&oauth_token=EIIMHUKS2TFQALQMUBRGUZQ4QVLUEUTDR4MG0U2UZ1DLND5E&v=20120917'
	response = urllib.urlopen(fq_api+location+limit+query+oauth_key)
	for line in response:
		response_dict = simplejson.loads(line)
		for venue in response_dict['response']['venues']:
			dest_name = venue['name']
			dest_lat = venue['location']['lat']
			dest_lng = venue['location']['lng']
	return dest_name, dest_lat, dest_lng

def get_transit_directions(bus_stop_lat, bus_stop_lng, dest_lat, dest_lng):
	mq_api = 'http://open.mapquestapi.com/directions/v1/route?outFormat=json&routeType=multimodal&timeType=1'
	from_bus_stop = '&from=' + str(bus_stop_lat) + ',' + str(bus_stop_lng)
	to_dest = '&to=' + str(dest_lat) + ',' + str(dest_lng)
	#print mq_api+from_bus_stop+to_dest
	response = urllib.urlopen(mq_api+from_bus_stop+to_dest)
	for line in response:
	    response_dict = simplejson.loads(line)
	#print response_dict
	legs_list = response_dict['route']['legs']
	if legs_list:
		legs_dict = legs_list[0]
		for v in legs_dict['maneuvers']:
			#if v['transportMode'] != 'WALKING':
				if v['transportMode'] != 'AUTO':
					print v['narrative']
	else:
		print 'Sorry, couldn\'t find directions there. Better ask somebody else.'

destination = parse_destination(message_list)
if not destination:
	print 'Sorry, couldn\'t find directions there. Better ask somebody else.'
	sys.exit()
dest_name, dest_lat, dest_lng = get_destination_lat_lon(bus_stop_lat,bus_stop_lng,destination)
print dest_name
get_transit_directions(bus_stop_lat,bus_stop_lng,dest_lat,dest_lng)




