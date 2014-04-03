from flask import Flask, request
import urllib, simplejson
import twilio.twiml

app = Flask(__name__)

@app.route("/")
def receive_text():
	
	# get_geo_url = 'http://localfreeweb.cartodb.com/api/v2/sql?q=SELECT stop_lat, stop_lon FROM stops WHERE stop_id = '
	# get_geo_url += stop_id
	# response = urllib.urlopen(get_geo_url)
	# for line in response:
	# 	response_dict = simplejson.loads(line)
	# #    print response_dict
	# geo_lat = str(response_dict['rows'][0]['stop_lat'])
	# geo_long = str(response_dict['rows'][0]['stop_lon'])
	# lat_long = [geo_lat,geo_long]
	# #    print lat_long

	# get_closest_free_net_url = 'http://localfreeweb.cartodb.com/api/v2/sql?q=SELECT name, address, zip, phone, ST_Distance(the_geom::geography, ST_PointFromText(\'POINT('+ geo_long + ' ' + geo_lat + ')\', 4326)::geography) AS distance FROM freeweb ORDER BY distance ASC LIMIT 3'
	# response = urllib.urlopen(get_closest_free_net_url)
	# for line in response:
	# 	response_dict = simplejson.loads(line)
	# #    	print response_dict
	# 	for i in range(0, 3):
	# 	    print '\nResult ' + str(i + 1) + ': '
	# 	    print str(response_dict['rows'][i]['name'])
	# 	    print str(response_dict['rows'][i]['address'])
	# 	    print 'San Francisco, CA ' + str(response_dict['rows'][i]['zip'])
	# 	    print 'Phone number: ' + str(response_dict['rows'][i]['phone'])

	# return str(response_dict['rows'][i]['address'])
	return str(request.values.keys())

if __name__ == "__main__":
    app.run(debug=True)