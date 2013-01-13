#!/usr/bin/env python
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
import pygeodb
from wtforms import Form, BooleanField, TextField, SelectField, SubmitField, validators, ValidationError

# configuration
DATABASE = 'wgm.db'
DEBUG = True
SECRET_KEY = 'foobar'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as file:
            db.cursor().executescript(file.read())
        db.commit()

def query_db(query, args=(), one=False):
    "Do database query and convert the result into a dict"

    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
        for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


@app.before_request
def before_request():
    "Connect to database on request"
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    "Close database connection after request"
    g.db.close()

# Show a full list of entries (no search)
@app.route('/list')
def show_entries():
    "Show full list of database entries, rendered through show_entries.html template"

    entries = query_db('select name, zip, city from entries order by id desc')
    return render_template('show_entries.html', entries=entries)

def zip_exists(message=None):
    "Validates that a zip exists"

    def _zip_exists(form, field):
        z = field.data
        if not z in pygeodb.geodata['DE']:
            raise ValidationError(message)

    return _zip_exists


distance_choices = [(5, "5km"), (10, "10km"), (15, "15km"), (20, "20km"), (30, "30km"), (40, "40km"), (50, "50km")]
distance_values = [distance[0] for distance in distance_choices]
class SearchForm(Form):
    zip     = TextField(u'Postleitzahl', [validators.Length(min=5, max=5, message=u'Postleitzahlen muessen 5 Ziffern enthalten'),
        zip_exists(u'Postleitzahl existiert nicht! Bitte geben Sie eine existierende PLZ ein.')])
    distance    = SelectField(u'Entfernung', coerce=int, choices=distance_choices, validators=[validators.AnyOf(values=distance_values, message=u'Please select one of the given options')])
    submit  = SubmitField(u'Search')


@app.route('/', methods=['GET', 'POST'])
def search_entry():
    "Search entries, either via ZIP/City or ZIP/distance (geodb), form template is template/search.html, rendering is done by show_entries.html"

    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        search_zip = str(form.zip.data)
        search_distance = int(form.distance.data) *1000

        # Get alle ZIPs from database
        zip_list = query_db('select zip from entries order by zip')

        # Create simple list of ZIPs that we can hand over to pygeodb.distances
        zips = []
        for zip_dict in zip_list:
            zips.append(str(zip_dict['zip']))

        # Get sorted ZIP list and distance to queried ZIP
        distances = pygeodb.distances(search_zip, zips)

        # Limit list of ZIPs we query the database for to the desired distance
        close_zips = []
        zip_distance = {}
        for distance_plz_tuple in distances:
            if distance_plz_tuple[0] <= search_distance:
                close_zips.append(distance_plz_tuple[1])
                zip_distance[distance_plz_tuple[1]] = distance_plz_tuple[0]

        entries = []
        for close_zip in close_zips:
            entries.extend(query_db('select name,zip,city from entries where zip=?', [close_zip]))

        for entry in entries:
            entry['distance'] = zip_distance[str(entry['zip'])]
        return render_template('show_entries.html', entries=entries)

    return render_template('search.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
