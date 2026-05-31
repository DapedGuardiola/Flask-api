from flask import Blueprint, request, jsonify
from app.service.computeService import newUserTastes,newUserRecommendation, recomputeTastes

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