import numpy as np

def standardize_images(matrix, N):
    # mean_vector = np.mean(images, axis=0)
    standardizedMatrix = []
    for j in range(len(matrix[j])):
        standardizedImage = []
        for i in range(N):
            sumOfPixelIntensity = sumOfPixelIntensity + matrix[i][j]
            mean =  sumOfPixelIntensity/N
            standardizedImage = matrix[i][j] - mean
        standardizedMatrix.append(standardizedImage)
    return standardizedMatrix

