#!/usr/bin/python

"""addlocation.py: Flask app that loads web interface for adding new locations
to our network of free to use internet enabled computers.
"""

import flask, flask.views
from pygeocoder import Geocoder
import urllib
import urllib2
import json
from urllib2 import Request, urlopen, URLError
import arrow
import os


app = flask.Flask(__name__)

app.secret_key = "bacon"

#Dictionary that maps secondary unit names to their abbreviations
sec_unit_abbrevs = {
    'LOWER': 'LOWR',
    'OFFICE': 'OFC',
    'STOP': 'STOP',
    'LOT': 'LOT',
    'SUITE': 'STE',
    'REAR': 'REAR',
    'PENTHOUSE': 'PH',
    'ROOM': 'RM',
    'FLOOR': 'FL',
    'TRAILER': 'TRLR',
    'DEPARTMENT': 'DEPT',
    'LOBBY': 'LBBY',
    'APARTMENT': 'APT',
    'SPACE': 'SPC',
    'FRONT': 'FRNT',
    'SLIP': 'SLIP',
    'BASEMENT': 'BSMT',
    'PIER': 'PIER',
    'UNIT': 'UNIT',
    'HANGAR': 'HNGR',
    'BUILDING': 'BLDG',
    'SIDE': 'SIDE',
    }

apikey = os.environ.get('CARTO_DB_API_KEY')
url = 'http://localfreeweb.cartodb.com/api/v2/sql'

class View(flask.views.MethodView):
    
    def get(self):
        return flask.render_template('addlocation.html')
    
    def post(self):
        """Pulls and cleans the new location's data from addlocation.html's
        HTML form. It then builds a SQL INSERT statement for adding a
        new location to the 'freeweb' database on CartoDB.
        """
        bizname = str(flask.request.form['name']).replace("'", "\'\'")
        street_address = str(flask.request.form['street_address'])
        line_two = str(flask.request.form['line_two'])
        phone = str(flask.request.form['phone'])
        website = str(flask.request.form['website'])
        
        if website == '': website = 'NONE'
        
        if str(flask.request.form['day0']) == '': hrs = ['CLOSED']
        else: hrs = [str(flask.request.form['day0'])]
        
        if str(flask.request.form['day1']) == '': hrs.append('CLOSED')
        else: hrs.append(str(flask.request.form['day1']))
        
        if str(flask.request.form['day2']) == '': hrs.append('CLOSED')
        else: hrs.append(str(flask.request.form['day2']))
        
        if str(flask.request.form['day3']) == '': hrs.append('CLOSED')
        else: hrs.append(str(flask.request.form['day3']))
        
        if str(flask.request.form['day4']) == '': hrs.append('CLOSED')
        else: hrs.append(str(flask.request.form['day4']))
        
        if str(flask.request.form['day5']) == '': hrs.append('CLOSED')
        else: hrs.append(str(flask.request.form['day5']))
        
        if str(flask.request.form['day6']) == '': hrs.append('CLOSED')
        else: hrs.append(str(flask.request.form['day6']))
        
        org_type = 'NONE'
        training_types = 'NONE'
        #Creates JSON object that includes all relevant location data about
        #address provided
        address = Geocoder.geocode(street_address + ", San Francisco, CA")
        if address.valid_address and bizname != '':      
            insert = build_sql_insert(address, line_two, bizname, hrs,
                                      org_type, phone, training_types, website)
            make_request(insert)
            result = "New location added to: "
            result += "https://localfreeweb.cartodb.com/tables/freeweb"
        else:
            result = "Invalid Address"
        flask.flash(result)
        return self.get()
        
        
app.add_url_rule('/', view_func=View.as_view('main'), methods=['GET', 'POST'])

#Helper functions
def build_sql_insert(address, line_two, bizname, hrs, org_type, phone,
                     training_types, website):
    """Takes the new location's meta data and uses it to create a
    SQL INSERT statement.
    
    In args:    address(JSON object with location data relevant to the address)
                hrs(List of strings each describing a weekday's hours of
                avaliablity starting with Monday's hours at index 0)
                line_two, bizname, org_type, phone, training_types, website
    Out arg:    insert
    """
    insert = 'INSERT INTO freeweb (address, bizname, '
    insert += 'day0, day1, day2, day3, day4, day5, day6, '
    insert += 'org_type, phone, training_types, website, the_geom) '
    insert += 'VALUES (\'' + trim_address(address, line_two) + '\', '
    insert += '\'' + bizname + '\', \'' + hrs[0] + '\', \'' + hrs[1]
    insert += '\', \'' + hrs[2] + '\', \'' + hrs[3] + '\', \'' + hrs[4]
    insert += '\', \'' + hrs[5] + '\', \'' + hrs[6] + '\', \'' + org_type
    insert += '\', \'' + phone + '\', \'' + training_types + '\', \''
    insert += website + '\', ST_SetSRID(ST_Point('
    insert += str(address[0].coordinates[1]) + ','
    insert += str(address[0].coordinates[0]) + '),4326))'
    return insert


def trim_address(address, line_two):
    """Takes as input the complete address object created by pygeocoder and
    'Apt/Fl/Rm/Ste' info as it was entered in the HTML form and returns the
    short version of the street address and 'Apt/Fl/Rm/Ste' info as one
    complete street address.
    
    Global var in:    sec_unit_abbrevs
    In args:          address
                      (JSON object with location data relevant to the address)
                      line_two
    Out arg:          shortened_address
    """
    street_addr = address.raw[0]['address_components'][1]['short_name']
    if line_two != '':
        line_two_parts = line_two.split()
        for i, token in enumerate(line_two_parts):
            if token.upper() in sec_unit_abbrevs.keys():
                line_two_parts[i] = sec_unit_abbrevs[token.upper()].title()
        street_addr += ', ' + ' '.join(line_two_parts)
    shortened_address = address.street_number + ' ' + street_addr
    return shortened_address

def make_request(insert):
    """Builds and opens url for SQL INSERT statement to add new location to the
    'freeweb' database on CartoDB.
    
    Global vars in:    api_key, url
    In arg:            insert
    """
    params = {
        'api_key' : apikey, # our account apikey, don't share!
        'q'       : insert  # our insert statement above
    }
    data = urllib.urlencode(params)
    print 'Encoded:', data
    
    try:
        response = urllib2.urlopen(url + '?' + data)
        
    except urllib2.HTTPError, e:
        
        print e.code
        print e.msg
        print e.headers
        print e.fp.read()
    

#Turn on debug mode ie; changes are immediately reflected 
app.debug = True

app.run()

