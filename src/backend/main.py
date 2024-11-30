from config import *
from preprocessing import load_images_from_folder
from standardization import standardize_images
from pca import compute_pca
from similarity import project_image, compute_similarity
from retrieval import retrieve_and_display_results

if __name__ == "__main__":
    # Load dataset
    images, image_names = load_images_from_folder(DATASET_PATH, IMAGE_SIZE)
    query_images, query_names = load_images_from_folder(QUERY_PATH, IMAGE_SIZE)
    
    # Standarisasi dataset
    standardized_images, mean_vector = standardize_images(images)
    
    # PCA Computation
    _, _, Vt_k = compute_pca(standardized_images, NUM_COMPONENTS)
    dataset_projections = standardized_images @ Vt_k.T
    
    # Process query image
    query_image = query_images[0]  # Ambil query pertama
    query_projection = project_image(query_image, mean_vector, Vt_k)
    
    # Compute similarities
    distances = compute_similarity(query_projection, dataset_projections)
    sorted_indices = distances.argsort()
    
    # Retrieve and display results
    retrieve_and_display_results(images, image_names, sorted_indices, distances, top_n=5, size=IMAGE_SIZE)
