import numpy as np
from backend.image_retrieval.preprocessing import process_image
from backend.image_retrieval.standardization import standardize_images
from backend.image_retrieval.pca import compute_pca
from backend.image_retrieval.similarity import compute_similarity

def image_retrieval_function(image_file):
    # Proses gambar menjadi vektor numpy
    image_vector = process_image(image_file)
    # Standarisasi dataset gambar
    standardized_images, mean_vector = standardize_images(image_vector)
    # Komputasi PCA
    _, _, Vt_k = compute_pca(standardized_images, num_components=50)
    # Proyeksi query ke ruang PCA
    query_projection = np.dot(image_vector - mean_vector, Vt_k.T)
    # Hitung kesamaan antara query dan dataset
    dataset_projections = np.dot(standardized_images, Vt_k.T)
    similarities = compute_similarity(query_projection, dataset_projections)
    return similarities.argsort()[::-1]
