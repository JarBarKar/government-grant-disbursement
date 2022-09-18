from ..models import Member
from ..extensions import db
from datetime import datetime
from flask import Flask, request, jsonify, Blueprint


member = Blueprint('member', __name__)

### Start of API point for Family member creation ###


@member.route("/add_member", methods=['POST'])
def create_member():
    """Create a family member for a selected household

    Returns:
        message (string): success message
    """
    expected = ["name", "gender", "marital_status", "spouse",
                "occupation_type", "annual_income", "dob", "household_id"]
    validGenders = ["m", "f", "male", "female"]
    # Retrieved from https://www.singstat.gov.sg/-/media/files/standards_and_classifications/scms.ashx
    validMaritalStatus = ["single", "married", "widowed",
                          "seperated", "divorced", "not reported"]
    validOccupationType = ["unemployed", "student", "employed"]
    data = request.get_json()

    # Check for missing input
    for key in expected:
        if key not in data.keys():
            return jsonify(
                {
                    "message": f"{key} is not found!"
                }
            ), 500

    # Check for valid gender input
    if not (data['gender'].isalpha() and data['gender'].lower() in validGenders):
        return jsonify(
            {
                "message": f"Please input valid gender again"
            }
        ), 500

    # Check for valid marital status input
    if not (data['marital_status'].isalpha() and data['marital_status'].lower() in validMaritalStatus):
        return jsonify(
            {
                "message": f"Please input valid marital status again"
            }
        ), 500

    # Check for valid occupation type input
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
                "error": e,
                "message": "Family member creation failed."
            }
        ), 500

### End of API points for Family member creation ###
