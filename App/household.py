from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/government-grant-disbursement'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


### Class Household ###
class Household(db.Model):
    __tablename__ = 'household'
    household_id= db.Column(db.Integer, primary_key=True, nullable=False)
    household_type = db.Column(db.String(64), nullable=False)


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
    __tablename__ = 'member'
    member_id= db.Column(db.Integer, primary_key=True, nullable=False)
    household_id= db.Column(db.Integer, db.ForeignKey('household.household_id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    marital_status = db.Column(db.String(64), nullable=False)
    spouse= db.Column(db.String(64), nullable=False)
    occupation_type = db.Column(db.String(64), nullable=False)
    annual_income = db.Column(db.Numeric(20,2), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)


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

# ### Auto-initate SQL DB and table once app.py launched ###
# db.create_all()
# db.session.commit()
# ### Auto-initate SQL DB and table once app.py launched ###


### Start of API point for Household creation ###
@app.route("/household/add", methods=['POST'])
def create_household():
    expected = ["household_type"]
    validHouseholdType = ["Landed","Condominium", "HDB"]
    data = request.get_json()
    
    #Check for missing key
    for key in expected:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is not found!"
            }
            ), 500
    
    #Check for invalid input
    if data["household_type"] not in validHouseholdType:
            return jsonify(
            {
                "message": f"{data['household_type']} is an invalid input!"
            }
            ), 500

    try:
        newHousehold = Household(household_type=data["household_type"])
        db.session.add(newHousehold)
        db.session.commit()
        return jsonify(
            {
                "data": newHousehold,
                "message": f"A {data['household_type']} house has been created in the system."
            }
        ), 200
    except Exception as e:
        return jsonify(
            {   
                "error": e,
                "message": "Household creation failed."
            }
        ), 500
### End of API point for Household creation ###


### Start of API point for Households retrieval ###
@app.route("/household", methods=['GET'])
def get_all_households():
    try:
        result = []
        queries = db.session.query(Household, Member).join(Member).all()
        for query in queries:
            house, member = query
            parsedQuery = {**house.to_dict(), **member.to_dict()}
            result.append(parsedQuery)
        return jsonify(
            {
                "data": result,
                "message": f"All households have been retrieved from the system."
            }
        ), 200

    except Exception as e:
        return jsonify(
            {   
                "error": e,
                "message": "Household retrieval failed."
            }
        ), 500
### End of API point for Households retrieval ###

### Start of API point for searching specific Household ###
@app.route("/household/search", methods=['GET'])
def search_household():
    id = request.args.get('id')
    try:
        result = []
        queries = db.session.query(Household, Member).join(Member).filter(Household.household_id==id).all()

        for query in queries:
            house, member = query
            parsedQuery = {**house.to_dict(), **member.to_dict()}
            result.append(parsedQuery)

        return jsonify(
            {
                "data" : result,
                "message": "Households has been found in the system."
            }
        ), 200

    except Exception as e:
        return jsonify(
            {   
                "error": e,
                "message": "Household retrieval failed."
            }
        ), 500
### End of API point for searching specific Household ###

if __name__ == '__main__':
    app.run(debug=True)