# # import numpy as np

# # def svd(matrix):
# #     # Matriks non-persegi
# #     AtA = np.dot(matrix.T, matrix)  
# #     AAt = np.dot(matrix, matrix.T) 
# #     eigenValuesAtA = eigenValues(AtA)
# #     eigenValuesAAt = eigenValues(AtA)
# #     # Nilai singular
# #     singularValues = np.sqrt(np.abs(eigenValuesAtA))
# #     singularValues = np.sort(singularValues)[::-1]
# #     # Rumus A = U * Sigma * V Transpose
# #     # Nilai Sigmanya
# #     Sigma = np.zeros(matrix.shape)
# #     np.fill_diagonal(Sigma, singularValues)
# #     # Nilai V
# #     V = np.array([solveEigenvector(AtA, 0) for val in eigenValuesAtA])
# #     U = np.array([solveEigenvector(AAt, 0) for val in eigenValuesAAt])
    
# #     return U, Sigma, V.T

# # def eigenValues(matrix):
# #     # Memeriksa apakah matriks adalah persegi (M x N)
# #     if matrix.shape[0] == matrix.shape[1]:
# #         coefficients = np.poly(matrix)
# #         eigenValues = np.roots(coefficients)
# #         return np.unique(eigenValues).astype(float)

# # def rowReduce(matrix):
# #     """ Fungsi untuk melakukan eliminasi Gauss pada matriks """
# #     matrix = matrix.astype(float)  # Pastikan kita bekerja dengan tipe data float
# #     rows, cols = matrix.shape
# #     for i in range(min(rows, cols)):
# #         # Cari baris dengan elemen terbesar di kolom i (untuk stabilitas numerik)
# #         max_row = np.argmax(np.abs(matrix[i: , i])) + i
# #         matrix[[i, max_row]] = matrix[[max_row, i]]
        
# #         # Cek apakah pivot element adalah nol atau sangat kecil
# #         if np.abs(matrix[i, i]) < 1e-10:
# #             continue  # Lewati baris ini jika elemen pivot terlalu kecil atau nol
        
# #         # Normalisasi baris i
# #         matrix[i] = matrix[i] / matrix[i, i]
        
# #         # Eliminasi elemen-elemen di bawahnya
# #         for j in range(i+1, rows):
# #             matrix[j] = matrix[j] - matrix[j, i] * matrix[i]
    
# #     # Back substitution untuk mengurangi menjadi matriks eselon tereduksi
# #     for i in range(min(rows, cols)-1, -1, -1):
# #         for j in range(i-1, -1, -1):
# #             matrix[j] = matrix[j] - matrix[j, i] * matrix[i]
    
# #     return matrix


# # def solveEigenvector(matrix, eigenvalue):
# #     """ Menyelesaikan sistem linier (A - λI) v = 0 dengan eliminasi Gauss """
# #     n = matrix.shape[0]
# #     I = np.eye(n)
# #     A_lambda = matrix - eigenvalue * I  # Matriks A - λI
    
# #     # Menggunakan row reduction untuk menemukan null space (vektor eigen)
# #     reduced_matrix = rowReduce(A_lambda)
    
# #     # Vektor eigen adalah solusi non-trivial (vektor bebas)
# #     # Ambil kolom terakhir dari reduced_matrix sebagai vektor eigen
# #     # Kita anggap baris yang tidak tereliminasi sebagai bebas
# #     eigenvector = np.zeros(n)
# #     eigenvector[-1] = 1  # Assign 1 pada posisi bebas
# #     return eigenvector

    
    
# # # Contoh matriks persegi (2x2)
# # # matrix_square = np.array([[3, -2, 0], [-2, 3, 0], [0, 0, 5]])
# # # U, Sigma, VT = singularValues(matrix_square)
# # # print("U : ", U)
# # # print("Sigma : ", Sigma)
# # # print("VT : ", VT)

