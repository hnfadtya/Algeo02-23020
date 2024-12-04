import numpy as np

def custom_round(value, tol=1e-9):
    # Memeriksa apakah nilai sangat dekat dengan bilangan bulat
    if abs(value - round(value)) < tol:
        return round(value)  # Jika dekat dengan bilangan bulat, bulatkan
    return value  # Jika tidak, kembalikan nilai aslinya

# Fungsi untuk menerapkan custom_round ke seluruh elemen dalam matriks
def round_matrix(matrix, tol=1e-9):
    vectorized_round = np.vectorize(custom_round)  # Vectorize custom_round function
    return vectorized_round(matrix, tol)

# Contoh matriks
matrix = np.array([
    [-0.9999999999999982, 0.5, 1.0000000001],
    [2.9999999999, 3.0000000001, -0.9999999999]
])

# Terapkan custom_round ke seluruh matriks
rounded_matrix = round_matrix(matrix)

print(rounded_matrix)
