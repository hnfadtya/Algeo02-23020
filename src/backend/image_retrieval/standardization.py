import numpy as np

def standardize_images(matrix, N):
    # mean_vector = np.mean(images, axis=0)
    standardizedImages = []
    for j in range(len(matrix[j])):
        standardizedIntensity = []
        for i in range(N):
            sumOfPixelIntensity = sumOfPixelIntensity + matrix[i][j]
            mean =  sumOfPixelIntensity/N
            standardizedIntensity = matrix[i][j] - mean
        standardizedImages.append(standardizedIntensity)
    return standardizedImages

