#!/usr/bin/python
# # # # # # # # # # # # # # # # # # # # # # 
#
# project: Smart Bus Stops Done Dirt Cheap
# title: localStories
# file: localStories.py
# description: Local stories for SBSDC
# language: python
# 
# authors: Andrew Hyder
# date: 9/26/2012
# version: 1.0.0
# notes: Hear a story about the bus stop
#
# keywords: share, tell, story, stories, overheard, munidiaries, twitter, hear, listen, tale
#
# # # # # # # # # # # # # # # # # # # # # #
import sys, urllib, simplejson, random
phoneNum = sys.argv[1]
bus_stop_lat = sys.argv[2]
bus_stop_lng = sys.argv[3]
message_string = sys.argv[4]
message_list = message_string.split(' ')

def share_local_story(bus_stop_lat,bus_stop_lng,message_string):
    message_string = message_string.replace('share','')
    message_string = message_string.replace('Share','')
    cdb_api = 'http://ondrae.cartodb.com/api/v2/sql'
    insert_sql = 'q=INSERT INTO local_stories (story, the_geom)'
    values_sql = 'VALUES (\''+message_string+'\', ST_SetSRID(ST_Point('+bus_stop_lng+','+bus_stop_lat+'),4326))'
    api_key = '&api_key=c76fc43a824ff3b12c0f6ea0d6bcff28fd787926'
    response = urllib.urlopen(cdb_api,insert_sql+values_sql+api_key)
    for line in response:
        response_dict = simplejson.loads(line)
        try:
            if response_dict['total_rows'] == 1:
                print 'Got it. We\'ll tell people your tall tale.'
        except:
            print 'Sorry, that story was boring. Or we broke something. Our fault.'
            

def clean_message_list(message_list):
    # Get rid of punctuation for parsing which stories to grab.
    if '.' or '?' in message_list[-1]:
        message_list[-1] = message_list[-1][:len(message_list[-1])-1]
    return message_list

def get_local_story(bus_stop_lat,bus_stop_lng,local_stories_list):
    cdb_api = 'http://ondrae.cartodb.com/api/v2/sql'
    select_sql = 'q=SELECT story FROM local_stories WHERE the_geom = ST_SetSRID(ST_Point('+bus_stop_lng+','+bus_stop_lat+'),4326)'
    api_key = '&api_key=c76fc43a824ff3b12c0f6ea0d6bcff28fd787926'
    response = urllib.urlopen(cdb_api,select_sql+api_key)
    for line in response:
        response_dict = simplejson.loads(line)
        for row in response_dict['rows']:
            if row:
                local_stories_list.append(row['story'])
    return local_stories_list 

def get_munidiaries(bus_stop_lat,bus_stop_lng,local_stories_list):
    response = urllib.urlopen('http://search.twitter.com/search.json?geocode='+bus_stop_lat+','+bus_stop_lng+',1mi&q=munidiaries')
    for line in response:
        response_dict = simplejson.loads(line)
        for result in response_dict['results']:
            local_stories_list.append(result['text'])
    return local_stories_list

def get_local_tweet(bus_stop_lat,bus_stop_lng,local_stories_list):
    response = urllib.urlopen('http://search.twitter.com/search.json?geocode='+bus_stop_lat+','+bus_stop_lng+',0.1mi')
    for line in response:
        response_dict = simplejson.loads(line)
        for result in response_dict['results']:
            local_stories_list.append(result['text'])
    return local_stories_list

local_stories_list = []

message_list = clean_message_list(message_list)

# If write or tell is in message, this will write the story to the bus stop.
if message_list[0].lower() == 'share':
    share_local_story(bus_stop_lat,bus_stop_lng,message_string)
else:
    # Else check the different sources for local stories
    local_stories_list = get_local_story(bus_stop_lat, bus_stop_lng, local_stories_list)
    if not local_stories_list:
        local_stories_list = get_munidiaries(bus_stop_lat,bus_stop_lng,local_stories_list)
    if not local_stories_list:
        local_stories_list = get_local_tweet(bus_stop_lat,bus_stop_lng,local_stories_list)

    if local_stories_list:
        print local_stories_list[random.randint(0,len(local_stories_list)-1)]
    else:
        print 'Sorry, no local stories to be found.'

    print '\nText \'share\' as the first word to add a local story to a bus stop id.'