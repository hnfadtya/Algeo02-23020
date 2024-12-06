import numpy as np

def svd(matrix):
    # Matriks non-persegi
    AtA = np.dot(matrix.T, matrix)  
    AAt = np.dot(matrix, matrix.T) 
    
    # Nilai singular
    eigenValuesAAt = eigenValues(AAt)
    singularValues = np.sqrt(eigenValuesAAt)
    singularValues = np.sort(singularValues)[::-1]
    
    # Rumus A = U * Sigma * V Transpose
    # Nilai Sigmanya
    Sigma = np.zeros(matrix.shape)
    np.fill_diagonal(Sigma, singularValues)
    
    # Nilai U dan V
    _, _, Vt = np.linalg.svd(matrix)
    U = np.array([solveEigenvector(AAt, val) for val in eigenValuesAAt])
    
    return U, Sigma, Vt

def eigenValues(matrix):
    # Memeriksa apakah matriks adalah persegi (M x N)
    if matrix.shape[0] == matrix.shape[1]:
        coefficients = np.poly(matrix)
        eigenValues = np.roots(coefficients)
        return np.unique(eigenValues).astype(float)

def solveEigenvector(matrix, eigenvalue):
    """ Menyelesaikan sistem linier (A - λI) v = 0 dengan np.linalg.solve """
    n = matrix.shape[0]
    I = np.eye(n)
    A_lambda = matrix - eigenvalue * I  # Matriks A - λI
    
    # Mencari solusi non-trivial untuk (A - λI) v = 0
    # Kita gunakan np.linalg.svd untuk mencari vektor null (vektor eigen)
    _, _, Vt = np.linalg.svd(A_lambda)
    eigenvector = Vt[-1]  # Vektor eigen adalah vektor terakhir dari Vt
    
    return eigenvector

# Contoh matriks non-persegi (3x2)
matrix_non_square = np.array([[1,1],[0,1],[1,0]])

# Menemukan dekomposisi SVD
U, Sigma, VT = svd(matrix_non_square)
print("U : ", U)
print("Sigma : ", Sigma)

# Matriks A yang direkonstruksi
A_reconstructed = np.dot(U, np.dot(Sigma, VT))
print("\nMatriks A yang direkonstruksi:")
print(A_reconstructed)
