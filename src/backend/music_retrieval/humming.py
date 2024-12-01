import numpy as np
import os
from backend.music_retrieval.preprocessing import process_audio
from backend.music_retrieval.feature_extraction import extract_features
from backend.music_retrieval.similarity import compute_similarity

def music_retrieval_function(audio_file):
    pitches, magnitudes = process_audio(audio_file)
    features = extract_features(pitches, magnitudes)
    dataset_features = load_audio_dataset()
    similarities = compute_similarity(features, dataset_features)
    sorted_indices = similarities.argsort()[::-1]
    return sorted_indices

def load_audio_dataset(dataset_folder='dataset/audio/'):
    """
    Memuat fitur dari semua file audio dalam folder dataset.
    
    Args:
    - dataset_folder (str): Folder yang berisi file audio dataset.

    Returns:
    - dataset_features (numpy.array): Array 2D berisi fitur dari semua audio dalam dataset.
    """
    dataset_features = []

    # Iterasi melalui file-file dalam folder dataset audio
    for filename in os.listdir(dataset_folder):
        if filename.lower().endswith(('.wav','.midi')):  # Filter file audio
            file_path = os.path.join(dataset_folder, filename)
            
            try:
                # Proses audio dan ekstraksi fitur
                pitches, magnitudes = process_audio(file_path)
                features = extract_features(pitches)  # Ekstraksi fitur dari audio
                dataset_features.append(features)     # Menambahkan fitur ke dalam dataset_features
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # Mengonversi list fitur menjadi array numpy
    return np.array(dataset_features)
