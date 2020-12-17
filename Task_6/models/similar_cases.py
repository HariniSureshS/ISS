import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_similar_cases(cases, user_embedding, top_n = 5):

    db_ids = [case['id'] for case in cases]
    db_embeddings = np.array([np.array(case['embedding']) for case in cases])
    case_ids_and_embeddings = list(zip(db_ids, db_embeddings))

    sim_score_to_id = {}
    for id, embedding in case_ids_and_embeddings:
        score = cosine_similarity(user_embedding, embedding.reshape(1, -1)).flatten()
        score = np.array_str(score)
        sim_score_to_id[score] = id

    top_n_scores = sorted(sim_score_to_id.keys(),reverse=True)[1:top_n+1]
    top_n_ids = [sim_score_to_id[score] for score in top_n_scores]

    top_n_cases = [case for case in cases for id in top_n_ids if case['id'] == id]
    for case in top_n_cases:
        case.pop('embedding', None)

    return top_n_cases
