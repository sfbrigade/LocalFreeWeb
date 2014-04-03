
#!/usr/bin/python
# # # # # # # # # # # # # # # # # # # # # # 
#
# project: Smart Bus Stops Done Dirt Cheap
# title: foursquare
# file: foursquare.py
# description: Local Places
# language: python
# 
# authors: Andrew Hyder, Cameron Jeffries
# date: 10/21/2012
# version: 2.0.0
# notes: Find stuff nearby
#
# keywords: test
# old_keys: places, food, drink, art, best, where, closest, nearby, near
#
# # # # # # # # # # # # # # # # # # # # # #



try:
	import sys, urllib, simplejson, datetime, random, re
except ImportError as e:
	print 'Trouble running module "Where_Is"'

class WhereIs:
	random_response=True
	return_walking=False
	def __init__(self, phone_num, bus_stop_lat, bus_stop_lng, message):
		self.phone_num = phone_num
		self.bus_stop_lat = bus_stop_lat
		self.bus_stop_lng = bus_stop_lng
		self.message=message
	def get_answer(self):
		if self.return_walking == True:
			r='%s\n' % self.fq_search()
			for item in (self.walking_direction_narrative()):
				r = r + item
			return r
			
		else:
			return self.fq_search()
		
		
	def fq_parser(self, s):
		hard_prefix_list=[' a ']
		prefix_list=[' best ', ' where ', ' closest ', ' find ', ' good ', ' are ']
		suffix_list=[' near me ', ' near me?', ' nearby?', ' nearby', '?']
		#query_string=s
		query_string = re.sub(" \d+", " ", s)
		for string in hard_prefix_list:
			if string.lower() in query_string.lower():
				query_string = query_string.split(string)[1]
				prefix_list=[]
		for string in prefix_list:
			if string.lower() in query_string.lower():
				query_string=query_string.split(string)[1]
		for string in suffix_list:
			if string.lower() in query_string.lower():
				query_string=query_string.split(string)[0]		
		self.query_string=query_string

	
	def fq_search(self):
		venue_count=0
		random_number=0
		self.fq_parser(self.message)

		fq_api = 'https://api.foursquare.com/v2/venues/search'
		location = 'll=%s,%s' % (self.bus_stop_lat, self.bus_stop_lng)
		if self.random_response == True:
			limit = 'limit=5'
		else:
			limit = 'limit=1'
		radius = 'radius=1000'
		query = 'query='+ self.query_string
		oauth_key ='&oauth_token=EIIMHUKS2TFQALQMUBRGUZQ4QVLUEUTDR4MG0U2UZ1DLND5E&v=20120917'
		fq_query = urllib.urlopen('%s?%s&%s&%s&%s&%s' % (fq_api,location,limit,query,radius,oauth_key))

		for line in fq_query:
			fq_dict = simplejson.loads(line)
			try:
				for venue in fq_dict['response']['venues']:
					venue_count+=1
					random_number=random.randint(0,venue_count-1)
				self.venue_name = fq_dict['response']['venues'][random_number]['name']
				self.venue_lat = fq_dict['response']['venues'][random_number]['location']['lat']
				self.venue_lng = fq_dict['response']['venues'][random_number]['location']['lng']
				self.venue_address = fq_dict['response']['venues'][random_number]['location']['address']
				return '%s: %s' % (self.venue_name, self.venue_address)
			except (IndexError, KeyError):
				return 'No Results.  Better ask someone else.'

	def walking_direction_narrative(self):
		#Needs to return an error if user doesn't have response from fq first.
		narrative_list=[]
		mq_api = 'http://open.mapquestapi.com/directions/v1/route'
		out_format='outFormat=json'
		route_type='routeType=pedestrian'
		time_type='timeType=1'
		from_bus_stop = 'from=' + self.bus_stop_lat + ',' + self.bus_stop_lng
		to_dest = 'to=%s,%s' % (self.venue_lat, self.venue_lng)
		mq_query = urllib.urlopen('%s?%s&%s&%s&%s&%s' % (mq_api,out_format,route_type,time_type,from_bus_stop,to_dest))
	
		for line in mq_query:
			response_dict = simplejson.loads(line)
		maneuvers = response_dict['route']['legs'][0]['maneuvers']
		narratives = []
		for v in maneuvers:
			narratives.append(str((v['narrative'])))
		return narratives
