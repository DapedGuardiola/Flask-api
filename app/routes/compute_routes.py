from flask import Blueprint, request, jsonify
from app.service.computeService import newUserTastes,newUserRecommendation, recomputeTastes, calculate_intersect_genres

compute_bp = Blueprint('compute', __name__, url_prefix='/compute')

@compute_bp.route('/new-taste', methods=['POST'])
def computeNewTaste():
    data = request.get_json()
    userGenres = data['userGenres']
    favoriteMovieData = data['favoriteMovieData'] 
    UserTastes = newUserTastes(userGenres,favoriteMovieData)

    return jsonify({
        'userNewTastes': UserTastes
    })

@compute_bp.route('/recompute-tastes', methods=['POST'])
def recomputeTaste():
    data = request.get_json()
    userGenres = data.get('userGenres')
    userTastes = data.get('userTastes')
    userLog = data.get('userLog')
    movies = data.get('movies') 
    tastes = recomputeTastes(userGenres,userTastes,userLog,movies)

    return jsonify({
        'userNewTastes': tastes
    })
    
@compute_bp.route('/new-recommendation', methods=['POST'])
def computeNewRecommendation():
    data = request.get_json()
    userGenres = data.get('userGenres')
    userTastes = data.get('userTastes')
    movies = data.get('movies') 
    recommendation_ids = newUserRecommendation(userGenres,userTastes,movies)

    return jsonify({
        'recommendation_ids': recommendation_ids
    })


@compute_bp.route('/intersect-genres', methods=['POST'])
def computeIntersectGenres():
    data = request.get_json()
    
    if not data or 'movies' not in data:
        return jsonify({'error': 'The movies field is required'}), 400
        
    movies_data = data.get('movies', [])
    
    # Sekarang result isinya langsung array ID film, misal: [12, 45, 89]
    result_movie_ids = calculate_intersect_genres(movies_data)

    return jsonify({
        'status': 'success',
        'valid_movie_ids': result_movie_ids,
        'count': len(result_movie_ids)
    })