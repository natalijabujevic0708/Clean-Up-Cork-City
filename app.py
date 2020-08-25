import os, time
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 
from  geopy.geocoders import Nominatim

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")
    
@app.route('/locations')
def locations():
    return render_template("locations.html", locations=mongo.db.locations.find())


@app.route('/insert_location', methods=['POST'])
def insert_location():
    if 'picture' in request.files:
        picture=request.files['picture']
        mongo.save_file(picture.filename, picture)
        geolocator = Nominatim(user_agent="natalijabujevic0708@gmail.com")
        city = "Cork"
        country = "Ireland"
        address = request.form.get('address')
        loc = geolocator.geocode(address + ','+ city +','+ country)
        mongo.db.locations.insert({'address': request.form.get('address'), 'picture_name': picture.filename, 
        'name': request.form.get('name'),'email': request.form.get('email'), 
        'date' : time.strftime("%Y-%m-%d %H:%M:%S"),"latitude": loc.latitude, "longitude" : loc.longitude})
        return redirect(url_for('locations'))

@app.route('/edit_location/<location_id>')
def edit_location(location_id):
    the_location =  mongo.db.locations.find_one({"_id": ObjectId(location_id)})
    return render_template('editlocation.html', location = the_location)

@app.route('/update_location/<location_id>', methods=["POST"])
def update_location(location_id):
    locations = mongo.db.locations
    locations.update( {'_id': ObjectId(location_id)},
    {
        'name':request.form.get('name'),
        'address':request.form.get('address'),
        'email': request.form.get('email'),
        'picture': request.form.get('picture'),
    })
    return redirect(url_for('locations'))

@app.route('/<picture_name>') 
def picture (picture_name): 
    return mongo.send_file(picture_name)

@app.route('/location_details/<location_id>')
def location_details(location_id):
    the_location_details = mongo.db.locations.find_one({"_id": ObjectId(location_id)})
    address = the_location_details['address']
    name = the_location_details['name']
    date = the_location_details['date']
    src =url_for('picture', picture_name = the_location_details['picture_name'])
    return render_template('location_details.html', src = src, address = address, name = name, date = date)

@app.route('/delete_location/<location_id>')
def delete_location(location_id):
    mongo.db.locations.remove({'_id': ObjectId(location_id)})
    return redirect(url_for('locations'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', '5000')),
            debug=True)