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
            movie['vector']
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
        normalized_rating = movie['rating']

        # NORMALISASI POPULARITY
        normalized_popularity = movie['popularity']

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
            'final_score': round(float(final_score), 4)
        })

    # SORT DESC
    recommendations = sorted(
        recommendations,
        key=lambda x: x['final_score'],
        reverse=True
    )

    # TOP 10
    top_movies = recommendations[:10]

    print("Similar Movies:")
    for movie in top_movies:
        print(f"  - {movie['id']}: {movie['final_score']}")

    # RETURN ID ONLY
    return [movie['id'] for movie in top_movies]