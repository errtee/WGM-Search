"Database routines for wgm_search"

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from wgm_search import app

engine = create_engine(app.config['DATABASE'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
    autoflush=False,
    bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    "Initializes databse with scheme.sql"
    import wgm_search.models
    Base.metadata.create_all(bind=engine)
