import numpy as np

def standardize_images(images):
    mean_vector = np.mean(images, axis=0)
    standardized_images = images - mean_vector
    return standardized_images, mean_vector
