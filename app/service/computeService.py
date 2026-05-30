from collections import defaultdict
import math

def newUserTastes(user_genres, favoriteMovieData):
    genre_count = defaultdict(int)
    director_count = defaultdict(int)
    actor_count = defaultdict(int)
    
    # print(f"data: {favoriteMovieData}") 
    era_counter = {
    'classic': 0,
    'modern': 0
    }

    genre_score = {}
    director_score = {}
    actor_score = {}
    era_score = {}
    normalized_rating_sum = 0.0
    normalized_popularity_sum = 0.0

    for genre_id in user_genres:
        genre_count[genre_id] += 1

    for movie in favoriteMovieData:
        
        year = movie['release_year']
        # print(f"release_year: {year}, type: {type(year)}") 
        if not year:
            continue
        year = int(year)
        if year < 2000:
            era_counter['classic'] += 1
        else:
            era_counter['modern'] += 1

        for d_id in movie.get('director_ids', []):
            director_count[d_id] += 1

        for a_id in movie.get('actor_ids', []):
            actor_count[a_id] += 1

        for genre_id in movie.get('genre_ids', []):
            genre_count[genre_id] += 1

        normalized = movie.get('normalized_data', {})
        normalized_rating_sum += float(normalized.get('n_rating', 0) or 0)
        normalized_popularity_sum += float(normalized.get('n_popularity', 0) or 0)

    total_genre = sum(genre_count.values()) or 0
    total_director = sum(director_count.values()) or 0
    total_actor = sum(actor_count.values()) or 0
    movie_count = len(favoriteMovieData) or 0

    for g, count in genre_count.items():
        genre_score[g] = round(count / total_genre,2)

    for d, count in director_count.items():
        director_score[d] = round(count / total_director,2)

    for a, count in actor_count.items():
        actor_score[a] = round(count / total_actor,2)
        
    for era,count in era_counter.items():
        era_score[era] = round(count / movie_count,2)
        
    preferred_normalized_rating = round(normalized_rating_sum / movie_count,2)
    preferred_normalized_popularity = round(normalized_popularity_sum / movie_count,2)
    
    return {
        'preferred_genres': genre_score,
        'preferred_directors': director_score,
        'preferred_actors': actor_score,
        'preferred_era':era_score,
        'preferred_normalized_rating': preferred_normalized_rating,
        'preferred_normalized_popularity': preferred_normalized_popularity,
    }
    
def gaussian_score(preferred, actual, sigma):
    return round(math.exp(-((actual - preferred) ** 2) / (2 * sigma ** 2)), 2)

def final_score(genre_score, director_score, actor_score, era_score, rating_score, popularity_score):
    WEIGHTS = {
            'genre'      : 0.40,
            'director'   : 0.20,
            'actor'      : 0.15,
            'era'        : 0.10,
            'rating'     : 0.10,
            'popularity' : 0.05,
    }
        
    return round(
        WEIGHTS['genre']      * genre_score      +
        WEIGHTS['director']   * director_score   +
        WEIGHTS['actor']      * actor_score      +
        WEIGHTS['era']        * era_score        +
        WEIGHTS['rating']     * rating_score     +
        WEIGHTS['popularity'] * popularity_score,
        2
    )

def newUserRecommendation(userGenres, userTastes, movies):
    genre_weight    = defaultdict(float)
    director_weight = defaultdict(float)
    actor_weight    = defaultdict(float)

    movie_genre_score      = defaultdict(float)
    movie_director_score   = defaultdict(float)
    movie_actor_score      = defaultdict(float)
    movie_final_scores     = defaultdict(float)

    preferredActors     = userTastes.get('preferred_actors', {})
    preferredDirectors  = userTastes.get('preferred_directors', {})
    preferredEra        = userTastes.get('preferred_era', {})
    preferredRating     = userTastes.get('preferred_normalized_rating', 0)
    preferredPopularity = userTastes.get('preferred_normalized_popularity', 0)

    # print(f"preferredActors: {preferredActors}")
    # print(f"preferredDirectors: {preferredDirectors}")
    # print(f"preferredEra: {preferredEra}")
    # print(f"preferredRating: {preferredRating}")
    # print(f"preferredPopularity: {preferredPopularity}")

    for era_key, weight in preferredEra.items():
        genre_weight[era_key] = weight

    for director_id, weight in preferredDirectors.items():
        director_weight[int(director_id)] = weight

    for actor_id, weight in preferredActors.items():
        actor_weight[int(actor_id)] = weight

    for ug in userGenres:
        genre_id = ug.get('genre_id')
        genre_weight[genre_id] = ug.get('weight', 0)

    # print(f"genre_weight: {dict(genre_weight)}")
    # print(f"director_weight: {dict(director_weight)}")
    # print(f"actor_weight: {dict(actor_weight)}")

    for m in movies:
        movie_id     = m.get('movie_id')
        release_year = m.get('release_year')
        normalized   = m.get('normalizedData') or {}
        # Genre score
        movie_genres = m.get('genre_ids', [])
        if not movie_genres:
            movie_genre_score[movie_id] = 0
        else:
            total = sum(genre_weight.get(mg, 0) for mg in movie_genres)
            movie_genre_score[movie_id] = round(total / len(movie_genres), 2)

        # Director score
        movie_directors = m.get('director_ids') or []
        if not movie_directors:
            movie_director_score[movie_id] = 0
        else:
            total = sum(director_weight.get(str(d), 0) for d in movie_directors)
            movie_director_score[movie_id] = round(total / len(movie_directors), 2)

        # Actor score
        movie_actors = m.get('actor_ids') or []
        if not movie_actors:
            movie_actor_score[movie_id] = 0
        else:
            total = sum(actor_weight.get(str(a), 0) for a in movie_actors)
            movie_actor_score[movie_id] = round(total / len(movie_actors), 2)

        # Rating & popularity score
        movie_rating_score     = gaussian_score(preferredRating, normalized.get('n_rating', 0),0.2)
        movie_popularity_score = gaussian_score(preferredPopularity, normalized.get('n_popularity', 0),0.2)

        # Era score
        if release_year:
            movie_era       = 'modern' if int(release_year) >= 2000 else 'classic'
            movie_era_score = preferredEra.get(movie_era, 0)
        else:
            movie_era_score = 0

        # Final score
        movie_final_scores[movie_id] = final_score(
            movie_genre_score[movie_id],
            movie_director_score[movie_id],
            movie_actor_score[movie_id],
            movie_era_score,
            movie_rating_score,
            movie_popularity_score
        )

    recommendation_ids = sorted(
        movie_final_scores,
        key=lambda x: movie_final_scores[x],
        reverse=True
    )[:40]

    # print(f'hasil rekomendasi: {recommendation_ids}')
    return recommendation_ids