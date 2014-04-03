#!/usr/bin/python
# # # # # # # # # # # # # # # # # # # # # # 
#
# project: Smart Bus Stops Done Dirt Cheap
# title: aboutProjects
# file: aboutProjects.py
# description: returns information about the varoius projects
# language: python
# 
# authors: Cameron Jeffries (camservo@gmail.com)
# date: 10.7.12
# version: 1.0.0
# notes: .
#
# keywords: lordareus
#
# # # # # # # # # # # # # # # # # # # # # #
import sys
import os
import csv

try:
    prog_name = sys.argv[0]
    phone_num = sys.argv[1]
    src_lat = sys.argv[2]
    src_lng = sys.argv[3]
    message_list = sys.argv[4:]
    message_str = " ".join(message_list)
except IndexError:
    sys.exit('Failure in module: aboutprojects.py')

if message_str.lower().startswith('about'):
    query_str = message_str[6:]
else:
    query_str = message_str
    
    
    

ret=''
data_dict={}

key = query_str
data_path = "%s/modules/data/aboutProjects.txt" % (os.getcwd())

try:
    with open(data_path, 'r') as f:
        reader = csv.reader(f, delimiter='|', quoting=csv.QUOTE_NONE)
        for row in reader:
            try:
                if key.lower() == str(row[0]).lower() or key.lower() in row[1].lower():
                    ret = row[2]
            except IndexError:
                continue
except Exception:
    sys.exit('Error in module aboutprojects.py')

if ret == '':
    print 'Project does not exist.  Please see project list and enter by ID or by name as printed.'
else:
    print ret
