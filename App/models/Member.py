from sqlalchemy import *
from sqlalchemy.orm import relationship

from models import Base

class Member(Base):
    __tablename__ = 'member'

    household_id= Column(Integer, primary_key=True, nullable=False)
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