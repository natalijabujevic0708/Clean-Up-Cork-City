import os
from flask import Flask


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
    locations = mongo.db.locations
    locations.insert_one(request.form.to_dict())
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

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', '5000')),
            debug=True)