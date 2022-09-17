from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from household import Household
from datetime import datetime


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


### Start of API point for Family member creation ###
@app.route("/add_member", methods=['POST'])
def create_member():
    expected = ["name","gender","marital_status","spouse", "occupation_type", "annual_income", "dob", "household_id"]
    validGenders = ["m","f","male","female"]
    #Retrieved from https://www.singstat.gov.sg/-/media/files/standards_and_classifications/scms.ashx
    validMaritalStatus = ["single","married","widowed","seperated","divorced","not reported"]
    validOccupationType = ["unemployed","student","employed"]
    data = request.get_json()
    
    #Check for missing input
    for key in expected:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is not found!"
            }
            ), 500

    #Check for valid gender input
    if not (data['gender'].isalpha() and data['gender'].lower() in validGenders):
        return jsonify(
            {
                "message": f"Please input valid gender again"
            }
            ), 500
    
    #Check for valid marital status input
    if not (data['marital_status'].isalpha() and data['marital_status'].lower() in validMaritalStatus):
        return jsonify(
            {
                "message": f"Please input valid marital status again"
            }
            ), 500

    #Check for valid occupation type input
    if not (data['occupation_type'].isalpha() and data['occupation_type'].lower() in validOccupationType):
        return jsonify(
            {
                "message": f"Please input valid occupation type again"
            }
            ), 500

    try:
        dobObject = datetime.strptime(data["dob"], '%d/%m/%Y')
        new_member = Member(household_id=data["household_id"], name=data["name"], gender=data["gender"], 
                            marital_status=data["marital_status"], spouse=data["spouse"], occupation_type=data["occupation_type"],
                            annual_income=data["annual_income"], dob=dobObject)
        db.session.add(new_member)
        db.session.commit()
        return jsonify(
            {
                "message": f"{data['name']} has been created and added into household {data['household_id']}."
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "error" : e,
                "message": "Family member creation failed."
            }
        ), 500
### End of API points for Member creation ###



if __name__ == '__main__':
    app.run(debug=True)