from sqlalchemy import *
from .extensions import db

### Class Household ###


class Household(db.Model):
    """
    Household class
    """
    __tablename__ = 'household'

    household_id = Column(Integer, primary_key=True, nullable=False)
    household_type = Column(String(64), nullable=False)

    def __init__(self, household_type):
        self.household_type = household_type

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
### Class Household ###

### Class Member ###


class Member(db.Model):
    """
    Member class
    """
    __tablename__ = 'member'
    member_id = Column(Integer, primary_key=True, nullable=False)
    household_id = Column(Integer, ForeignKey(
        'household.household_id'), nullable=False)
    name = Column(String(64), nullable=False)
    gender = Column(String(10), nullable=False)
    marital_status = Column(String(64), nullable=False)
    spouse = Column(String(64), nullable=False)
    occupation_type = Column(String(64), nullable=False)
    annual_income = Column(Numeric(20, 2), nullable=False)
    dob = Column(DateTime, nullable=False)

    def __init__(self, household_id, name, gender, marital_status, spouse, occupation_type, annual_income, dob):
        self.household_id = household_id
        self.name = name
        self.gender = gender
        self.marital_status = marital_status
        self.spouse = spouse
        self.occupation_type = occupation_type
        self.annual_income = annual_income
        self.dob = dob

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
### Class Member ###
