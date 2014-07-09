import flask, flask.views
from pygeocoder import Geocoder
import urllib
import urllib2
from urllib2 import Request, urlopen, URLError

app = flask.Flask(__name__)

app.secret_key = "bacon"

class View(flask.views.MethodView):
    
    def get(self):
        return flask.render_template('index.html')
    
    def post(self):
        username = 'localfreeweb'
        apikey = '7270d49fc0df4bde53065e27dd5942d264bc46ef'
        url = 'http://localfreeweb.cartodb.com/api/v2/sql'
        name = str(flask.request.form['name'])
        street_address = str(flask.request.form['street_address'])
        city = str(flask.request.form['city'])
        state = str(flask.request.form['state'])
        zipcode = str(flask.request.form['zip'])
        phone = str(flask.request.form['phone'])
        website = str(flask.request.form['website'])
        if website == '':
            website = 'NONE'
        org_type = 'NONE'
        training_types = 'NONE'
        result = "Name: " + name + "\n"
        result += "Street address: " + street_address + "\n"
        result += "City, State: " + city + ", " + state + "\n"
        result += "Zipcode: " + zipcode + "\n"
        result += "Contact Number: " + phone + "\n"
        result += "Website: " + website + "\n"
        
        address = Geocoder.geocode(street_address + ", " + city + ", " + state)
        if address.valid_address and name != '':
            result += "Clean address: " + str(address) + "\n"
            result += "Lat: " + str(address[0].coordinates[0]) + "\n"
            result += "Long: " + str(address[0].coordinates[1]) + "\n"
            insert = 'INSERT INTO freeweb (address, city, name, org_type, phone, training_types, website, zip, the_geom) '
            insert += 'VALUES (' + '\'' + address.street_number + ' ' + address.route + '\', \'' + city + '\', \'' + name + '\', \'' + org_type + '\', \'' + phone + '\', \'' + training_types + '\', \'' + website + '\', \'' + zipcode + '\', '
            insert += 'ST_SetSRID(ST_Point(' + str(address[0].coordinates[1]) + ',' + str(address[0].coordinates[0]) + '),4326))'
            
            params = {
                'api_key' : apikey, # our account apikey, don't share!
                'q'       : insert  # our insert statement above
            }
            data = urllib.urlencode(params)
            print 'Encoded:', data
            url += '?' + data
            #request = urllib2.Request(url)
            
            try:
                response = urllib2.urlopen(url)
                
            except urllib2.HTTPError, e:
                
                print e.code
                print e.msg
                print e.headers
                print e.fp.read()
            
            result += '\n' + url
        else:
            result = "Invalid Address"
        flask.flash(result)
        return self.get()
    
    
        
app.add_url_rule('/', view_func=View.as_view('main'), methods=['GET', 'POST'])

#Turn on debug mode ie; changes are immediately reflected 
app.debug = True

app.run()
