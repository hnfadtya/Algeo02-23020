import numpy as np
import os
import math
import time
from PIL import Image
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix

# from svd import svd
# from image_retrieval.preprocessing import process_image
# from image_retrieval.standardization import standardize_images
# from image_retrieval.pca import compute_pca
# from image_retrieval.similarity import compute_similarity

def image_retrieval_function(image_file):
    # Proses gambar menjadi vektor numpy
    folder_path = ("src/dataset/images/")
    intensityMatrix = []
    filenames = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            full_path = os.path.join(folder_path, filename)
            try:
                filenames.append(filename)
                intensityMatrix.append(process_image(full_path))
            except Exception as e:  
                print(f"Error processing {filename}: {e}")
    
    # Standarisasi dataset gambar
    standardizedImages, meanVector = standardize_images(intensityMatrix) #standardizedImages adalah matrix dari seluruh gambar yang telah distandarisasi, size = MN x MN

    # Komputasi PCA
    U = svd(standardizedImages)
    Uk = U[:, :50]

    # Hitung kesamaan antara query dan dataset
    Z = np.dot(standardizedImages, Uk)
    imagePath = (f"src/dataset/query/{image_file}")
    imageVector = process_image(imagePath)
    query_projection = np.dot(imageVector - meanVector, Uk)
    similarities = compute_similarity(query_projection, Z, len(filenames))
    return similarities

# 1. Preprocessing
def process_image(image_path):
    with Image.open(image_path) as img:
        # Konversi ke grayscale
        img = img.convert("RGB")                
        arrayOfRGB = np.array(img)
        grayscaledArray = 0.2989 * arrayOfRGB[:, :, 0] + 0.5870 * arrayOfRGB[:, :, 1] + 0.1140 * arrayOfRGB[:, :, 2]
        grayscaledImage = Image.fromarray(grayscaledArray.astype("uint8"))
        resizedImage = grayscaledImage.resize((128, 128))

        # Ubah ke numpy array dan flatten
        return np.array(resizedImage).flatten()

# 2. Standardization 
def standardize_images(matrix, N):
    standardizedMatrix = matrix.copy()
    meanVector = []
    pixelLength = len(matrix[0])
    # k = 0
    for j in range(pixelLength):
        sumOfPixelIntensity = 0
        for i in range(N):
            sumOfPixelIntensity = sumOfPixelIntensity + matrix[i][j]
        mean =  sumOfPixelIntensity/N
        i = 0
        for i in range(N):
            standardizedMatrix[i][j] = matrix[i][j] - mean
        meanVector.append(mean)
        # print(f"{k+1}\n")
        # k += 1

    return standardizedMatrix, meanVector

# 3. PCA
def getCovarian(matrix, totalImages):
    transpose = np.transpose(matrix)
    matrix = np.dot(transpose, matrix)
    matrix = np.dot(matrix, (1 / totalImages))
    matrix = matrix / np.linalg.norm(matrix)

    return matrix


# 4. Similarity
def compute_similarity(query_projection, dataset_projections, totalImages):
    # distances = np.linalg.norm(dataset_projections - query_projection, axis=1)
    distances = []
    for i in range(totalImages):
        sum = 0
        for j in range(50):
            sum += math.pow((query_projection[j] - dataset_projections[i][j]), 2)
        index = [i, math.sqrt(sum)]
        distances.append(index) 

    for i in range(len(distances)):
        for j in range((len(distances)) - i - 1):
            if distances[i][1] < distances[i+1][1]:
                temp = distances[i]
                distances[i] = distances[i+1]
                distances[i+1] = temp

    return distances

if __name__ == "__main__":
    # 1. preprocessing 
    start = time.time()
    folder_path = ("src/dataset/images/")
    intensityMatrix = []
    filenames = []
    # totalImages = len(filenames)
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            full_path = os.path.join(folder_path, filename)
            try:
                filenames.append(filename)
                intensityMatrix.append(process_image(full_path))
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    end = time.time()
    print(f"Processed {len(filenames)} images.")
    print(f"Waktu yang dibutuhkan untuk preprocessing adalah: {end - start} detik\n")
    # for i in range(len(intensityMatrix)):
        # print(f"image name: {filenames[i]}\n")
        # print(f"image vector: {(intensityMatrix[i])}\n")
        # print(f"vector length: {len(intensityMatrix[i])}\n")

    # 2. stamdar
    start = time.time()
    standardizedImages, meanVector = standardize_images(intensityMatrix, len(filenames)) #standardizedImages adalah matrix dari seluruh gambar yang telah distandarisasi, size = jumlah gambar x MN
    end = time.time()
    print(f"Waktu yang dibutuhkan untuk standardization: {end - start} detik\n")

    # print(f"standarisasi: {(standardizedImages)}\n")
    # # print(f"vektor rata2: {(meanVector)}\n")
    # print(f"matriks length: {len(standardizedImages[0])}\n")

    # Komputasi PCA
    start = time.time()
    covarian = csr_matrix(getCovarian(standardizedImages, len(filenames))) #size = MN x MN
    end = time.time()
    print(f"Waktu yang dibutuhkan untuk mencari kovarian : {end - start} detik\n")
    # print(f"covarian: {covarian}\n")
    # print(f"matriks length: {len(covarian[0])}\n")
    # U, S, V = np.linalg.svd(getCovarian(standardizedImages, len(filenames)), full_matrices=True)
    start = time.time()
    U, S, Vt = svds(covarian, k=50)
    end = time.time()
    print(f"Waktu yang dibutuhkan untuk mencari matriks U : {end - start} detik\n")
    # print(f"svd: {U}\n")
    # vertical, horizontal = U.shape
    # print(f"matriks length: {vertical}\n")
    # print(f"matriks length: {horizontal}\n")

    # # Hitung kesamaan antara query dan dataset
    start = time.time()
    Z = np.dot(standardizedImages, U)
    imagePath = (f"src/dataset/query/Puyol.jpg")
    imageVector = process_image(imagePath)
    query_projection = np.dot(imageVector - meanVector, U)
    similarities = compute_similarity(query_projection, Z, len(filenames))
    end = time.time()
    print(f"Waktu yang dibutuhkan untuk mencari similarity : {end - start} detik\n")
    print(similarities)
    for i in range(len(filenames)):
        print(f"nama file ke-{similarities[i][0] + 1}: {filenames[similarities[i][0]]}; memiliki similarity sebesar : {similarities[i][1]}\n")
    # print(f"similarity: {image_retrieval_function("src/dataset/images/JayRidho.jpg")}\n")