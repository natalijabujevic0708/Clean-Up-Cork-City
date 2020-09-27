import os
import time
from flask import Flask, render_template, redirect, request, url_for, session, flash
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

@app.route('/<picture_name>')
def picture(picture_name):
    return mongo.send_file(picture_name)

# more details about the location

@app.route('/events')
def events():
    """
    Returns locations.html and documents from a active_locations collection in MongoDB.
    """

    return render_template('events.html', locations=mongo.db.active_locations.find())


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
    if 'username' in session:
        the_location = mongo.db.active_locations.find_one(
            {"_id": ObjectId(location_id)})
        return render_template('edit_location.html', location=the_location)
    return render_template('login.html')

# to update a location

@app.route('/update_location/<location_id>', methods=['POST'])
def update_location(location_id):
    location = mongo.db.active_locations.find_one(
        {"_id": ObjectId(location_id)})
    locations = mongo.db.active_locations
    picture = request.files['picture']
    mongo.save_file(picture.filename, picture)
    locations.update({'_id': ObjectId(location_id)},
                     {'status': 'cleaned',
                      'address_of_location': location['address_of_location'],
                      'picture_name': location['picture_name'],
                      'cleaned_picture_name': picture.filename,
                      'uploaded_by':  session['username'],
                      'date_of_cleanup': request.form.get('date_of_cleanup'),
                      'number_of_people': request.form.get('number_of_people'),
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

# to delete a location

@app.route('/delete_location_update/<location_id>', methods=['POST'])
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

# cleaned_locations.html

@app.route('/cleaned_locations')
def cleaned_locations():
    return render_template("cleaned_locations.html", locations=mongo.db.active_locations.find())


@app.route('/cleaned_location_details/<location_id>')
def cleaned_location_details(location_id):
<<<<<<< HEAD
=======
    """
    Find the current location by the location_id, and set the necessary variables needed for the template (src, src_cleaned, address, name, date and
    number of people).
    """
<<<<<<< HEAD
    
>>>>>>> d95e7c1... Add key:value pair number_of_people
=======

>>>>>>> 2937988... Check if the input address is valid
    the_location_details = mongo.db.active_locations.find_one(
        {"_id": ObjectId(location_id)})
    address = the_location_details['address_of_location']
    name = the_location_details['uploaded_by']
<<<<<<< HEAD
    date = the_location_details['date_of_clenup']
    src = url_for('picture', picture_name=the_location_details['picture_name'])
    src_cleaned = url_for(
        'picture', picture_name=the_location_details['cleaned_picture_name'])
    return render_template('cleaned_location_details.html', src=src, src_cleaned=src_cleaned, address=address, name=name, date=date)
=======
    date = the_location_details['date_of_cleanup']
    number_of_people = the_location_details['number_of_people']
<<<<<<< HEAD
    
    return render_template('cleaned_location_details.html', src=src, src_cleaned=src_cleaned, address=address, name=name, date=date, number_of_people = number_of_people)
>>>>>>> d95e7c1... Add key:value pair number_of_people

# register.html
=======

    return render_template('cleaned_location_details.html', src=src, src_cleaned=src_cleaned, address=address, name=name, date=date, number_of_people=number_of_people)
>>>>>>> 2937988... Check if the input address is valid


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
            return render_template('profile.html', locations=mongo.db.active_locations.find())

    flash("Invalid username/password combination")
    return render_template('login.html')

# profile.html

@app.route('/profile_page')
def profile_page():
    if 'username' in session:
        return render_template('profile.html', locations=mongo.db.active_locations.find())
    return render_template('login.html')


@app.route('/profile_edit_location/<location_id>')
def profile_edit_location(location_id):
    the_location_details = mongo.db.active_locations.find_one(
<<<<<<< HEAD
        {"_id": ObjectId(location_id)})
    src = url_for('picture', picture_name=the_location_details['picture_name'])
    return render_template('profile_edit_location.html', location=the_location_details,  src=src)

@app.route('/profile_edit_locationandpicture/<location_id>')
def profile_edit_locationandpicture(location_id):
    the_location_details = mongo.db.active_locations.find_one(
        {"_id": ObjectId(location_id)})
    return render_template('profile_edit_location+picture.html', location=the_location_details)


@app.route('/profile_update_location/<location_id>', methods=["POST"])
=======
        {'_id': ObjectId(location_id)})

    return render_template('profile_edit_location.html', location=the_location_details)


@app.route('/profile_update_location/<location_id>', methods=['POST', 'GET'])
>>>>>>> 2937988... Check if the input address is valid
def profile_update_location(location_id):
    location = mongo.db.active_locations.find_one(
<<<<<<< HEAD
        {"_id": ObjectId(location_id)})
    locations = mongo.db.active_locations
    locations.update({'_id': ObjectId(location_id)},
                     {'status': location['status'],
                      'address_of_location': request.form.get('address'),
                      'picture_name': location['picture_name'],
                      'uploaded_by':  session['username'],
                      'date': time.strftime("%Y-%m-%d %H:%M:%S"),
                      'latitude_of_location': location['latitude_of_location'],
                      'longitude_of_location': location['longitude_of_location'],
                      })
    return render_template('profile.html', locations=mongo.db.active_locations.find())


@app.route('/profile_update_locationandpicture/<location_id>', methods=["POST"])
def profile_update_locationandpicture(location_id):
=======
        {'_id': ObjectId(location_id)})

    # using geolocator to determine latitude and longitude
    locations = mongo.db.active_locations
    geolocator = Nominatim(user_agent='http://127.0.0.1:5000/locations')
    address = request.form.get('address')
    loc = geolocator.geocode(address)

    # make sure the user entered a valid address
    if loc: 
        # make sure the user entered an address in Cork City
        if 51.86 <= loc.latitude <= 51.92 and -8.54 <= loc.longitude <= -8.41:
            locations.update({'_id': ObjectId(location_id)},
                                {'status': location['status'],
                                'address_of_location': request.form.get('address'),
                                'picture_name': location['picture_name'],
                                'uploaded_by':  session['username'],
                                'date': time.strftime("%Y-%m-%d %H:%M:%S"),
                                'latitude_of_location': loc.latitude,
                                'longitude_of_location': loc.longitude
                                })
            src = url_for('picture', picture_name=location['picture_name'])
            return render_template('profile_edit_picture.html', location=location, location_id=location_id, src=src)

        flash('Address you have entered is outside of Cork City')
        return render_template('profile_edit_location.html',  location_id=location_id, location=location)

    flash('Invalid address')
    return render_template('profile_edit_location.html',  location_id=location_id, location=location)
    


