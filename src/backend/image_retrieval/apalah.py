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

def A_to_Q(matriks):
    Q = []
    tempMat = []

    for i in range(len(matriks)):
        tempMat.append(matriks[i])
        
    for i in range(len(matriks)):
        ak = GetVectorK(tempMat,i)
        if (i == 0):
            temp = GetVectorK(tempMat,i)
            Q.extend([VektorSatuan(temp)])
        else:
            temp = ak
            for j in range (i):
                ej = GetVectorK(np.transpose(Q),j)
                ej = VektorSatuan(ej)
                temp = np.subtract(temp,DotProduct(ak,ej)*ej)
            Q.extend([VektorSatuan(temp)])

    Q = np.array(Q)
    Q = np.transpose(Q)
    return Q

def A_to_R(Q, A):
    # Make transpose
    R = [[0 for i in range(len(A[0]))] for j in range(len(A))]
    temp = Q
    skip = 0
    for i in range(len(A)):
        for j in range(len(A[0])):
            if (j<skip):
                R[i][j] = 0
            else:
                ai = GetVectorK(A,j)
                ei = GetVectorK(Q,i)
                R[i][j] = np.dot(ai,ei)
        skip +=1
    return R
def VektorSatuan(M):
    # convert numpy array to normal array
    temp = []
    for i in range(len(M)):
        temp.append(M[i])

    sum = np.linalg.norm(temp)

    for i in range (len(M)):
        temp[i] = temp[i] / sum
    temp = np.array(temp)

    return temp
    
def DotProduct(M,N):
    sum = 0
    for i in range (len(M)):
        sum = sum + M[i] * N[i]
    return sum

def GetVectorK(matriks, k):
    temp = []
    for i in range(len(matriks)):
        temp.append(matriks[i][k])
    temp = np.array(temp)
    return temp

def getEigen(A):
    # Mengembalikan EigenValue dan EigenVector
    
    # Eigen Value dalam bentuk Matriks
    EigenValMat = []
    for i in range(len(A)):
        EigenValMat.append(A[i])
    
    # buat matriks diagonal seukuran A untuk Eigen Vector
    EigenVec = [[0 for i in range(len(A[0]))] for j in range(len(A))]
    for i in range(len(EigenVec)):
        for j in range(len(EigenVec[0])):
            if(i == j):
                EigenVec[i][j] = 1

    # Iterasi sebanyak 20 kali untuk konvergen
    for i in range(20):
        # print(f"{(i+1)*100/20}%")
        # print("Start Q")
        Q = A_to_Q(EigenValMat)
        # print("Start R")
        R = A_to_R(Q,EigenValMat)
        EigenVec = np.dot(EigenVec, Q)
        EigenValMat = np.dot(R,Q)
        # print(f"Done {(i+1)*100/20}%")

    # simpan Eigen Value dari EigenValMat dalam EigenVal
    EigenVal = []
    for i in range(len(EigenValMat)):
        for j in range(len(EigenValMat)):
            if (i == j):
                EigenVal.append(EigenValMat[i][j])
    
    EigenVal = np.array(EigenVal)

    return EigenVal, EigenVec
arr1 = [1, 2, -1]
arr2 = [2, 1, -1]
mat = []
mat.append(arr1)
mat.append(arr2)
val, vector = getEigen(mat)
print(val)
print(vector)