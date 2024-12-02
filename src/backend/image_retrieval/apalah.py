import numpy as np
intensityMatrix = []
array1 = [1, 2, 3, 4]
array2 = [5, 6, 7, 8]
array3 = [9, 10, 11, 12]
array4 = [13, 14, 15, 16]

intensityMatrix.append(array1)
intensityMatrix.append(array2)
intensityMatrix.append(array3)
intensityMatrix.append(array4)
print(intensityMatrix)
print(intensityMatrix[1][1])
print(intensityMatrix[0])
print(intensityMatrix[1])
print(intensityMatrix[2])
print(intensityMatrix[3])

Matrix = []
array = [1, 1, 1, 1]
Matrix.append(array)
Matrix.append(array)
Matrix.append(array)
Matrix.append(array)
print(Matrix)

dot = np.dot(intensityMatrix, Matrix) 
print(dot)
dot = np.transpose(dot) 
print(dot)
Matrix = np.dot(Matrix, 2)
print(Matrix)

arr1 = [1, 2, -1]
arr2 = [2, 1, -1]
# arr1 = np.sort(arr1)
distances = []
for i in range(4):
    sum = 0
    for j in range(len(arr1)):
        sum += arr1[j]
    index = [i, sum]
    distances.append(index) 

print(distances)
for i in range(4):
    index = distances[i][0]
    print(index)
