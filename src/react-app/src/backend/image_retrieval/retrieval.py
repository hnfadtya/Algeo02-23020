import numpy as np
import os
import math
import time
from PIL import Image
import scipy.sparse.linalg

def image_retrieval_function(image_file):
    start = time.time()
    folder_path = os.path.abspath("src/react-app/src/media/picture")  # Dataset gambar
    query_path = os.path.abspath(f"src/react-app/src/media/uploads/{image_file}")  # Query

    intensityMatrix = []
    filenames = []

    # Proses dataset gambar
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            full_path = os.path.join(folder_path, filename)
            filenames.append(filename)
            intensityMatrix.append(process_image(full_path))
    total_images = len(filenames)

    standardizedImages, meanVector = standardize_images(intensityMatrix)
    matrixU = PCA(standardizedImages, total_images)
    Z = np.dot(standardizedImages, matrixU)

    # Proses query image
    imageVector = process_image(query_path)
    standardizedQuery = imageVector - meanVector
    query_projection = np.dot(standardizedQuery, matrixU)
    similarities = compute_similarity(query_projection, Z, total_images)

    end = time.time()
    return similarities, total_images, end - start

# 1. Preprocessing
def process_image(image_path):
    with Image.open(image_path) as img:
        # Konversi ke grayscale
        # img = img.convert("RGB")                
        # arrayOfRGB = np.array(img)
        # grayscaledArray = 0.2989 * arrayOfRGB[:, :, 0] + 0.5870 * arrayOfRGB[:, :, 1] + 0.1140 * arrayOfRGB[:, :, 2]
        # grayscaledImage = Image.fromarray(grayscaledArray.astype("uint8"))
        # resizedImage = grayscaledImage.resize((8, 8))
        grayscaleImage = img.convert("L")
        resizedImage = grayscaleImage.resize((10, 10))

        # Ubah ke numpy array dan flatten
        return np.array(resizedImage).flatten()

# 2. Standardization 
def standardize_images(images):
    mean_vector = np.mean(images, axis=0) # Hitung rata-rata setiap piksel di seluruh gambar
    standardized_images = images - mean_vector # Kurangi rata-rata dari setiap piksel
    return standardized_images, mean_vector

# 3. PCA
def PCA(matrix, totalImages):
    transpose = np.transpose(matrix)
    covarian = np.dot(transpose, matrix)
    constant = (1 / totalImages)
    covarian = np.multiply(covarian, constant)
    matU, S, Vt = scipy.sparse.linalg.svds(covarian, k=3) #0 < k < min(A.shape)
    matU = matU[:, :3]  # Komponen utama
    return matU


# 4. Similarity
def compute_similarity(query_projection, dataset_projections, totalImages):
    distances = []
    for i in range(totalImages):
        sum = 0
        for j in range(3):
            sum += math.pow((query_projection[j] - dataset_projections[i][j]), 2)
        index = [i, math.sqrt(sum)]
        distances.append(index) 

    for i in range(len(distances)):
        for j in range((len(distances)) - i - 1):
            if distances[j][1] > distances[j+1][1]:
                distances[j], distances[j+1] = distances[j+1], distances[j]

    return distances