import numpy as np

def svd(matrix):
    # Matriks non-persegi
    # AtA = np.dot(np.transpose(matrix), matrix)  
    AAt = np.dot(matrix, np.transpose(matrix))
    # print(matrix)
    # print(matrix.T)
    # print(AAt)
    eigenValuesAAt = eigenValues(AAt)
    vektorEigenAAt = np.sort(eigenValuesAAt)[::-1]

    # eigenValuesAtA = eigenValues(AtA)
    # vektorEigenAtA = np.sort(eigenValuesAtA)[::-1]

    pertamaAAt = True
    # pertamaAtA = True

    #Singular Kiri
    for i in vektorEigenAAt:
        lambdaVal = custom_round(i)
        AAt = AAt * -1
        np.fill_diagonal(AAt, np.float64(lambdaVal + np.diagonal(AAt)))
        N = AAt.shape[0]
        matrixZeros = np.zeros((N, 1))
        AAt = np.hstack((AAt, matrixZeros))
        AAt = round_matrix(AAt)
        # print(AAt)
        result = driver_gauss_jordan_elimination(AAt)
        norm = np.linalg.norm(result)
        print(result)
        print(norm)
        result = result / norm
        if (pertamaAAt):
            vektorEigenAkhirAAt = result
            pertamaAAt = False
        else:
            vektorEigenAkhirAAt = np.vstack((vektorEigenAkhirAAt, result))
        AAt = np.dot(matrix, np.transpose(matrix)) 
     
    # Nilai singular
    # singularValues = np.sqrt(np.abs(eigenValuesAAt))
    # singularValues = np.sort(singularValues)[::-1]
    # Rumus A = U * Sigma * V Transpose
    # Nilai Sigmanya
    # Sigma = np.zeros(matrix.shape)
    # np.fill_diagonal(Sigma, singularValues)
    # singularValues = np.array([])
    # for i in vektorEigenAAt:
    #     lambdaVal = custom_round(i)
    #     singularValue = np.sqrt(np.abs(lambdaVal))
    #     singularValues = np.append(singularValues, singularValue)

    # Sigma = round_matrix(singularValues)
    # Nilai U
    # U = vektorEigenAkhirAAt
    
    return vektorEigenAkhirAAt

def eigenValues(matrix):
    # Memeriksa apakah matriks adalah persegi (M x N)
    if matrix.shape[0] == matrix.shape[1]:
        coefficients = np.poly(matrix)
        eigenValues = np.roots(coefficients)
        return np.unique(eigenValues).astype(float)
    

def gauss_jordan_elimination(matrix):
    n, m = matrix.shape
    has_free_variable = False
    idx_pivot = 0
    
    for i in range(n):
        while idx_pivot < m - 1 and abs(matrix[i, idx_pivot]) < 1e-9:
            if not switch_row(matrix, i):
                has_free_variable = True
                idx_pivot += 1
                if idx_pivot == m - 2:
                    break
        
        if idx_pivot == m - 2:
            break
        
        pivot = matrix[i, idx_pivot]
        if abs(pivot) > 1e-9:
            matrix[i] /= pivot
        
        for j in range(i + 1, n):
            if abs(matrix[j, idx_pivot]) > 1e-9:
                factor = matrix[j, idx_pivot] / matrix[i, idx_pivot]
                matrix[j] -= factor * matrix[i]
        
        for j in range(i - 1, -1, -1):
            if abs(matrix[j, idx_pivot]) > 1e-9:
                factor = matrix[j, idx_pivot]
                matrix[j] -= factor * matrix[i]
        
        idx_pivot += 1
    
    for i in range(n):
        if is_row_zero(matrix[i]) and abs(matrix[i, m - 1]) < 1e-9:
            has_free_variable = True
        
        if is_row_zero(matrix[i]) and abs(matrix[i, m - 1]) > 1e-9:
            return None
    
    # print_matrix(matrix)
    
    if has_free_variable:
        return parametric_back_substitution(matrix)
    else:
        return normal_back_substitution(matrix)

