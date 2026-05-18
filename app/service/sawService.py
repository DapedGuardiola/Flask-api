import json
from pathlib import Path

def calculate_saw(movies):
    # logic SAW di sini
    ranked_ids = []
    return ranked_ids

def calculate_coocurrence(user_input, genres_vector, matrix):
    results = []
    total_user_genres = sum(user_input)
    
    for movie in genres_vector:
        movie_id = movie['id']
        movie_vector = movie['vector']
        match = [
            idx
            for idx, (u, m)
            in enumerate(zip(user_input, movie_vector))
            if u == 1 and m == 1
        ]
        if not match:
            results.append({
                'id': movie_id,
                'score': 0
            })
            continue
        match_set = set(match)
        other_genres = [
            idx
            for idx, val in enumerate(movie_vector)
            if val == 1 and idx not in match_set
        ]

        direct_score = len(match) / total_user_genres

        relation_scores = [
            matrix[m]['cooccurrence_vector'][o]
            for m in match
            for o in other_genres
        ]

        relation_score = (
            sum(relation_scores) / len(relation_scores)
            if relation_scores else 0
        )

        final_score = (
            0.7 * direct_score +
            0.3 * relation_score
        )

        results.append({
            'id': movie_id,
            'score': final_score
        })

    return results

def calculate_saw_discover_test(user_input, movies):
    current_file = Path(__file__).resolve()
    root_path = current_file.parent.parent.parent
    file_path = root_path / "genre_cooccurrence.json"

    with open(file_path, "r", encoding="utf-8") as file:
        matrix = json.load(file)

    genres_vector = [
        {'id': movie["id"], 'vector': json.loads(movie['vector']) if isinstance(movie['vector'], str) else movie['vector']}
        for movie in movies
    ]

    genre_coocurrence = calculate_coocurrence(user_input, genres_vector, matrix)
    cooc_lookup = {item['id']: item['score'] for item in genre_coocurrence}

    weights = {'rating': 0.2, 'popularity': 0.2, 'genre': 0.6}

    if not movies:
        return []

    def safe_float(value, default=0.0):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    scored = []
    for m in movies:
        score = (
            safe_float(m.get('rating'))     * weights['rating'] +
            safe_float(m.get('popularity')) * weights['popularity'] +
            safe_float(cooc_lookup.get(m['id'], 0)) * weights['genre']
        )
        scored.append({'id': m['id'], 'score': score})
    scored.sort(key=lambda x: x['score'], reverse=True)
    return [m['id'] for m in scored]

def calculate_saw_discover(movies):
    
    weights = {
        'rating':      0.5,
        'popularity':  0.3,
        'rating_count': 0.2,
    }

    if not movies:
        return []

    max_rating       = max(float(m['rating']) for m in movies) or 1
    max_popularity   = max(float(m['popularity']) for m in movies) or 1
    max_rating_count = max(float(m['rating_count']) for m in movies) or 1

    scored = []
    for m in movies:
        score = (
            (float(m['rating']) / max_rating) * weights['rating'] +
            (float(m['popularity']) / max_popularity) * weights['popularity'] +
            (float(m['rating_count']) / max_rating_count) * weights['rating_count']
        )
        scored.append({'id': m['id'], 'score': score})

    scored.sort(key=lambda x: x['score'], reverse=True)

    return [m['id'] for m in scored]