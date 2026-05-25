from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def get_similar_movies(target_movie, movies):

    target_vector = np.array(
        target_movie['movie_genre_vector']
    ).reshape(1, -1)

    recommendations = []

    for movie in movies:

        # SKIP jika movie yang sama
        if movie['id'] == target_movie['id']:
            continue

        movie_vector = np.array(
            movie['movie_genre_vector']
        ).reshape(1, -1)

        # HITUNG COSINE SIMILARITY
        similarity_score = cosine_similarity(
            target_vector,
            movie_vector
        )[0][0]

        # FILTER movie yang terlalu tidak mirip
        if similarity_score < 0.3:
            continue

        # NORMALISASI RATING
        normalized_rating = movie['rating'] / 10

        # NORMALISASI POPULARITY
        normalized_popularity = movie['popularity'] / 1000

        # FINAL SCORE (Hybrid SAW Ranking)
        final_score = (
            (similarity_score * 0.80)
            +
            (normalized_rating * 0.15)
            +
            (normalized_popularity * 0.05)
        )

        recommendations.append({
            'id': movie['id'],
            'title': movie['title'],
            'similarity_score': round(float(similarity_score), 4),
            'final_score': round(float(final_score), 4)
        })

    # SORTING BERDASARKAN FINAL SCORE
    recommendations = sorted(
        recommendations,
        key=lambda x: x['final_score'],
        reverse=True
    )

    # AMBIL TOP 10 MOVIES
    return recommendations[:10]