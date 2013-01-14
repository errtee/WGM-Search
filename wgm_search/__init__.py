#!/usr/bin/env python
"Simple web frontend that allows searching an exported CiviCRM database for wirgehenmit.org"

from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
from wtforms import Form, BooleanField, TextField, SelectField, SubmitField, validators, ValidationError

# create our little application :)
app = Flask(__name__)

import wgm_search.views
from wgm_search.database import connect_db, init_db, query_db

# Load default config from config file and optionally from a file
# pointed to bei WGMSEARCH_SETTING in the environment
app.config.from_object('wgm_search.config')
app.config.from_envvar('WGMSEARCH_SETTING',silent=True)

@app.before_request
def before_request():
    "Connect to database on request"
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    "Close database connection after request"
    g.db.close()

if __name__ == '__main__':
    app.run(debug=True)
