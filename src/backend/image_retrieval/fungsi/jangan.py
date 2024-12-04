import numpy as np

def svd(matrix):
    # Matriks non-persegi
    AtA = np.dot(matrix.T, matrix)  
    AAt = np.dot(matrix, matrix.T) 
    eigenValuesAtA = eigenValues(AtA)
    eigenValuesAAt = eigenValues(AtA)
    # Nilai singular
    singularValues = np.sqrt(np.abs(eigenValuesAtA))
    singularValues = np.sort(singularValues)[::-1]
    # Rumus A = U * Sigma * V Transpose
    # Nilai Sigmanya
    Sigma = np.zeros(matrix.shape)
    np.fill_diagonal(Sigma, singularValues)
    # Nilai V
    V = np.array([solveEigenvector(AtA, 0) for val in eigenValuesAtA])
    U = np.array([solveEigenvector(AAt, 0) for val in eigenValuesAAt])
    
    return U, Sigma, V.T

def eigenValues(matrix):
    # Memeriksa apakah matriks adalah persegi (M x N)
    if matrix.shape[0] == matrix.shape[1]:
        coefficients = np.poly(matrix)
        eigenValues = np.roots(coefficients)
        return np.unique(eigenValues).astype(float)

def rowReduce(matrix):
    """ Fungsi untuk melakukan eliminasi Gauss pada matriks """
    matrix = matrix.astype(float)  # Pastikan kita bekerja dengan tipe data float
    rows, cols = matrix.shape
    for i in range(min(rows, cols)):
        # Cari baris dengan elemen terbesar di kolom i (untuk stabilitas numerik)
        max_row = np.argmax(np.abs(matrix[i: , i])) + i
        matrix[[i, max_row]] = matrix[[max_row, i]]
        
        # Cek apakah pivot element adalah nol atau sangat kecil
        if np.abs(matrix[i, i]) < 1e-10:
            continue  # Lewati baris ini jika elemen pivot terlalu kecil atau nol
        
        # Normalisasi baris i
        matrix[i] = matrix[i] / matrix[i, i]
        
        # Eliminasi elemen-elemen di bawahnya
        for j in range(i+1, rows):
            matrix[j] = matrix[j] - matrix[j, i] * matrix[i]
    
    # Back substitution untuk mengurangi menjadi matriks eselon tereduksi
    for i in range(min(rows, cols)-1, -1, -1):
        for j in range(i-1, -1, -1):
            matrix[j] = matrix[j] - matrix[j, i] * matrix[i]
    
    return matrix


def solveEigenvector(matrix, eigenvalue):
    """ Menyelesaikan sistem linier (A - λI) v = 0 dengan eliminasi Gauss """
    n = matrix.shape[0]
    I = np.eye(n)
    A_lambda = matrix - eigenvalue * I  # Matriks A - λI
    
    # Menggunakan row reduction untuk menemukan null space (vektor eigen)
    reduced_matrix = rowReduce(A_lambda)
    
    # Vektor eigen adalah solusi non-trivial (vektor bebas)
    # Ambil kolom terakhir dari reduced_matrix sebagai vektor eigen
    # Kita anggap baris yang tidak tereliminasi sebagai bebas
    eigenvector = np.zeros(n)
    eigenvector[-1] = 1  # Assign 1 pada posisi bebas
    return eigenvector

    
    
# Contoh matriks persegi (2x2)
# matrix_square = np.array([[3, -2, 0], [-2, 3, 0], [0, 0, 5]])
# U, Sigma, VT = singularValues(matrix_square)
# print("U : ", U)
# print("Sigma : ", Sigma)
# print("VT : ", VT)

# Contoh matriks non-persegi (3x2)
matrix_non_square = np.array([[3, 1, 1], [-1, 3, 1]])
U, Sigma, VT = svd(matrix_non_square)
print("U : ", U)
print("Sigma : ", Sigma)
print("VT : ", VT)

A_reconstructed = np.dot(U, np.dot(Sigma, VT))
print("\nMatriks A yang direkonstruksi:")
print(A_reconstructed)
