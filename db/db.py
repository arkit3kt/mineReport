import sqlite3, sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from db.tables import *


conn_string = 'sqlite:///test.sqlite3'
engine = create_engine(conn_string)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
