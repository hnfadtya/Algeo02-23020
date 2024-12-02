import numpy as np
import math
from PIL import Image

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
        for j in range((len(distances)) - i):
            if distances[i][1] < distances[j][1]:
                temp = distances[i][1]
                distances[i][1] = distances[j][1]
                distances[j][1] = temp

    return distances