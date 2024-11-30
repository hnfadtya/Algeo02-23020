import numpy as np

def compute_similarity(query_features, dataset_features):
    similarities = []
    for features in dataset_features:
        similarity = np.dot(query_features, features) / (
            np.linalg.norm(query_features) * np.linalg.norm(features)
        )
        similarities.append(similarity)
    return np.array(similarities) * 100
