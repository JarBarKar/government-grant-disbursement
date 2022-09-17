from distutils.command.sdist import sdist
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


### Start of API point for retrieve eligible households for grant scheme ###
@app.route("/grant_schemes", methods=['GET'])
def grant_schemes():
    grantSchemesSelected = request.args.get('grant', default=None)
    if not grantSchemesSelected:           
        return jsonify(
            {   
                "message": "Grant parameter in URL is not found."
            }
        ), 500
    try:
        grantSchemesSelected = request.args.get('grant')
        if grantSchemesSelected == "student-encouragement-bonus":
            queries = db.engine.execute("SELECT * FROM MEMBER WHERE household_id in \
                                        (SELECT DISTINCT(household_id) as household_id from member \
                                        where timestampdiff(YEAR, dob, now()) < 16 and occupation_type='Student' \
                                        group by household_id \
                                        having SUM(annual_income)<600000) AND \
                                        timestampdiff(YEAR, dob, now()) < 16;").fetchall()
            return jsonify(
                {
                    'result': [dict(row) for row in queries],
                    'message': 'All eligible members for Student Encouragement bonus retrieved'
                } 
            ), 200
            

        elif grantSchemesSelected == "multigeneration-scheme":
            queries = db.engine.execute("SELECT * from member \
                                        where household_id in \
                                        (SELECT DISTINCT(household_id)as household_id from member \
                                        where timestampdiff(YEAR, dob, now()) < 18 or timestampdiff(YEAR, dob, now()) > 55 \
                                        group by household_id \
                                        having SUM(annual_income)<150000);").fetchall()
            return jsonify(
                {
                    'result': [dict(row) for row in queries],
                    'message': 'All eligible members for Multigeneration Scheme retrieved'
                } 
            ), 200

        elif grantSchemesSelected == "elder-bonus":
            queries = db.engine.execute("SELECT * from member as m \
                                        inner join household as h \
                                        on m.household_id=h.household_id \
                                        where timestampdiff(YEAR, dob, now()) >=55 and \
                                        household_type='HDB';").fetchall()
            return jsonify(
                {
                    'result': [dict(row) for row in queries],
                    'message': 'All eligible members for Elder Bonus'
                } 
            ), 200

        elif grantSchemesSelected == "baby-sunshine-grant":
            queries = db.engine.execute("SELECT * from member as m \
                                        inner join household as h \
                                        on m.household_id=h.household_id \
                                        where timestampdiff(MONTH, dob, now()) <8;").fetchall()
            return jsonify(
                {
                    'result': [dict(row) for row in queries],
                    'message': 'All eligible members for Baby Sunshine Grant'
                } 
            ), 200


        elif grantSchemesSelected == "yolo-gst-grant":
            queries = db.engine.execute("SELECT * from member \
                                        where household_id in \
                                        (SELECT DISTINCT(m.household_id) from member as m \
                                        inner join household as h \
                                        on m.household_id=h.household_id \
                                        group by m.household_id \
                                        having SUM(annual_income)<100000);").fetchall()
            return jsonify(
                {
                    'result': [dict(row) for row in queries],
                    'message': 'All eligible members for YOLO GST Grant'
                } 
            ), 200

        return jsonify(
            {   
                "message": f"{grantSchemesSelected} is not a valid grant."
            }
        ), 500



    except Exception as e:
        return jsonify(
            {   
                "error": e,
                "message": "Household retrieval failed."
            }
        ), 500


### End of API point for Household creation ###

if __name__ == '__main__':
    app.run(debug=True, port=5001)