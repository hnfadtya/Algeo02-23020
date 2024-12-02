from PIL import Image
import numpy as np
import os
import cv2 as cv



def process_image(image_path, size=(100, 100)):
    """
    Memproses gambar:
    - Membuka gambar dari file.
    - Mengubah ke grayscale.
    - Mengubah ukuran gambar ke ukuran tertentu.
    - Mengonversi ke vektor numpy.
    """
    # Buka gambar menggunakan Pillow
    with Image.open(image_path) as img:
        # Konversi ke grayscale
        X = Image. #lebar sebuah gambar = N
        Y = Image. #lebar sebuah gambar = M
        for i in range(X):
            for j in range(Y):
                img = grayscaling(X, Y)
                
        # Ubah ukuran gambar
        img = img.resize(size)
        # Ubah ke numpy array dan flatten
        return np.array(img).flatten()



def grayscaling(X, Y):
    # membuat gambar menjadi grayscale
    # _grey = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    R = (X,Y)
    G = (X,Y)
    B = (X,Y)
    I = 0.2989*R + 0.5870*G + 0.1140*B
    return I

def DataSetToMatrix(dir):
    S = []
    FileNames = []
    for filename in os.listdir(dir):
        temp = ImgToMatrix(f'{dir}/{filename}')
        S += [temp]
        FileNames += [filename]
    return S, FileNames

def getAllDir():
    S = []
    dir = '../datasets'
    for filename in os.listdir(dir):
        S += [filename]
    return S

def FolderToMatrix(dir):
    S = []
    for i in range(len(dir)):
        temp = DataSetToMatrix(f'../datasets/{dir[i]}')
        S += [temp]
    return S


# untuk testingnya
if __name__ == "__main__":
    vectors, filenames = load_images_from_folder("dataset/images/")
    print(f"Processed {len(vectors)} images.")
    print(f"First image vector: {vectors[0]}")
