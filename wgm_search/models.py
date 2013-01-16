from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper
from wgm_search.database import Base

class Mitlaeufer(Base):
    __tablename__ = 'entries'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(50))
    zip = Column('zip', String(5))
    city = Column('city', String(50))

    def __init__(self, name=None, zip=None, city=None):
        self.name = name
        self.zip = zip
        self.city = city

    def __repr__(self):
        return '<Mitlaeufer %r>' % (self.name)
