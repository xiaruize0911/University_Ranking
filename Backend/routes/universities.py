from flask import Blueprint, request, jsonify
from models.universities import search_universities

universities_bp = Blueprint("universities", __name__)

@universities_bp.route("/", methods=["GET"])
def search():
    query = request.args.get("search")
    print(f"Received query: {query}")
    sort_credit = request.args.get("sort_credit")
    print(f"Received sort_credit: {sort_credit}")
    results = search_universities(query, sort_credit)
    if results is None:
        return jsonify({"error": "An error occurred while searching for universities"}), 500
    return jsonify(results)
