import numpy as np
import InputImage as II
import os
# import cv2 as cv

def SumOfMatrix(M1, M):
    for i in range(len(M)):
        for j in range(len(M[0])):
            M[i][j] += M1[i][j]

def RataRataMatrix(S):
    M = len(S)
    sumofmatriks = [[0 for j in range(len(S[0][0]))] for i in range(len(S[0]))]
    for matriks in S:
        SumOfMatrix(matriks, sumofmatriks)
    for i in range (len(sumofmatriks[0])):
        for j in range(len(sumofmatriks)):
            sumofmatriks[j][i] /= M
    return sumofmatriks

#cari selisih
def Selisih(S,data):
    sp = np.array(S)
    d = np.array([[[0 for j in range (len(S[0][0]))] for i in range (len(S[0]))] for k in range (data)])
    mp = np.array(RataRataMatrix(S))
    for i in range (data):
        d[i] = np.subtract(sp[i],mp)
    return d
sel = [[1,2,3],[1,2,3],[1,2,3]]
    
def kovarian(S,data):
    sp = np.array(S)
    k = np.array([S[0]])
    for i in range(1,data):
        k = np.concatenate((k,[sp[i]]),axis = 0)
    kt = np.transpose(k)
    kt = kt[0]
    k = np.transpose(kt)
    c = np.dot(k, kt)
    return c