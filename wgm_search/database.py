"Database routines for wgm_search"

import sqlite3
from contextlib import closing
from wgm_search import app, g

def connect_db():
    "Connect to database specified in config"

    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    "Initializes databse with scheme.sql"
    
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
