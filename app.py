import os
import time
from flask import Flask, render_template, redirect, request, url_for, session, flash, abort
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime, date
import googlemaps


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)


def validate_form(form, form_purpose):
    """ 
    Returns an error list if the data that the user submitted fail validation.
    """

    # variables
    max_username = 20
    max_email = 30
    max_password = 20
    max_home_address = 50
    max_number_of_people = 500
    today = datetime.today()

    error_list = []

    # validate register form
    if form_purpose == 'register':
        valid_date_of_birth = datetime.strptime(
            form['date_of_birth'], '%Y-%m-%d').date()
        if not form['username'] or len(form['username']) > max_username:
            error_list.append(
                'Please enter a username with minimum 1 and maximum 20 characters.'
            )
        if not form['email'] or len(form['email']) > max_email:
            error_list.append(
                'Please enter an email with minimum 1 and maximum 30 characters.'
            )
        if not form['pass'] or len(form['pass']) > max_password:
            error_list.append(
                'Please enter a password with minimum 1 and maximum 20 characters.'
            )
        if not form['home_address'] or len(form['home_address']) > max_home_address:
            error_list.append(
                'Please enter a home address with minimum 1 and maximum 50 characters.'
            )
        if valid_date_of_birth:
            if not (date(1920, 1, 1) <= valid_date_of_birth <= date(2010, 1, 1)):
                error_list.append(
                    'Your date of birth should be between 1/1/1920 and 1/1/2010'
                )
        else:
            error_list.append(
                'Invalid date!'
            )
    # validate form to mark a location cleaned
    if form_purpose == 'mark_cleaned':
        valid_date_of_cleanup = datetime.strptime(
            form['date_of_cleanup'], '%Y-%m-%d').date()
        if not form['number_of_people'] or float(form['number_of_people']) > max_number_of_people:
            error_list.append(
                'Please enter a number of people that participated in the cleanup (min 1, max 500)'
            )
        if valid_date_of_cleanup:
            if not (date(1920, 1, 1) <= valid_date_of_cleanup <= date.today()):
                error_list.append(
                    'The date of cleanup should be between 1/1/2019 and today'
                )
        else:
            error_list.append(
                'Invalid date!'
            )
    # returns error list
    return error_list


@app.route('/')
def index():
    return render_template('index.html', page_title="Home")


@app.route('/about')
def about():
    return render_template('about.html', page_title="About")


@app.route('/locations')
def locations():
    """
    Returns locations.html and documents from a active_locations collection
    in MongoDB.
    """

    return render_template('locations.html',
                           locations=mongo.db.active_locations.find(),
                           page_title="Locations")


@app.route('/location_details/<location_id>')
def location_details(location_id):
    """
    Find the current location by the location_id,
    and set the necessary variables needed for the template (src, name,
    address, date and page title).
    """

    the_location_details = mongo.db.active_locations.find_one(
        {'_id': ObjectId(location_id)})
    if not the_location_details:
        abort(404)
    src = url_for('picture', picture_name=the_location_details['picture_name'])
    address = the_location_details['address_of_location']
    name = the_location_details['uploaded_by']
    date = the_location_details['date']

    return render_template('location_details.html', src=src, address=address,
                           name=name, date=date, location_id=location_id,
                           page_title="Location Details")


@app.route('/<picture_name>')
def picture(picture_name):
    """
    Retrieve the image stored in the MongoDB GridFS.
    """

    return mongo.send_file(picture_name)


@app.route('/mark_location_cleaned/<location_id>', methods=['GET'])
def mark_location_cleaned(location_id):
    """
    If the user is logged in, find the current location by the location_id,
    render template mark_location_cleaned.html
    and set the necessary variable needed for the template (location and
    page title).

    If the user is not logged in, redirect to login.html and save the url
    in session to bring the user back after the login.
    """
    if 'username' in session:
        the_location = mongo.db.active_locations.find_one(
            {'_id': ObjectId(location_id)})
        if not the_location:
            abort(404)
        return render_template('mark_location_cleaned.html',
                               location=the_location,
                               page_title="Mark as cleaned")
    session['url'] = url_for('mark_location_cleaned', location_id=location_id)
    return redirect(url_for('login_page'))


@app.route('/update_location/<location_id>', methods=['POST'])
def update_location(location_id):
    """
    In case there is no errors:
    If the user is logged in, find the current location by the location_id,
    update the location with the new information from the form.
    The information not gathered in the form remain the same.

    If the user is not logged in, redirect to login.html.

    If there is errors, return mark_location_cleaned.html and
    list the errors.
    """
    error_list = validate_form(request.form, 'mark_cleaned')
    if error_list == []:
        if 'username' in session:
            location = mongo.db.active_locations.find_one(
                {'_id': ObjectId(location_id)})
            if not location:
                abort(404)
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
            return redirect(url_for('cleaned_location_details',
                                    location_id=location_id))
        return redirect(url_for('login_page'))
    else:
        the_location = mongo.db.active_locations.find_one(
            {'_id': ObjectId(location_id)})
        return render_template('mark_location_cleaned.html',
                               page_title="Register", location=the_location,
                               errors=error_list)