# # # Contoh matriks non-persegi (3x2)
# # matrix_non_square = np.array([[3, 1, 1], [-1, 3, 1]])
# # U, Sigma, VT = svd(matrix_non_square)
# # print("U : ", U)
# # print("Sigma : ", Sigma)
# # print("VT : ", VT)

# # A_reconstructed = np.dot(U, np.dot(Sigma, VT))
# # print("\nMatriks A yang direkonstruksi:")
# # print(A_reconstructed)
# import numpy as np

# # Fungsi untuk melakukan eliminasi Gauss-Jordan
# def gauss_jordan_elimination(matrix):
#     n, m = matrix.shape
#     has_free_variable = False
#     idx_pivot = 0
    
#     for i in range(n):
#         while idx_pivot < m - 1 and abs(matrix[i, idx_pivot]) < 1e-9:
#             if not switch_row(matrix, i):
#                 has_free_variable = True
#                 idx_pivot += 1
#                 if idx_pivot == m - 2:
#                     break
        
#         if idx_pivot == m - 2:
#             break
        
#         pivot = matrix[i, idx_pivot]
#         if abs(pivot) > 1e-9:
#             matrix[i] /= pivot
        
#         for j in range(i + 1, n):
#             if abs(matrix[j, idx_pivot]) > 1e-9:
#                 factor = matrix[j, idx_pivot] / matrix[i, idx_pivot]
#                 matrix[j] -= factor * matrix[i]
        
#         for j in range(i - 1, -1, -1):
#             if abs(matrix[j, idx_pivot]) > 1e-9:
#                 factor = matrix[j, idx_pivot]
#                 matrix[j] -= factor * matrix[i]
        
#         idx_pivot += 1
    
#     for i in range(n):
#         if is_row_zero(matrix[i]) and abs(matrix[i, m - 1]) < 1e-9:
#             has_free_variable = True
        
#         if is_row_zero(matrix[i]) and abs(matrix[i, m - 1]) > 1e-9:
#             print("Tidak ditemukan solusi unik")
#             return None
    
#     print("\nMatrix akhir:")
#     print_matrix(matrix)
    
#     if has_free_variable:
#         print("Ditemukan solusi parametrik")
#         return parametric_back_substitution(matrix)
#     else:
#         return normal_back_substitution(matrix)

# # Memeriksa apakah sebuah baris adalah baris nol
# def is_row_zero(row):
#     return np.allclose(row[:-1], 0)

# # Mengubah baris jika elemen diagonal adalah nol
# def switch_row(matrix, i):
#     for row in range(i + 1, matrix.shape[0]):
#         if matrix[row, i] != 0:
#             matrix[[i, row]] = matrix[[row, i]]
#             return True
#     return False

# # Menampilkan matriks
# def print_matrix(matrix):
#     for row in matrix:
#         print(' '.join(f'{elem:.4f}' for elem in row))

# # Fungsi substitusi mundur biasa
# def normal_back_substitution(matrix):
#     n = matrix.shape[0]
#     solution = np.zeros(n)
    
#     # Iterasi mundur untuk melakukan substitusi
#     for i in range(n - 1, -1, -1):
#         solution[i] = matrix[i, -1] - np.dot(matrix[i, i + 1:n], solution[i + 1:])
    
#     return solution

# # Fungsi substitusi mundur parametrik (Basis solusi parametrik)
# def parametric_back_substitution(matrix):
#     n, m = matrix.shape
#     free_variables = []  # List untuk variabel bebas
#     pivot_columns = []   # List untuk kolom pivot
#     solutions = []       # Basis solusi parametrik
    
#     # Menentukan kolom pivot
#     for i in range(n):
#         if np.count_nonzero(matrix[i, :-1]) > 0:
#             pivot_columns.append(i)
    
#     # Identifikasi variabel bebas (kolom tanpa pivot)
#     for j in range(m - 1):
#         if j not in pivot_columns:
#             free_variables.append(j)
    
