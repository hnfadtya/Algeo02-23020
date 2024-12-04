import numpy as np

def eigenValues(matrix):
    # Memeriksa apakah matriks adalah persegi (M x N)
    if matrix.shape[0] == matrix.shape[1]:
        # Untuk matriks persegi, kita dapat menghitung nilai eigen secara langsung
        coefficients = np.poly(matrix)
        eigenValues = np.roots(coefficients)
        return np.unique(eigenValues).astype(float)
    else:
        # Matriks non-persegi, kita hitung nilai singular dengan cara manual

        # Menghitung A^T A dan A A^T
        AtA = np.dot(matrix.T, matrix)  # Matriks A^T A (N x N)
        AAt = np.dot(matrix, matrix.T)  # Matriks A A^T (M x M)

        # Menghitung eigenvalues dari A^T A atau A A^T
        eigenvalues_AtA = np.linalg.eigvals(AtA)
        
        # Nilai singular adalah akar kuadrat dari nilai eigen dari A^T A
        singular_values = np.sqrt(np.abs(eigenvalues_AtA))
        
        # Mengembalikan nilai singular (diurutkan dan dibulatkan)
        return np.sort(singular_values)

# Contoh matriks persegi (2x2)
matrix_square = np.array([[3, -2, 0], [-2, 3, 0], [0, 0, 5]])
eigen_square = eigenValues(matrix_square)
print("Eigen values (persegi):", eigen_square)

# Contoh matriks non-persegi (3x2)
matrix_non_square = np.array([[1, 1], [0, 1], [1, 0]])
eigen_non_square = eigenValues(matrix_non_square)
print("Singular values (non-persegi):", eigen_non_square)