@app.route('/cleaned_locations')
def cleaned_locations():
    """
    Returns cleaned_locations.html and documents from active_locations
    collection in MongoDB.
    """

    return render_template('cleaned_locations.html',
                           locations=mongo.db.active_locations.find(),
                           page_title="Cleaned locations")


@app.route('/cleaned_location_details/<location_id>')
def cleaned_location_details(location_id):
    """
    Find the current location by the location_id, and set the necessary
    variables needed for the template
    (src, src_cleaned, address, name, date, number of people and
    page title).
    """

    the_location_details = mongo.db.active_locations.find_one(
        {'_id': ObjectId(location_id)})
    if not the_location_details:
        abort(404)
    src = url_for('picture', picture_name=the_location_details['picture_name'])
    src_cleaned = url_for(
        'picture', picture_name=the_location_details['cleaned_picture_name'])
    address = the_location_details['address_of_location']
    name = the_location_details['uploaded_by']
    date = the_location_details['date_of_cleanup']
    number_of_people = the_location_details['number_of_people']

    return render_template('cleaned_location_details.html', src=src,
                           src_cleaned=src_cleaned,
                           address=address, name=name, date=date,
                           number_of_people=number_of_people,
                           page_title="Location details")


@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('register.html', page_title="Register")


@app.route('/register_update', methods=['POST'])
def register_update():
    """
    In case there is no errors:
    Search for username in users collection.

    If the username doesn't exsist, insert the information from the form.

    If the username already exists flash an error message.

    If there is errors, return register.html and
    list the errors.
    """
    error_list = validate_form(request.form, 'register')

    if error_list == []:
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
                return redirect(url_for('profile_page'))

            flash('That username already exists!')

        return render_template('register.html', page_title="Register")
    else:
        return render_template('register.html', page_title="Register",
                               errors=error_list)


@app.route('/login_page')
def login_page():
    return render_template('login.html', page_title="Log in")


@app.route('/login', methods=['POST'])
def login():
    """
    Search for the username in users collection.

    If the username exsist, check if the password is correct.
    Return a url stored in session.
    If there is none return profile.html and documents from a
    active_locations collection in MongoDB.

    If the username doesn't exist or the password is incorrect
    flash an error message.
    """

    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if request.form['pass'] == login_user['password']:
            session['username'] = request.form['username']
            if 'url' in session:
                return redirect(session['url'])
            return render_template('profile.html',
                                   locations=mongo.db.active_locations.find(),
                                   page_title="Profile")

    flash('Invalid username/password combination')
    return redirect(url_for('login_page'))


@app.route('/profile_page')
def profile_page():
    """
    If the user is logged in, returns profile.html and documents
    from a active_locations collection in MongoDB.

    If the user is not logged in, redirect to login.html.
    """

    if 'username' in session:
        return render_template('profile.html',
                               locations=mongo.db.active_locations.find(),
                               page_title="Profile")
    return redirect(url_for('login_page'))


@app.route('/profile_edit_location/<location_id>')
def profile_edit_location(location_id):
    """
    If the user is logged in, find the current location by the location_id,
    and set the necessary variables needed for the template (location and
    page title).

    If the user is not logged in, redirect to login.html.
    """

    if 'username' in session:
        the_location_details = mongo.db.active_locations.find_one(
            {'_id': ObjectId(location_id)})
        if not the_location_details:
            abort(404)
        return render_template('profile_edit_location.html',
                               location=the_location_details,
                               page_title="Edit location")

    return redirect(url_for('login_page'))


@app.route('/profile_update_location/<location_id>', methods=['POST', 'GET'])
def profile_update_location(location_id):
    """
    If the user is logged in, find the current location by the location_id,
    update the location with the new information from the form.
    The information not gathered in the form remain the same.

    If the user is not logged in, redirect to login.html.
    """

    if 'username' in session:
        location = mongo.db.active_locations.find_one(
            {'_id': ObjectId(location_id)})
        if not location:
            abort(404)
        locations = mongo.db.active_locations
        # use Geocoding to determine latitude and longitude
        gmaps = googlemaps.Client(key=os.environ.get('API_KEY'))
        address = request.form.get('address')
        geocode_result = gmaps.geocode(address)
        # make sure the user entered a valid address
        if geocode_result:
            latitude = geocode_result[0]["geometry"]["location"]["lat"]
            longitude  = geocode_result[0]["geometry"]["location"]["lng"]
            # make sure the user entered an address in Cork City
            if 51.86 <= latitude <= 51.92 and -8.54 <= longitude <= -8.41:
                locations.update({'_id': ObjectId(location_id)},
                                 {'status': location['status'],
                                  'address_of_location': request.form.get('address'),
                                  'picture_name': location['picture_name'],
                                  'uploaded_by':  session['username'],
                                  'date': time.strftime("%Y-%m-%d %H:%M:%S"),
                                  'latitude_of_location': latitude,
                                  'longitude_of_location': longitude
                                  })
                src = url_for('picture', picture_name=location['picture_name'])
                return render_template('profile_edit_picture.html',
                                       location=location,
                                       location_id=location_id,
                                       src=src, page_title="Edit location")

            flash('Address you have entered is outside of Cork City')
            return redirect(url_for('profile_edit_location',
                                    location_id=location_id))

        flash('Invalid address')
        return redirect(url_for('profile_edit_location', location_id=location_id))
    return redirect(url_for('login_page'))