#     # Menentukan basis solusi parametrik
#     for var in free_variables:
#         solution_vector = np.zeros(n)
#         solution_vector[var] = 1  # Set variabel bebas = 1
#         for i in range(n - 1, -1, -1):
#             if matrix[i, var] != 0:
#                 solution_vector[i] = matrix[i, -1] - np.dot(matrix[i, i + 1:n], solution_vector[i + 1:])
#         solutions.append(solution_vector)
    
#     # Menampilkan basis solusi parametrik
#     print("Basis solusi parametrik:")
#     for i, sol in enumerate(solutions):
#         print(f"t{i + 1} * {sol}")
    
#     return solutions

# # Fungsi utama untuk mengambil input dan menjalankan eliminasi Gauss-Jordan
# def driver_gauss_jordan_elimination():
#     print("Masukkan jumlah baris dan kolom matriks augmented:")
#     rows = int(input("Jumlah baris: "))
#     cols = int(input("Jumlah kolom: "))
    
#     matrix = np.zeros((rows, cols))  # Matriks augmented (termasuk kolom hasil)
    
#     print("Masukkan elemen-elemen matriks:")
#     for i in range(rows):
#         row = list(map(float, input(f"Masukkan baris {i + 1} (pisahkan dengan spasi): ").split()))
#         matrix[i] = row
    
#     result = gauss_jordan_elimination(matrix)
#     if result is None:
#         return "Tidak ada solusi unik"
#     else:
#         return result

# # Fungsi main
# if __name__ == '__main__':
#     result = driver_gauss_jordan_elimination()
#     print("Hasil:", result)


import numpy as np

def gauss_jordan_basis(matrix):
    n, m = matrix.shape
    augmented_matrix = matrix.astype(float)

    # Reduksi Gauss-Jordan untuk mendapatkan RREF
    for i in range(n):
        # Cek apakah pivot pada augmented_matrix[i, i] adalah nol
        if augmented_matrix[i, i] == 0:
            # Coba tukar baris dengan baris berikutnya yang tidak nol di kolom ini
            for j in range(i + 1, n):
                if augmented_matrix[j, i] != 0:
                    augmented_matrix[[i, j]] = augmented_matrix[[j, i]]
                    break
            # Jika tidak ada baris yang bisa ditukar, lanjutkan ke langkah berikutnya
            else:
                continue

        # Normalisasi baris i sehingga elemen pivot menjadi 1
        augmented_matrix[i] /= augmented_matrix[i, i]

        # Eliminasi elemen-elemen lainnya di kolom i
        for j in range(n):
            if j != i:
                augmented_matrix[j] -= augmented_matrix[i] * augmented_matrix[j, i]

    # Menampilkan matriks yang tereduksi
    print("Matriks yang tereduksi (RREF):")
    print(augmented_matrix)

    # Identifikasi variabel bebas dan pivot
    pivot_columns = []  # Kolom yang memiliki pivot
    free_variables = []  # Variabel bebas

    # Menentukan kolom pivot
    for i in range(n):
        if np.count_nonzero(augmented_matrix[i, :-1]) > 0:
            pivot_columns.append(i)

    # Menentukan variabel bebas
    for i in range(m - 1):
        if i not in pivot_columns:
            free_variables.append(i)

    print("\nPivot Columns:", pivot_columns)
    print("Free Variables:", free_variables)

    # Mencari basis solusi parametrik
    basis = []
    for free_var in free_variables:
        # Untuk setiap variabel bebas, buat vektor basis
        basis_vector = np.zeros(n)
        basis_vector[free_var] = 1  # Set variabel bebas = 1
        for i in range(n - 1, -1, -1):
            if augmented_matrix[i, free_var] != 0:
                basis_vector[i] = augmented_matrix[i, -1] - np.dot(augmented_matrix[i, i + 1:n], basis_vector[i + 1:])
        basis.append(basis_vector)

    print("\nBasis Solusi Parametrik:")
    for b in basis:
        print(b)

    return basis

# Contoh sistem persamaan linier dengan solusi parametrik
A = np.array([[1 , -1, -2],
              [-1 , 2, 0],
              [0 , 0, 2]], dtype=float)

basis = gauss_jordan_basis(A)
