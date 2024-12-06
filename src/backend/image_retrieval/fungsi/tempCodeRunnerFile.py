rt numpy as np

# Fungsi untuk QR dekomposisi
def qr_decomposition(A):
    Q, R = np.linalg.qr(A)
    return Q, R

# Fungsi untuk menghitung nilai eigen dan eigenvektor menggunakan QR Iteration
def qr_eigenvalues_and_eigenvectors(A, max_iter=1000, tol=1e-10):
    A_k = A.copy()  # Matriks awal
    Q_all = np.eye(A.shape[0])  # Matriks identitas untuk menyimpan eigenvektor
    for i in range(max_iter):
        Q, R = qr_decomposition(A_k)
        A_k = R @ Q  # Matriks baru setelah QR dekomposisi
        Q_all = Q_all @ Q  # Mengumpulkan eigenvektor di setiap iterasi
        # Mengecek konvergensi (matriks semakin diagonal)
        if np.allclose(A_k - np.diag(np.diagonal(A_k)), 0, atol=tol):
            break
    
    # Nilai eigen ada di diagonal matriks yang telah dikonvergensi
    eigenvalues = np.diagonal(A_k)
    eigenvectors = Q_all  # Eigenvektor berada di kolom-kolom Q_all
    return eigenvalues, eigenvectors

# Contoh matriks A
A = np.array([[1, 1],[0, 1],[1, 0]])

Menghitung nilai eigen dan eigenvektor menggunakan QR Iteration
eigenvalues, eigenvectors = qr_eigenvalues_and_eigenvectors(A)

print("Nilai Eigen:", eigenvalues)
print("Eigenvektor:")
print(eigenvectors)

