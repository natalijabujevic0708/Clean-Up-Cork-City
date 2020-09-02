import os
import time
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from geopy.geocoders import Nominatim

app = Flask(__name__)
mongo = PyMongo(app)


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
    return render_template("locations.html", locations=mongo.db.locations.find({"status":"active"}))


@app.route('/insert_location', methods=['POST'])  # form on locations.html
def insert_location():
    if 'picture' in request.files:
        picture = request.files['picture']
        mongo.save_file(picture.filename, picture)
        # using geolocator to determine latitude and longitude
        geolocator = Nominatim(user_agent="natalijabujevic0708@gmail.com")
        address = request.form.get('address')
        loc = geolocator.geocode(address)
        # inserting data in the MongoDB
        mongo.db.locations.insert({
            'status' : 'active',
            'address': address,
            'picture_name': picture.filename,
            'uploaded_by': request.form.get('name'),
            'email': request.form.get('email'),
            'date': time.strftime("%Y-%m-%d %H:%M:%S"),
            'latitude_of_location': loc.latitude,
            'longitude_of_location': loc.longitude
            })
        return redirect(url_for('locations'))

# options under every location - more details, edit or delete location
@app.route('/<picture_name>')  # to render the picture from MongoDB
def picture(picture_name):
    return mongo.send_file(picture_name)

@app.route('/location_details/<location_id>')
def location_details(location_id):
    the_location_details = mongo.db.locations.find_one(
        {"_id": ObjectId(location_id)})
    address = the_location_details['address']
    name = the_location_details['uploaded_by']
    date = the_location_details['date']
    src = url_for('picture', picture_name=the_location_details['picture_name'])
    return render_template('location_details.html', src=src, address=address, name=name, date=date)


@app.route('/edit_location/<location_id>')
def edit_location(location_id):
    the_location = mongo.db.locations.find_one({"_id": ObjectId(location_id)})
    return render_template('edit_location.html', location=the_location)


@app.route('/update_location/<location_id>', methods=["POST"])
def update_location(location_id):
    locations = mongo.db.locations
    # using geolocator to determine latitude and longitude
    geolocator = Nominatim(user_agent="natalijabujevic0708@gmail.com")
    address = request.form.get('address')
    loc = geolocator.geocode(address)
    locations.update({'_id': ObjectId(location_id)},
    {   'status' : 'active',
        'address_of_location': address,
        'picture_name': request.form.get('picture'),
        'uploaded_by': request.form.get('name'),
        'email': request.form.get('email'),
        'date': time.strftime("%Y-%m-%d %H:%M:%S"),
        'latitude_of_location': loc.latitude,
        'longitude_of_location': loc.longitude
        })
    return redirect(url_for('locations'))

@app.route('/delete_location/<location_id>')
def delete_location(location_id):
    the_location = mongo.db.locations.find_one({"_id": ObjectId(location_id)})
    return render_template('delete_location.html', location=the_location)

@app.route('/delete_location_update/<location_id>', methods=["POST"])
def delete_location_update(location_id):
    locations = mongo.db.locations
    # using geolocator to determine latitude and longitude
    geolocator = Nominatim(user_agent="natalijabujevic0708@gmail.com")
    address = request.form.get('address')
    loc = geolocator.geocode(address)
    locations.update({'_id': ObjectId(location_id)},
    {   'status' : 'deleted',
        'address': address,
        'reason_for_deleting': request.form.get('reason'),
        'deleted_by': request.form.get('name'),
        'email': request.form.get('email'),
        'date': time.strftime("%Y-%m-%d %H:%M:%S"),
        'latitude_of_location': loc.latitude,
        'longitude_of_location': loc.longitude
        })
    return redirect(url_for('locations'))


if __name__ == '__main__':
    app.run(host = os.environ.get('IP'),
            port = int(os.environ.get('PORT', '5000')),
            debug = True)
