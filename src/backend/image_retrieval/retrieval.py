import numpy as np
import os
from backend.image_retrieval.preprocessing import process_image
from backend.image_retrieval.standardization import standardize_images
from backend.image_retrieval.pca import compute_pca
from backend.image_retrieval.similarity import compute_similarity

def image_retrieval_function(image_file):
    # Proses gambar menjadi vektor numpy
    folder_path = 
    totalImages = getTotalImage(folder_path)
    size = (100,100)
    intensityMatrix = []
    filenames = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            full_path = os.path.join(folder_path, filename)
            try:
                filenames.append(filename)
                intensityMatrix.append(process_image(full_path, size))
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    # Standarisasi dataset gambar
    standardized_images = standardize_images(intensityMatrix) #standardized_images adalah matrix dari seluruh gambar yang telah distandarisasi, size = MN x MN

    # Komputasi PCA
    _, _, Vt_k = compute_pca(standardized_images, num_components=50, totalImages)
    # Proyeksi query ke ruang PCA
    query_projection = np.dot(image_vector - mean_vector, Vt_k.T)
    # Hitung kesamaan antara query dan dataset
    dataset_projections = np.dot(standardized_images, Vt_k.T)
    similarities = compute_similarity(query_projection, dataset_projections)
    return similarities.argsort()[::-1]


def getTotalImage(folder_path):

