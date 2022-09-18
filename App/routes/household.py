from ..extensions import db
from ..models import Member
from ..models import Household
from flask import Flask, request, jsonify, Blueprint

household = Blueprint('household', __name__)

### Start of API point for Household creation ###


@household.route("/household/add", methods=['POST'])
def create_household():
    expected = ["household_type"]
    validHouseholdType = ["Landed", "Condominium", "HDB"]
    data = request.get_json()

    # Check for missing key
    for key in expected:
        if key not in data.keys():
            return jsonify(
                {
                    "message": f"{key} is not found!"
                }
            ), 500

    # Check for invalid input
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
                "data": newHousehold.to_dict(),
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


### Start of API point for all Households retrieval ###
@household.route("/household/search", methods=['GET'])
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
### End of API point for all Households retrieval ###


### Start of API point for searching specific Household ###
@household.route("/household/search", methods=['GET'])
def search_household():
    id = request.args.get('id')
    try:
        result = []
        queries = db.session.query(Household, Member).join(
            Member).filter(Household.household_id == id).all()

        for query in queries:
            house, member = query
            parsedQuery = {**house.to_dict(), **member.to_dict()}
            result.append(parsedQuery)

        return jsonify(
            {
                "data": result,
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
