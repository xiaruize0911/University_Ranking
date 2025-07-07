from flask import Blueprint, request, jsonify
from models.university import search_universities

universities_bp = Blueprint("universities", __name__)

@universities_bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    if not query.strip():
        return jsonify({"error": "Missing search query"}), 400
    
    results = search_universities(query)
    return jsonify(results)
