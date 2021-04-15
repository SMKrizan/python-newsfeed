# 'getenv' is part of Python's built-in os model
from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask import g

load_dotenv()

# connect to database using env variable
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
# generates temp connections for performing CRUD operations
Session = sessionmaker(bind=engine)
# maps models to real MySQL tables
Base = declarative_base()

# same method used within seeds.py file, called following initialization - runs whenever a context is destroyed so that connections do not remain open
def init_db(app):
  Base.metadata.create_all(engine)

  app.teardown_appcontext(close_db)

# returns new session-connection saved within g-object, if not already there
def get_db():
  if 'db' not in g:
    # store db connection in app context
    g.db = Session()

  return g.db

# pop() method removes db from the g object, if db exists
def close_db(e=None):
  db = g.pop('db', None)

  if db is not None:
    db.close()
  