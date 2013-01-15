from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper
from wgm_search.database import metadata, db_session

class Mitlaeufer(object):
    query = db_session.query_property()

    def __init__(self, name=None, zip=None, city=None):
        self.name = name
        self.zip = zip
        self.city = city

    def __repr__(self):
        return '<Mitlaeufer %r>' % (self.name)

mitlaeufer = Table('entries', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), unique=True),
    Column('zip', String(5)),
    Column('city', String(255))
)

mapper(Mitlaeufer, mitlaeufer)
