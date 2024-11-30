import numpy as np

def compute_similarity(query_projection, dataset_projections):
    distances = np.linalg.norm(dataset_projections - query_projection, axis=1)
    return distances
