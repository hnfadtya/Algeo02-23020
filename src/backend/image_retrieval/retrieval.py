import numpy as np
from backend.image_retrieval.preprocessing import process_image
from backend.image_retrieval.standardization import standardize_images
from backend.image_retrieval.pca import compute_pca
from backend.image_retrieval.similarity import compute_similarity

def image_retrieval_function(image_file):
    image_vector = process_image(image_file)
    standardized_images, mean_vector = standardize_images(image_vector)
    _, _, Vt_k = compute_pca(standardized_images, num_components=50)
    query_projection = np.dot(Vt_k, image_vector - mean_vector)
    dataset_projections = np.dot(standardized_images, Vt_k.T)
    similarities = compute_similarity(query_projection, dataset_projections)
    sorted_indices = similarities.argsort()[::-1]
    return sorted_indices
