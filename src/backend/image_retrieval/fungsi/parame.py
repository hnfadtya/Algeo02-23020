import numpy as np
import sympy as sym

# Matriks koefisien a dan vektor b
a = np.array([[45.13274595, -8, -7],
              [-8, 34.13274595 ,0],
              [-7, 0, 1.13274595],])

b = np.array([0, 0, 0])

# Mendapatkan jumlah variabel dan persamaan
num_equations, num_variables = a.shape

# Membuat array simbol untuk variabel x
x = sym.symarray('x', num_variables)

# Membuat persamaan linier dari hasil perkalian matriks a dan vektor x
equations = [sym.Eq(np.dot(a[i], x), b[i]) for i in range(num_equations)]

# Menyelesaikan sistem persamaan
solution = sym.solve(equations, x)

# Menampilkan hasil
print("Solusi Sistem Persamaan:")
print(solution)

# Menyelesaikan untuk ruang solusi (basis)
# Menggunakan metode pemrograman parametrik (solusi dalam bentuk variabel bebas)
null_space = sym.Matrix(a).nullspace()

# Menampilkan basis dari ruang solusi
print("\nBasis Ruang Solusi (Null Space):")
for vec in null_space:
    print(vec)
