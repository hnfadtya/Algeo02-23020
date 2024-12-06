from PIL import Image
import numpy as np
import os

def process_image(image_path):
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
        img = img.convert("RGB")                
        arrayOfRGB = np.array(img)
        grayscaledArray = 0.2989 * arrayOfRGB[:, :, 0] + 0.5870 * arrayOfRGB[:, :, 1] + 0.1140 * arrayOfRGB[:, :, 2]
        img = img.
        grayscaledImage = Image.fromarray(grayscaledArray.astype("uint8"))
        resizedImage = grayscaledImage.resize((128, 128))

        # Ubah ke numpy array dan flatten
        return np.array(resizedImage).flatten()

# untuk testingnya
if __name__ == "__main__":
    folder_path = ("src/dataset/images/")
    intensityMatrix = []
    filenames = []
    # totalImages = len(filenames)
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            full_path = os.path.join(folder_path, filename)
            try:
                filenames.append(filename)
                intensityMatrix.append(process_image(full_path))
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print(f"Processed {len(filenames)} images.")
    for i in range(len(intensityMatrix)):
        print(f"image name: {filenames[i]}\n")
        print(f"image vector: {(intensityMatrix[i])}\n")
