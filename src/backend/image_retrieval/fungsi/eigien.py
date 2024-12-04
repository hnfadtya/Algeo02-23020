import numpy as np
from numpy import array

# Buat Matriks Identitas NxN
def matrixIdentitas(N):
    return np.eye(N)

# Menghitung determinan
def determinan(matrix):
    return np.linalg.det(matrix)

# Mendapatkan Nilai Eigen dengan menggunakan persamaan karakteristik
def eigenValues(matrix):
    coefficients = np.poly(matrix)
    eigenValues = np.roots(coefficients)
    
    return np.unique((eigenValues)).astype(int)
    # return np.unique(np.round(eigenValues, 2)).astype(int)

matrix = array([[3, -2, 0], [-2, 3, 0], [0, 0, 5]])
eigen = eigenValues(matrix)
print(eigen)
# det = determinan(matrix)
# identitas = matrixIdentitas(3)
# print("Determinannya adalah:", det)
# print(identitas)

