#!/usr/bin/python
# # # # # # # # # # # # # # # # # # # # # # 
#
# project: Smart Bus Stops Done Dirt Cheap
# file: module.py
# description: module loader and loader program for SBSDC
# language: python
# 
# authors: Anders Finn (anders@visiblethinking.com)
# date: 9/9/2012
# version: 1.0.1
# notes: still working on getting return input
#
# # # # # # # # # # # # # # # # # # # # # # 

# search modules/ directory and determine name, language and keywords to available mods
print 'working to modules.'

try:
   import os
   import sys
   import subprocess
   import datetime
   import httplib
   import base64
   import urllib
   import logging
   import glob
except ImportError as e:
   sys.exit(e)
   
#Logging formatting
   try:
      logging.basicConfig(filename=logfile,
         format='%(asctime)s %(levelname)s %(message)s',
         datefmt='%a, %d %b %Y %H:%M:%S',
         level=logging.DEBUG)

   except IOError, e:
      sys.exit("Unable to print to log: %s" % e)

module_name = []
module_lang = {}
global module_keys
module_keys = {}

# TODO: Check to make sure modules directory isn't empty.
#

# Read modules/ directory and determine their name, language and keywords
for module in glob.glob("%s/modules/*" % os.getcwd()):
   if os.path.isfile(module): 
      x = ''
      # open module
      f = open(module, 'r')
      # Search each file found line by line for keywords
      for line in f.readlines():
         # If Title is found, save to memory cache and create a list for that module
         if "title" in line:
            y = line.split("title: ")[1][:-1]
            module_name.append(y.lower())
            x = line.split("title: ")[1][:-1].lower()
         # If Language found, save to memory cache
         if "# language:" in line:
            y = line.split("language: ")[1][:-1]
            module_lang[x] = y.lower()
            lang = ''
         # If Keywords found, save to memory cache 
         if "# keywords:" in line:
            y = line.split("keywords: ")[1][:-1]
            module_keys[x] = y.lower()
            # Write new module to logfile and check and repair permissions
      logging.info("Opening file %s. written in %s with keywords: %s." % (module, module_lang[x], module_keys[x]))
      
      # Should we really keep this line?  IMO this is kinda sloppy.  Maybe just check read permissions as it parses and fail module if it fails.
      if oct(os.stat(module)[0]) != oct(33277):
         logging.warning("Warning!! Module %s has file permissions %s, fixing. . ." % (module, oct(os.stat(module)[0])))
         os.system("chmod 775 %s" % module)
logging.info("Done loading modules.")

def split_text(s):
   #Return a list of the text messages broken up
   s_length = len(s)
   if s_length < 1386:
      cut_length = 154
   elif s_length < 13860:
      cut_length = 152
   else:
      return ['Reply too long.']
   reply_count = s_length / cut_length + 1
   r_list = []
   this_message_count=0
   for i in range(0, s_length, cut_length):
      this_message_count+=1
      if not reply_count == 1:
         r_list.append(s[i:i+cut_length] + '(%sof%s)' % (this_message_count, reply_count))
      else:
         r_list.append(s)
   return r_list   
   
   
# sub that forks off a call to external module
def run_module(name, location, message, tosms, logfile):
   out_message_list=[]
   try:
      prog = langs[module_lang[name.lower()]].split("|")[0]
      lang = langs[module_lang[name.lower()]].split("|")[1]
      myoutput = None
      PIPE = subprocess.PIPE
      logging.info("%s%s %s %s %s %s" % (name.lower(), lang, tosms, location[0], location[1], message))
      process = subprocess.Popen(["%s" % prog, "%s/modules/%s%s" % (os.getcwd(), name, lang), tosms, location[0], location[1], message], stdin=PIPE, stdout=PIPE, shell=False)
      myoutput = process.stdout.read()

      out_message_list=split_text(myoutput)

      logging.info("Running %s looking for %s." % (name.lower(), message))
   except:
      logging.error("Failed to run: %s%s" % (name.lower(), lang), tosms, location[0], location[1], message)
      #This should be made to work..
      myoutput = "Sorry there was an error in your message."
   
   for i in range(0,len(out_message_list)):

      try:
         username = "AC47761615be8d2db6fcf6512360fb7815"
         password = "89a918aa03f5c16d5f8dac2bb69c0431"
         params = {'From' : '14154187890', 'To' : tosms, 'Body' : out_message_list[i]}
         params = urllib.urlencode(params)
         auth = base64.encodestring("%s:%s" % (username, password)).replace('\n', '')
         headers = {"Authorization" : "Basic %s" % auth, 'Content-Type': 'application/x-www-form-urlencoded'}

      except:
         logging.error("Unable to load txt header.")

      try:
         conn = httplib.HTTPSConnection("api.twilio.com")
         conn.request("POST", "/2010-04-01/Accounts/AC47761615be8d2db6fcf6512360fb7815/SMS/Messages.xml", params, headers)
         response = conn.getresponse()
         data = response.read()
         conn.close()
      except:
         logging.error("Unable to send text.")

   
      
      
langs = {}
try:
   langfile = open('languages','r')
except IOError as e:
   logging.info("Unable to open logfile: %s" % (e))
   sys.exit()
for line in langfile:
   if not line[0] == "#":
      x=line.split("|")
      langs[x[0].rstrip()] = "%s|%s" % (x[1].rstrip(),x[2].rstrip())