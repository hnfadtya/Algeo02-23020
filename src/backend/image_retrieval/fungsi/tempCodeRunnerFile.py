def eigenValues(matrix):
    coefficients = np.poly(matrix)
    eigenValues = np.roots(coefficients)
    return eigenValues

matrix = array([[3, -2, 0], [-2, 3, 0], [0, 0, 5]])
eigen = eigenValues(matrix)
print(eigen)