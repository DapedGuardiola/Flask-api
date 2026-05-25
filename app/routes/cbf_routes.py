from flask import Blueprint, request, jsonify
from app.service.sawService import calculate_saw
from app.service.similar_movie_service import get_similar_movies

cbf_bp = Blueprint('cbf', __name__, url_prefix='/cbf')


# EXISTING ROUTE
@cbf_bp.route('/rank', methods=['POST'])
def rank():

    data = request.get_json()
    movies = data['movies']

    ranked_ids = calculate_saw(movies)

    return jsonify({
        'ranked_ids': ranked_ids
    })


# NEW ROUTE - SIMILAR MOVIES
@cbf_bp.route('/similar', methods=['POST'])
def similar_movies():

    data = request.get_json()

    target_movie = data['target_movie']
    movies = data['movies']

    result = get_similar_movies(
        target_movie,
        movies
    )

    return jsonify({
        'recommended_movies': result
    })

# @cbf_bp.route('/similar-movies', methods=['GET'])
# def similar_movies():

#     return jsonify({
#         'message': 'similar movies route active'
#     })