# import numpy as np

# def svd(matrix):
#     # Matriks non-persegi
#     AtA = np.dot(matrix.T, matrix)  
#     AAt = np.dot(matrix, matrix.T) 
#     eigenValuesAAt = eigenValues(AtA)
#     vektorEigen = np.sort(eigenValuesAAt)[::-1]
#     print(vektorEigen)
#     for i in vektorEigen:
#             val = generateMatrixFromEigenvalue(i)
#             N = val.shape[0]
#             matrixZeros = np.zeros((N, 1))
#             print(matrixZeros)
#             print(val)
#             # koefisien = np.linalg.solve(val, matrixZeros)
            
#     # Nilai singular
#     singularValues = np.sqrt(np.abs(eigenValuesAAt))
#     singularValues = np.sort(singularValues)[::-1]
#     # Rumus A = U * Sigma * V Transpose
#     # Nilai Sigmanya
#     Sigma = np.zeros(matrix.shape)
#     np.fill_diagonal(Sigma, singularValues)
#     # Nilai V
    
#     return Sigma

# def eigenValues(matrix):
#     # Memeriksa apakah matriks adalah persegi (M x N)
#     if matrix.shape[0] == matrix.shape[1]:
#         coefficients = np.poly(matrix)
#         eigenValues = np.roots(coefficients)
#         return np.unique(eigenValues).astype(float)

# def generateMatrixFromEigenvalue(eigenvalue):
#     # Membuat matriks berdasarkan nilai eigen yang diberikan
#     lambda_val = eigenvalue
#     matrix = np.array([[lambda_val - 11, -1],
#                        [-1, lambda_val - 11]])
#     return matrix
    
    
# # Contoh matriks persegi (2x2)
# # matrix_square = np.array([[3, -2, 0], [-2, 3, 0], [0, 0, 5]])
# # U, Sigma, VT = singularValues(matrix_square)
# # print("U : ", U)
# # print("Sigma : ", Sigma)
# # print("VT : ", VT)

# # Contoh matriks non-persegi (3x2)
# matrix_non_square = np.array([[3, 1, 1], [-1, 3, 1]])
# Sigma= svd(matrix_non_square)
# print("Sigma : ", Sigma)


import numpy as np

def gauss_jordan(A):
    """
    Melakukan eliminasi Gauss-Jordan pada matriks A dan mengembalikan solusi dalam bentuk reduced row echelon form (RREF).
    """
    A = A.astype(float)  # Pastikan matriks berupa float
    rows, cols = A.shape
    
    for i in range(min(rows, cols)):
        # Jika pivot di baris i adalah nol, cari baris lain yang bisa dipakai
        if A[i, i] == 0:
            # Mencari baris dengan elemen non-zero di kolom yang sama
            for j in range(i + 1, rows):
                if A[j, i] != 0:
                    # Tukar baris i dan baris j
                    A[[i, j]] = A[[j, i]]
                    break
        
        # Membuat pivot menjadi 1
        if A[i, i] != 0:  # Periksa sebelum melakukan pembagian
            A[i] = A[i] / A[i, i]
        
        # Mengeliminasi elemen-elemen lainnya di kolom i
        for j in range(rows):
            if j != i and A[j, i] != 0:  # Jika ada elemen yang perlu dihapus
                A[j] = A[j] - A[j, i] * A[i]
    
    return A

def find_solution(A):
    # Mengubah matriks A menjadi bentuk RREF
    rref_A = gauss_jordan(A)
    
    # Tampilkan matriks RREF
    print("\nMatriks setelah Gauss-Jordan (RREF):")
    print(rref_A)
    
    # Periksa apakah ada kolom yang tidak mengandung pivot
    rows, cols = rref_A.shape
    
    # Jika ada kolom bebas, solusinya adalah parametrik
    if np.all(rref_A[:, -1] == 0) and np.any(rref_A[:, 0] == 0):
        print("\nSolusi parametrik ditemukan.")
        print("X1 = t, X2 = t (Solusi parametrik dengan t adalah parameter bebas).")
    else:
        # Jika tidak ada kolom bebas, solusi akan terdefinisi secara unik
        print("\nSolusi unik ditemukan.")
        print(f"X1 = {rref_A[0, -1]}, X2 = {rref_A[1, -1]}")

# Matriks yang diberikan [[-1, 1], [1, -1]]
A = np.array([[-1, 1], [1, -1]])

print("Matriks A:")
print(A)

# Menyelesaikan A * X = 0 menggunakan Gauss-Jordan dan mencari solusi
find_solution(A)