@app.route('/profile_update_picture/<location_id>', methods=['POST'])
def profile_update_picture(location_id):
    """
    If the user is logged in, find the current location by the location_id,
    update the location with the new information from the form.
    The information not gathered in the form remain the same.

    If the user is not logged in, redirect to login.html.
    """

    if 'username' in session:
        location = mongo.db.active_locations.find_one(
            {'_id': ObjectId(location_id)})
        if not location:
            abort(404)
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

        return redirect(url_for('location_details',
                                location_id=location_id))
    return redirect(url_for('login_page'))


@app.route('/events')
def events():
    """
    Returns events.html and documents from a active_locations collection
    in MongoDB.
    """

    return render_template('events.html',
                           locations=mongo.db.active_locations.find(),
                           page_title="Events")


@app.route('/delete_location/<location_id>')
def delete_location(location_id):
    """
    If the user is logged in, find the current location by the location_id,
    render template delete_location.html and set the necessary variable
    needed for the template (location and page title).

    If the user is not logged in, redirect to login.html.
    """

    if 'username' in session:
        the_location = mongo.db.active_locations.find_one(
            {'_id': ObjectId(location_id)})
        if not the_location:
            abort(404)
        return render_template('delete_location.html', location=the_location,
                               page_title="Delete location")
    return redirect(url_for('login_page'))


@app.route('/delete_location_update/<location_id>', methods=['POST'])
def delete_location_update(location_id):
    """
    If the user is logged in, find the current location by the location_id,
    update the location with the new information from the form.
    The information not gathered in the form remain the same.

    Insert the document in deleted_locations collection. Remove the document
    from active_locations collection.

    If the user is not logged in, redirect to login.html.
    """

    if 'username' in session:
        the_location = mongo.db.active_locations.find_one(
            {'_id': ObjectId(location_id)})
        if not the_location:
            abort(404)
        mongo.db.deleted_locations.insert(
            {'_id': ObjectId(location_id),
             'address': the_location['address_of_location'],
             'reason_for_deleting': request.form.get('reason'),
             'deleted_by': session['username'],
             'date': time.strftime("%Y-%m-%d %H:%M:%S"),
             })
        mongo.db.active_locations.remove(the_location)
        return redirect(url_for('locations'))
    return redirect(url_for('login_page'))


@app.route('/insert_location', methods=['POST'])
def insert_location():
    """
    If the user is logged in and inputs an address:

        1. Check if the address is valid.

        2. Check the address is in Cork City.

        3. Check if the address is already in the database.

        4. Insert the data to the database.

    If the user is not logged in, redirect to login.html.
    """

    if 'username' in session:
        if 'picture' in request.files:
            picture = request.files['picture']
            mongo.save_file(picture.filename, picture)
            # use Geocoding to determine latitude and longitude
            gmaps = googlemaps.Client(key=os.environ.get('API_KEY'))
            address = request.form.get('address')
            geocode_result = gmaps.geocode(address)
            # make sure the user entered a valid address
            if geocode_result:
                latitude = geocode_result[0]["geometry"]["location"]["lat"]
                longitude  = geocode_result[0]["geometry"]["location"]["lng"]
                # make sure the user entered an address in Cork City
                if 51.86 <= latitude <= 51.92 and -8.54 <= longitude <= -8.41:
                    # make sure the adress is not laready in the database
                    same_location = 0
                    for i in mongo.db.active_locations.find():
                        if i['latitude_of_location'] == latitude and i['longitude_of_location'] == longitude:
                            same_location += 1
                    if same_location > 0:
                        flash('This address already exists')
                        return redirect(url_for('locations'))
                    date = time.strftime("%Y-%m-%d %H:%M:%S")
                    name = session['username']
                    mongo.db.active_locations.insert({
                        'status': 'not_cleaned',
                        'address_of_location': address,
                        'picture_name': picture.filename,
                        'uploaded_by': name,
                        'date': date,
                        'latitude_of_location': latitude,
                        'longitude_of_location': longitude
                    })
                    loc = mongo.db.active_locations.find_one({
                        "address_of_location": address
                    })
                    location_id = loc.get('_id')
                    return redirect(url_for('location_details',
                                            location_id=location_id,
                                            date=date,
                                            address=address,
                                            name=name))
                flash('Address you have entered is outside of Cork City')
                return redirect(url_for('locations'))

            flash('Invalid address')
            return redirect(url_for('locations'))
    return redirect(url_for('login_page'))


@app.route('/logout')
def logout():
    """
    Log out the user, redirect to index.html.
    """
    session.pop('username', None)
    return redirect('/')


@app.errorhandler(404)
def page_not_found(error):
    """
    Return a 404 error.
    """
    return render_template('404.html', page_titl='404'), 404


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', '5000')),
            debug=True)
