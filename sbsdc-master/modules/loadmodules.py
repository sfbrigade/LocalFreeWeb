#!/usr/bin/python
# # # # # # # # # # # # # # # # # # # # # # 
#
# project: Smart Bus Stops Done Dirt Cheap
# title: example
# file: example.py
# description: example modulefor SBSDC
# language: python
# 
# authors: Anders Finn (anders@visiblethinking.com)
# date: 9/9/2012
# version: 1.0.0
# notes: An example of what a module needs for input and output.
#
# keywords: test
#
# # # # # # # # # # # # # # # # # # # # # #


import sys
import os
sys.path.insert(0, 'test_area')
from WhereIs import WhereIs

phone_num = sys.argv[1]
bus_stop_lat = sys.argv[2]
bus_stop_lng = sys.argv[3]
message_string = sys.argv[4]
message_list = message_string.split(' ')

x=WhereIs(phone_num, bus_stop_lat, bus_stop_lng, message_string)
#x.return_walking=True
import pdb; pdb.set_trace()
print x.get_answer()

print x.query_string
