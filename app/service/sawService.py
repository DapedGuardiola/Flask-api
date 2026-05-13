import json

def calculate_saw(movies):
    # logic SAW di sini
    ranked_ids = []
    return ranked_ids

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