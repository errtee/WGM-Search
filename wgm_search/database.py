"Database routines for wgm_search"

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from wgm_search import app

engine = create_engine(app.config['DATABASE'], convert_unicode=True)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
    autoflush=False,
    bind=engine))

def init_db():
    "Initializes databse with scheme.sql"
    import wgm_search.models
    metadata.create_all(bind=engine)