# Memeriksa apakah sebuah baris adalah baris nol
def is_row_zero(row):
    return np.allclose(row[:-1], 0)

# Mengubah baris jika elemen diagonal adalah nol
def switch_row(matrix, i):
    for row in range(i + 1, matrix.shape[0]):
        if matrix[row, i] != 0:
            matrix[[i, row]] = matrix[[row, i]]
            return True
    return False

# Menampilkan matriks
def print_matrix(matrix):
    for row in matrix:
        print(' '.join(f'{elem:.4f}' for elem in row))

# Fungsi substitusi mundur biasa
def normal_back_substitution(matrix):
    n = matrix.shape[0]
    solution = np.zeros(n)
    
    # Iterasi mundur untuk melakukan substitusi
    for i in range(n - 1, -1, -1):
        solution[i] = matrix[i, -1] - np.dot(matrix[i, i + 1:n], solution[i + 1:])
    
    return solution

# Fungsi substitusi mundur parametrik (Basis solusi parametrik)
def parametric_back_substitution(matrix):
    n, m = matrix.shape
    free_variables = []  # List untuk variabel bebas
    pivot_columns = []   # List untuk kolom pivot
    solutions = []       # Basis solusi parametrik
    
    # Menentukan kolom pivot
    for i in range(n):
        if np.count_nonzero(matrix[i, :-1]) > 0:
            pivot_columns.append(i)
    
    # Identifikasi variabel bebas (kolom tanpa pivot)
    for j in range(m - 1):
        if j not in pivot_columns:
            free_variables.append(j)
    
    # Menentukan basis solusi parametrik
    for var in free_variables:
        solution_vector = np.zeros(n)
        solution_vector[var] = 1  # Set variabel bebas = 1
        for i in range(n - 1, -1, -1):
            if matrix[i, var] != 0:
                solution_vector[i] = matrix[i, -1] - np.dot(matrix[i, i + 1:n], solution_vector[i + 1:])
        solutions.append(solution_vector)
    
    # Menampilkan basis solusi parametrik
    # for i, sol in enumerate(solutions):
    #     print(f"t{i + 1} * {sol}")
    
    return solutions

# Fungsi utama untuk mengambil input dan menjalankan eliminasi Gauss-Jordan
def driver_gauss_jordan_elimination(matrixInput):
    matrix = np.array(matrixInput, dtype=np.float64)
    result = gauss_jordan_elimination(matrix)
    if result is None:
        return "None"
    else:
        return result

def custom_round(value, tol=1e-9):
    # Memeriksa apakah nilai sangat dekat dengan bilangan bulat
    if abs(value - round(value)) < tol:
        return round(value)  # Jika dekat dengan bilangan bulat, bulatkan
    return value

def round_matrix(matrix, tol=1e-9):
    vectorized_round = np.vectorize(custom_round)  # Vectorize custom_round function
    return vectorized_round(matrix, tol)




matrix_non_square = np.array([[3,1,1], [-1, 3, 1]], dtype=np.float64)
U = svd(matrix_non_square)
print("1 Komponen U: \n",U)

matriksU, sigma, Vh = np.linalg.svd(matrix_non_square)
print("Komponen U: \n", matriksU)
print("Komponen Sigma : \n",sigma)


matrix_non_square = np.array([[1,1],[0,1],[1,0]], dtype=np.float64)
U = svd(matrix_non_square)
print("2 Komponen U: \n",U)
print("\n")

matriksU, sigma, Vh = np.linalg.svd(matrix_non_square)
print("Komponen U: \n", matriksU)
print("Komponen Sigma : \n",sigma)


# matrix_non_square = np.array([[1,2],[0,4],[7,0]], dtype=np.float64)
# U, Sigma= svd(matrix_non_square)
# print("Komponen U: \n",U)
# print("Komponen Sigma : \n",Sigma)

# matriksU, sigma, Vh = np.linalg.svd(matrix_non_square)
# print("Komponen U: \n", matriksU)
# print("Komponen Sigma : \n",sigma)
