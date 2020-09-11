import os
import time
<<<<<<< HEAD
from flask import Flask, render_template, redirect, request, url_for
=======
from flask import Flask, render_template, redirect, request, url_for, session, flash
>>>>>>> e4f685d... Deleted the contact route, modified the key value pairs for edit and insert location (created a key status), added flash messages for invalid login
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from geopy.geocoders import Nominatim

app = Flask(__name__)
mongo = PyMongo(app)

# index.html


@app.route('/')
def index():
    return render_template("index.html")


# about.html


@app.route('/about')
def about():
    return render_template("about.html")

# locations.html


@app.route('/locations')
def locations():
    return render_template("locations.html", locations=mongo.db.locations.find({"status":"active"}))

# to render the picture from MongoDB

<<<<<<< HEAD
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
=======
>>>>>>> e4f685d... Deleted the contact route, modified the key value pairs for edit and insert location (created a key status), added flash messages for invalid login

@app.route('/<picture_name>')
def picture(picture_name):
    return mongo.send_file(picture_name)

# more details about the location


@app.route('/location_details/<location_id>')
def location_details(location_id):
    the_location_details = mongo.db.locations.find_one(
        {"_id": ObjectId(location_id)})
    address = the_location_details['address']
    name = the_location_details['uploaded_by']
    date = the_location_details['date']
    src = url_for('picture', picture_name=the_location_details['picture_name'])
    return render_template('location_details.html', src=src, address=address, name=name, date=date)

# edit_location.html


@app.route('/edit_location/<location_id>')
def edit_location(location_id):
<<<<<<< HEAD
    the_location = mongo.db.locations.find_one({"_id": ObjectId(location_id)})
    return render_template('edit_location.html', location=the_location)
=======
    if 'username' in session:
        the_location = mongo.db.active_locations.find_one(
            {"_id": ObjectId(location_id)})
        return render_template('edit_location.html', location=the_location)
    return render_template('login.html')

# to update a location
>>>>>>> e4f685d... Deleted the contact route, modified the key value pairs for edit and insert location (created a key status), added flash messages for invalid login


@app.route('/update_location/<location_id>', methods=["POST"])
def update_location(location_id):
<<<<<<< HEAD
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
=======
    location = mongo.db.active_locations.find_one(
        {"_id": ObjectId(location_id)})
    locations = mongo.db.active_locations
    locations.update({'_id': ObjectId(location_id)},
                     {'status': 'cleaned',
                      'address_of_location': location['address_of_location'],
                      'picture_name': location['picture_name'],
                      'cleaned_picture_name': request.form.get('picture'),
                      'uploaded_by':  session['username'],
                      'date_of_clenup': request.form.get('date_of_cleanup'),
                      'latitude_of_location': location['latitude_of_location'],
                      'longitude_of_location': location['longitude_of_location'],
                      })
    return redirect(url_for('cleaned_locations'))

# delete_location.html


@app.route('/delete_location/<location_id>')
def delete_location(location_id):
    if 'username' in session:
        the_location = mongo.db.active_locations.find_one(
            {"_id": ObjectId(location_id)})
        return render_template('delete_location.html', location=the_location)
    return render_template('login.html')
>>>>>>> e4f685d... Deleted the contact route, modified the key value pairs for edit and insert location (created a key status), added flash messages for invalid login

# to delete a location


@app.route('/delete_location_update/<location_id>', methods=["POST"])
def delete_location_update(location_id):
<<<<<<< HEAD
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

=======
    the_location = mongo.db.active_locations.find_one(
        {"_id": ObjectId(location_id)})
    address = the_location['address_of_location']
    # Adding to the delted_locations collection in MongoDB
    mongo.db.deleted_locations.insert(
        {'_id': ObjectId(location_id),
         'address': address,
         'reason_for_deleting': request.form.get('reason'),
         'deleted_by': session['username'],
         'date': time.strftime("%Y-%m-%d %H:%M:%S"),
         })
    mongo.db.active_locations.remove(the_location)
    return redirect(url_for('locations'))

# clened_locations.html


@app.route('/cleaned_locations')
def cleaned_locations():
    return render_template("cleaned_locations.html", locations=mongo.db.active_locations.find())

# register.html


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            users.insert({
                'name': request.form['username'],
                'email': request.form['email'],
                'password': request.form['pass'],
                'home_address': request.form['home_address'],
                'date_of_birth': request.form['date_of_birth']
            })
            session['username'] = request.form['username']
            return render_template('profile.html')

        flash('That username already exists!')

    return render_template('register.html')


# login.html
@app.route('/login_page')
def login_page():
    return render_template('login.html')

# to log in


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if request.form['pass'] == login_user['password']:
            session['username'] = request.form['username']
            return render_template('profile.html')

    flash("Invalid username/password combination")
    return render_template('login.html')

# profile.html


@app.route('/profile_page')
def profile_page():
    if 'username' in session:
        return render_template('profile.html')
    return render_template('login.html')

# to insert a location on locations.html


@app.route('/insert_location', methods=['POST'])
def insert_location():
    if 'username' in session:
        if 'picture' in request.files:
            picture = request.files['picture']
            mongo.save_file(picture.filename, picture)
            # using geolocator to determine latitude and longitude
            geolocator = Nominatim(user_agent="natalijabujevic0708@gmail.com")
            address = request.form.get('address')
            loc = geolocator.geocode(address)
            # inserting data in the MongoDB
            mongo.db.active_locations.insert({
                'status': 'not_cleaned',
                'address_of_location': address,
                'picture_name': picture.filename,
                'uploaded_by': session['username'],
                'date': time.strftime("%Y-%m-%d %H:%M:%S"),
                'latitude_of_location': loc.latitude,
                'longitude_of_location': loc.longitude
            })
            return redirect(url_for('locations'))
    flash("Please log in to add a location")
    return redirect(url_for('locations'))

    

>>>>>>> e4f685d... Deleted the contact route, modified the key value pairs for edit and insert location (created a key status), added flash messages for invalid login

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', '5000')),
            debug=True)
