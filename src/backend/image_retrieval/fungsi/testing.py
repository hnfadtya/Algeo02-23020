import numpy as np

def qr_decomposition(A):
    """ Melakukan dekomposisi QR pada matriks A menggunakan Gram-Schmidt """
    m, n = A.shape
    Q = np.zeros((m, n))  # Matriks ortogonal Q
    R = np.zeros((n, n))  # Matriks segitiga atas R
    
    for j in range(n):
        # Ambil kolom A[j] sebagai vektor
        v = A[:, j]
        
        # Proyeksikan v ke kolom-kolom Q sebelumnya
        for i in range(j):
            R[i, j] = np.dot(Q[:, i], v)
            v = v - R[i, j] * Q[:, i]
        
        # Normalisasi vektor untuk mendapatkan Q[:, j]
        R[j, j] = np.linalg.norm(v)
        Q[:, j] = v / R[j, j]
    
    return Q, R

def qr_iteration(A, max_iter=1000, tol=1e-6):
    """ Melakukan QR Iteration untuk mencari eigenvektor """
    A = A.copy()  # Menghindari perubahan pada matriks asli
    m, n = A.shape
    
    if m != n:
        raise ValueError("QR Iteration hanya dapat digunakan pada matriks persegi.")

    # Matriks untuk menyimpan eigenvektor
    Q_total = np.eye(n)
    
    for _ in range(max_iter):
        Q, R = qr_decomposition(A)
        A = np.dot(R, Q)  # Update A menjadi RQ
        Q_total = np.dot(Q_total, Q)
        
        # Periksa konvergensi: jika A mendekati diagonal
        off_diagonal_sum = np.sum(np.abs(A - np.diag(np.diagonal(A))))
        if off_diagonal_sum < tol:
            break
    
    # Eigenvektor adalah kolom-kolom Q_total
    return Q_total

def svd_eigenvectors(A):
    """ Menghitung eigenvektor menggunakan SVD """
    U, S, Vt = np.linalg.svd(A)
    
    # Eigenvektor dari A^T A adalah baris dari Vt (V transpos)
    eigenvectors_V = Vt.T
    
    # Eigenvektor dari A A^T adalah kolom dari U
    eigenvectors_U = U
    
    return eigenvectors_U, eigenvectors_V

# Contoh matriks NxN (misalnya matriks persegi 3x3)
A = np.array([[41, 12, 87],
              [62, 63, 98],
              [72, 21, 61]])

# Menghitung eigenvektor menggunakan SVD
eigenvectors_U, eigenvectors_V = svd_eigenvectors(A)
print("Eigenvektor menggunakan SVD (kolom-kolom U):\n", eigenvectors_U)

# Menghitung eigenvektor menggunakan QR Iteration
eigenvectors_qr = qr_iteration(A)
print("Eigenvektor menggunakan QR Iteration (kolom-kolom Q):\n", eigenvectors_qr)

# Membandingkan hasil
print("\nPerbandingan hasil (harus mirip):")
print("Eigenvektor SVD (U):\n", eigenvectors_U)
print("Eigenvektor QR Iteration (Q):\n", eigenvectors_qr)
