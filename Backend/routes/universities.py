from flask import Blueprint, request, jsonify
from models.universities import filter_universities

universities_bp = Blueprint("universities", __name__)

@universities_bp.route("/filter", methods=["GET"])
def filter_universities_route():
    query = request.args.get("query")
    sort_credit = request.args.get("sort_credit")
    country = request.args.get("country")
    city = request.args.get("city")

    results = filter_universities(query, sort_credit, country, city)
    return jsonify(results)

@universities_bp.route("/<int:univ_id>", methods=["GET"])
def get_university(univ_id):
    from models.university import get_university_by_id
    result = get_university_by_id(univ_id)
    if result:
        return jsonify(result)
    return jsonify({"error": "University not found"}), 404