@app.route('/profile_update_picture/<location_id>', methods=['POST'])
def profile_update_picture(location_id):
    """
    Find the current location by the location_id, update the location with the new information from the form.
    The information not gathered in the form remain the same. 
    """

>>>>>>> 2937988... Check if the input address is valid
    location = mongo.db.active_locations.find_one(
        {"_id": ObjectId(location_id)})
    locations = mongo.db.active_locations
    picture = request.files['picture']
    mongo.save_file(picture.filename, picture)
    locations = mongo.db.active_locations
    locations.update({'_id': ObjectId(location_id)},
                     {'status': location['status'],
                      'address_of_location': location['address_of_location'],
                      'picture_name':  picture.filename,
                      'uploaded_by':  session['username'],
                      'date': time.strftime("%Y-%m-%d %H:%M:%S"),
                      'latitude_of_location': location['latitude_of_location'],
                      'longitude_of_location': location['longitude_of_location'],
                      })

    return render_template('profile.html', locations=mongo.db.active_locations.find())


<<<<<<< HEAD
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
=======
@app.route('/insert_location', methods=['POST'])
def insert_location():
    """
    When a user inputs an address:

        1. Check if the address is valid.

        2. Check the address is in Cork City.

        3. Check if the address is already in the database.

        4. Insert the data to the database.

    """
    if 'picture' in request.files:
        picture = request.files['picture']
        mongo.save_file(picture.filename, picture)
        # use geolocator to determine latitude and longitude
        geolocator = Nominatim(user_agent='http://127.0.0.1:5000/locations')
        address = request.form.get('address')
        loc = geolocator.geocode(address)
        # make sure the user entered a valid address
        if loc: 
            # make sure the user entered an address in Cork City
            if 51.86 <= loc.latitude <= 51.92 and -8.54 <= loc.longitude <= -8.41:
                # make sure the database is not empty
                if mongo.db.active_locations.find().count() > 0:
                    # make sure the adress is not laready in the database
                    for i in mongo.db.active_locations.find():
                        if i['latitude_of_location'] != loc.latitude or i['longitude_of_location'] != loc.longitude:
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
                        
                        flash('This address already exists')
                        return redirect(url_for('locations'))

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

            flash('Address you have entered is outside of Cork City')
            return redirect(url_for('locations'))

        flash('Invalid address')
        return redirect(url_for('locations'))
>>>>>>> 2937988... Check if the input address is valid

<<<<<<< HEAD
<<<<<<< HEAD
    

>>>>>>> e4f685d... Deleted the contact route, modified the key value pairs for edit and insert location (created a key status), added flash messages for invalid login
=======
>>>>>>> b80accd... Create new routes -  cleaned_location_details, profile_edit_location,   profile_edit_locationandpicture, profile_update_location, profile_update_locationandpicture
=======
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

>>>>>>> 75dd38f... Create log out option

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', '5000')),
            debug=True)
