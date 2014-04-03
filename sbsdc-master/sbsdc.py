#!/usr/bin/python
# # # # # # # # # # # # # # # # # # # # # # 
#
# project: Smart Bus Stops Done Dirt Cheap
# file: sbsdc.py
# description: core program for SBSDC
# language: python
# 
# authors: Anders Finn (anders@visiblethinking.com)
# date: 10/10/2012
# version: 1.10.2
# notes: for now does not do geolocation, just uses San Francisco
#
# # # # # # # # # # # # # # # # # # # # # # 
    
def get_module_name(message_list):
	# TODO: remove punctuation
    if message_list[0].lower() == 'about':
	return 'aboutprojects'
    for module_name, keywords in module_keys.items():
        keywords = keywords.split(', ')
        for keyword in keywords:
            for message_word in message_list:
                if keyword.lower() == message_word.lower():
                	return module_name
                    
def get_stop_id(message_list):
    for message_word in message_list:
        try:
            message_number = int(message_word)
            if len(message_word) > 3:
                stop_id = message_number
                return stop_id
        except:
            pass
    if not stop_id:
        logging.error('Didn\'t enter a bus stop id.')

def accept_conn(data):
    try:
        message = ""
        sender = ""
        for x in data.split('&'):
            if "body=" in x.lower():
                message = x[5:]
            if "from=" in x.lower():
                sender = x[8:]
        if NL == 1:
            try:
                message = " ".join(message.split("+"))
                nl_data = nl_process(message,logfile,module_keys)
                geo = get_location(nl_data[0])
                run_module(nl_data[1], geo, nl_data[2], sender, logfile)
            except Exception as e:
                logging.error("Failed in run_module in NLTK mode.\nmessage: %s\n module: %s\ngeo: %s\n%s" % message, nl_data[1], nl_data[0], e)
        else:
            try:
                message_list = message.split("+")
                message_list[-1] = message_list[-1].replace('%3F','')
                message_string = " ".join(message_list)
                module_name = get_module_name(message_list)
                # Special case for aboutprojects
		if module_name != 'aboutprojects':
		    stop_id = get_stop_id(message_list)
		    geo = get_location(stop_id)
		    run_module(module_name, geo, message_string, sender, logfile)
		else:
		    run_module(module_name, ['0','0'], message_string, sender, logfile)
            except Exception as e:
                logging.error("Failed in run_module in basic mode: %s" % e)
    except Exception as e:
        logging.error("failed in accept_conn: %s" % e)
	
if __name__ == "__main__":
    try:
	import sys
	import datetime
	import os
	import time
	import socket
	import threading
	import logging

    except ImportError as e:
	print "Unable to import all modules: %s" % e
	sys.exit()

    print 'working to here'
    # Read config file and sset global standards
    global hostname
    global port
    global logfile
    global NL
    NL=0
    
    try:
	config = open('config','r').readlines()
    except IOError as e:
	print "Unable to find Configuration file! %s" % e
	sys.exit()
	
    #Parse config file
    for line in config:
	x = line.split("=")
	if x[0].lower() == "hostname":
	    hostname = x[1].rstrip()
	elif x[0].lower() == "port":
	    port = x[1].rstrip()
	elif x[0].lower() == "logfile":
	    logfile = x[1].rstrip()
	elif x[0].lower() == "natural language":
	    x[1] = x[1].rstrip()
	    if x[1].lower() == "on":
		NL = 1

    #Logging formatting
    try:
        logging.basicConfig(filename=logfile,
			    format='%(asctime)s %(levelname)s %(message)s',
			    datefmt='%a, %d %b %Y %H:%M:%S',
			    level=logging.DEBUG)
	logging.info("\n-----------------------------------------------------\n: Startup, checking core and scanning modules.")
    except IOError, e:
        print "Unable to print to log: %s" % e
	sys.exit()

    from modules import *
    from geocode import *
    
   #If NL = 1 in config file, turn on NL processor.  
    if NL == 1:
	try:
	    from nlprocessor import *
	    #******* Fix logging std_out and this shouldn't need to be printed.********
	    print "Starting natural language processor."
	    logging.info('Starting natural language processor.')
	except ImportError as e:
	    print e
	    logging.warning(e)
    elif NL != 1:
	logging.info("Disabling NL processor")
	print("Disabling NL processor")
    backlog = 5 
    size = 1024 

    print("Starting server at %s:%s" % (hostname, port))
    logging.info("Starting server at %s:%s" % (hostname, port))

    while 1:
	try:
	    soc = None
	    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    port = int(float(port))
	    soc.bind((hostname,port))
	    soc.listen(backlog)
	    print "Server is now running on %s:%s" % (hostname, port)
	    logging.info("Server is now running on %s:%s" % (hostname, port))
	    try:
		while 1:
		    client, address = soc.accept()
		    data = client.recv(size)
		    logging.info(data)
		    if data:
			accept_conn(data)
		    client.close()
	    except Exception as e:
		logging.error(str(e) + ": Server failed.")
		sys.exit(e)
	except Exception as e:
	    logging.warning(str(e) + ': Server failed to start. %s' % soc)
	    soc = None
	time.sleep(3)
