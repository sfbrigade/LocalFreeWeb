#!/usr/bin/python
# # # # # # # # # # # # # # # # # # # # # # 
#
# project: Smart Bus Stops Done Dirt Cheap
# title: weather
# file: weather.py
# description: Weather modulefor SBSDC
# language: python
# 
# authors: Andrew Hyder
# date: 9/9/2012
# version: 1.0.0
# notes: fetches and sends latest weather forecast
#
# keywords: weather, forecast, hot, cold, rain, warm, fog, foggy, rainy, sun, sunny, cats, dogs
#
# # # # # # # # # # # # # # # # # # # # # #
import sys, urllib, simplejson, datetime
phoneNum = sys.argv[1]
lat = sys.argv[2]
lon = sys.argv[3]
message = sys.argv[4]

response = urllib.urlopen('http://free.worldweatheronline.com/feed/weather.ashx?q='+str(lat)+','+str(lon)+'&format=json&num_of_days=5&key=4e11214676001957120909')
for line in response:
	response_dict = simplejson.loads(line)

today = str(datetime.date.today())
retString = ''

for day in response_dict['data']['weather']:
	
	if day['date'] == today:
		retString += 'Today:' + day['tempMinF'] + '-' + day['tempMaxF'] + '\n'
		retString += 'Next 4 days:' 
	else:
		retString += day['tempMinF'] + '-' + day['tempMaxF'] + ';'

retString = retString[:-1]

print retString
