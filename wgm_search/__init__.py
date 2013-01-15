#!/usr/bin/env python
"Simple web frontend that allows searching an exported CiviCRM database for wirgehenmit.org"

import os
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
from wtforms import Form, BooleanField, TextField, SelectField, SubmitField, validators, ValidationError

# create our little application :)
app = Flask(__name__)

# Load default config from config file and optionally from a file
# pointed to bei WGMSEARCH_SETTING in the environment
if 'WGMDEVELOPMENT' in os.environ:
    app.config.from_object('wgm_search.config.DevelopmentConfig')
elif 'WGMTESTING' in os.environ:
    app.config.from_object('wgm_search.config.TestingConfig')
else:
    app.config.from_object('wgm_search.config.ProductionConfig')
app.config.from_envvar('WGMSEARCH_SETTING',silent=True)

import wgm_search.views
from wgm_search.database import db_session, init_db

@app.teardown_request
def teardown_request(exception=None):
    "Close database connection after request"
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)
