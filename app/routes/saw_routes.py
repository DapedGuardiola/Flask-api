from flask import Blueprint,request,jsonify
from app.service.sawService import calculate_saw, calculate_saw_discover_test
saw_bp = Blueprint('saw',__name__,url_prefix='/saw')

@saw_bp.route('/rank',methods=['POST'])
def rank():
    data = request.get_json()
    movies = data['movies']
    ranked_ids = calculate_saw(movies)
    return jsonify({'ranked_ids':ranked_ids})

@saw_bp.route('/discoverTest', methods=['POST'])
def discover():
    try:
        data = request.get_json()

        if not data or 'movie_ids' not in data or 'user_vector' not in data:
            return jsonify({'error': 'missing fields'}), 400

        movie_ids = data['movie_ids']
        userInput = data['user_vector']
        
        ranked_ids = calculate_saw_discover_test(userInput, movie_ids)
        return jsonify({'ranked_id': ranked_ids})
    
    except Exception as e:
        import traceback
        print(traceback.format_exc())  # tampil di Flask log
        return jsonify({'error': str(e), 'ranked_id': []}), 500
# @saw_bp.route('/discover', methods=['POST'])
# def discover():
#     data = request.get_json()
#     movies = data['movies']
#     ranked_ids = calculate_saw_discover(movies)

#     return jsonify({'ranked_id': ranked_ids})