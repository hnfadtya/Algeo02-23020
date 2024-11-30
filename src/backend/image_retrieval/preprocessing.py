import cv2
import numpy as np

def process_image(image_path, size=(100, 100)):
    image = cv2.imread(image_path)
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(grayscale, size)
    flattened = resized.flatten()
    return flattened

def load_images_from_folder(folder_path, size=(100, 100)):
    image_vectors, filenames = [], []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            full_path = os.path.join(folder_path, filename)
            image_vectors.append(process_image(full_path, size))
            filenames.append(filename)
    return np.array(image_vectors), filenames
