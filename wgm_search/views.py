"Flask views for wgm_search"

from wgm_search import app
from wgm_search.database import connect_db, init_db, query_db
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
import pygeodb
from wgm_search.forms import SearchForm, CitySearchForm, DistanceSearchForm

# Show a full list of entries (no search)
@app.route('/list')
def show_entries():
    "Show full list of database entries, rendered through show_entries.html template"

    entries = query_db('select name, zip, city from entries order by id desc')
    return render_template('show_entries.html', entries=entries)

@app.route('/', methods=['GET', 'POST'])
def distance_search_entry():
    "Search entries, via ZIP/distance (geodb), form template is template/search.html, rendering is done by show_entries.html"

    form = DistanceSearchForm(request.form)
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

    return render_template('distancesearch.html', form=form)

@app.route('/citysearch', methods=['GET', 'POST'])
def city_search_entry():
    "Search entries, via ZIP/City, form template is template/search.html, rendering is done by show_entries.html"

    form = CitySearchForm(request.form)
    if request.method == 'POST' and form.validate():
        search_zip = str(form.zip.data)
        search_city = str(form.city.data)

        entries = query_db('select name,zip,city from entries where zip like ? and city like ?', [search_zip + '%', search_city + '%'])
        return render_template('show_entries.html', entries=entries)

    return render_template('citysearch.html', form=form)
