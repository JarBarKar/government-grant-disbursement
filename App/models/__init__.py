from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

_DB_URI = 'mysql+pymysql://root:@127.0.0.1:3306/government-grant-disbursement'
engine = create_engine(_DB_URI)

Base = declarative_base()
Base.metadata.create_all(engine)
db = sessionmaker(bind=engine)
session = db()

from .Household import Household
from .Member import Member