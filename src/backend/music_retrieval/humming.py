import librosa
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
