from PIL import Image
import numpy as np
import os

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
        img = img.convert('L')
        # Ubah ukuran gambar
        img = img.resize(size)
        # Ubah ke numpy array dan flatten
        return np.array(img).flatten()

def load_images_from_folder(folder_path, size=(100, 100)):
    """
    Memuat semua gambar dari folder tertentu:
    - Memproses setiap gambar di folder.
    - Mengembalikan array vektor gambar dan nama file-nya.
    """
    image_vectors = []
    filenames = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            full_path = os.path.join(folder_path, filename)
            try:
                image_vectors.append(process_image(full_path, size))
                filenames.append(filename)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    return np.array(image_vectors), filenames

# untuk testingnya
if __name__ == "__main__":
    vectors, filenames = load_images_from_folder("dataset/images/")
    print(f"Processed {len(vectors)} images.")
    print(f"First image vector: {vectors[0]}")
