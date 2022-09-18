from ..extensions import db
from flask import Flask, request, jsonify, Blueprint

grant = Blueprint('grant', __name__)

### Start of API point for retrieving eligible family member for grant scheme ###


@grant.route("/grant_schemes", methods=['GET'])
def grant_schemes():
    grantSchemesSelected = request.args.get('grant', default=None)
    if not grantSchemesSelected:
        return jsonify(
            {
                "message": "Grant parameter in URL is not found."
            }
        ), 500
    try:
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
                "message": "Grant candidate retrieval failed."
            }
        ), 500

### End of API point for retrieving eligible family member for grant scheme ###
