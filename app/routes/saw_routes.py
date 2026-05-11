from flask import Blueprint,request,jsonify
from app.service.sawService import calculate_saw
saw_bp = Blueprint('saw',__name__,url_prefix='/saw')

@saw_bp.route('/rank',methods=['POST'])
def rank():
    data = request.get_json()
    movies = data['movies']
    ranked_ids = calculate_saw(movies)
    return jsonify({'ranked_ids':ranked_ids})