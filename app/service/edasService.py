def calculate_edas_alltime(movies: list) -> list:
    if not movies:
        return []

    weights = {
        'popularity':   0.50,
        'rating':       0.35,
        'rating_count': 0.15,
    }
    criteria = list(weights.keys())

    # 1. Average Solution per kriteria
    av = {}
    for c in criteria:
        values = [m.get(c, 0) for m in movies]
        av[c] = sum(values) / len(values) if values else 0

    # 2. Hitung PDA dan NDA
    results = []
    for movie in movies:
        sp = 0.0
        sn = 0.0

        for c in criteria:
            val  = movie.get(c, 0)
            av_c = av[c] if av[c] != 0 else 1e-9

            pda = max(0, (val - av_c) / av_c)
            nda = max(0, (av_c - val) / av_c)

            sp += weights[c] * pda
            sn += weights[c] * nda

        results.append({'id': movie['id'], 'sp': sp, 'sn': sn})

    # 3. Normalisasi → Appraisal Score
    max_sp = max(r['sp'] for r in results) or 1e-9
    max_sn = max(r['sn'] for r in results) or 1e-9

    for r in results:
        nsp        = r['sp'] / max_sp
        nsn        = 1 - (r['sn'] / max_sn)
        r['score'] = 0.5 * (nsp + nsn)

    results.sort(key=lambda x: x['score'], reverse=True)

    return [r['id'] for r in results]

def calculate_edas_bestbygenre(movies: list) -> list:
    if not movies:
        return []

    weights = {
        'popularity':   0.35,
        'rating':       0.45,
        'rating_count': 0.20,
    }
    criteria = list(weights.keys())

    # 1. Hitung Average Solution (AV) per kriteria
    av = {}
    for c in criteria:
        values = [m.get(c, 0) for m in movies]
        av[c] = sum(values) / len(values) if values else 0

    # 2. Hitung PDA dan NDA tiap movie
    results = []
    for movie in movies:
        sp = 0.0
        sn = 0.0

        for c in criteria:
            val  = movie.get(c, 0)
            av_c = av[c] if av[c] != 0 else 1e-9

            pda = max(0, (val - av_c) / av_c)
            nda = max(0, (av_c - val) / av_c)

            sp += weights[c] * pda
            sn += weights[c] * nda

        results.append({'id': movie['id'], 'sp': sp, 'sn': sn})

    # 3. Normalisasi → Appraisal Score
    max_sp = max(r['sp'] for r in results) or 1e-9
    max_sn = max(r['sn'] for r in results) or 1e-9

    for r in results:
        nsp       = r['sp'] / max_sp
        nsn       = 1 - (r['sn'] / max_sn)
        r['score'] = 0.5 * (nsp + nsn)

    results.sort(key=lambda x: x['score'], reverse=True)

    return [r['id'] for r in results]