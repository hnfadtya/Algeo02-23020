import numpy as np
from PIL import Image
import InputImage as II

def compute_similarity(query_projection, dataset_projections):
    distances = np.linalg.norm(dataset_projections - query_projection, axis=1)
    return distances



# def EigenFace(eigenvector, selisih, S):
#     eigFace = []
#     A = np.array([selisih[0]])
#     for i in range(1,len(selisih)):
#         A = np.concatenate((A,[selisih[i]]),axis = 0)
#     A = np.transpose(A)
#     A = A[0]
#     rata = OM.RataRataMatrix(S)
#     rata = np.array(rata)
#     eigFace = np.matmul(A,eigenvector)
#     eigFace = np.transpose(eigFace)
#     for i in range (len(eigFace)):
#         for j in range (len(eigFace[0])):
#             eigFace[i][j] = eigFace[i][j] + rata[i]
#     #cari k untuk membuat suatu eigen face yang paling efektif (diambil 50%)
#     k = round(len(eigFace)*0.5)
#     ret = [[0 for i in range (len(eigFace[0]))] for j in range (k)]
#     for i in range (len(ret)):
#         for j in range (len(ret[0])):
#             ret[i][j] = eigFace[i][j]
#     eigFace = np.array(ret)
#     # calculate the weight of each eigenface
#     weight = [[0 for x in range(len(eigFace))] for y in range(len(selisih))]

#     for i in range(len(selisih)):
#         for j in range(len(eigFace)):
#             weight[i][j] = np.dot(eigFace[j],selisih[i])
#     weight = np.array(weight)
#     return eigFace, weight

# def EigenNewFace(FaceDir,mean, eigFace):
#     # Buat wajah jadi matriks
#     faceMatriks = II.ImgToMatrix(FaceDir)
#     subtracted = np.subtract(faceMatriks, mean)
#     subtracted = np.transpose(subtracted)
#     subtracted = subtracted[0]
#     subtracted = np.transpose(subtracted)
#     weight = np.matmul(eigFace,subtracted)
#     return weight

def EuclideanDistance(faceMatriks, EigenNewFace):
    # I.S. faceMatriks dan EigenNewFace terdefinisi
    # F.S. mengembalikan nilai jarak euclidean dari wajah baru dengan wajah yang sudah ada
    distance = [0 for i in range(len(faceMatriks))]
    sum  = 0
    for i in range (len(faceMatriks)):
        sum = 0
        for j in range (len(faceMatriks[0])):
            sum += (faceMatriks[i][j] - EigenNewFace[j])**2
        distance[i] = np.sqrt(sum)
    # find the minimum distance
    min = distance[0]
    max = distance[0]
    index = 0
    for i in range(len(distance)):
        if distance[i] < min:
            min = distance[i]
            index = i
        if distance[i]>max:
            max = distance[i]
    th = 0.15*max
    if (min<th):
        bth = True
    else:
        bth = False
    return index,bth