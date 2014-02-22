from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from openfreeweb import db

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.

'''
class User(Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password
'''

class AccessPoint
    __tablename__ = 'InternetAccessPoint'

    iap_id = db.Column(db.Integer, primary_key=True)
    iap_name = db.Column(db.String(120), unique=True)
    iap_str_address = db.Column(db.String(120))
    iap_city = db.Column(db.String(120))
    iap_state = db.Column(db.String(16))
    iap_zip = db.Column(db.Integer)
    email = db.Column(db.String(120))
    tel = db.Column(db.String(10))



# Create tables.
Base.metadata.create_all(bind=engine)
