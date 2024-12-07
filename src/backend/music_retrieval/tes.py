import os
from mir3 import process_midi, extract_features, cosine_similarity, proses_database, query_by_humming, print_top_similar_song
import numpy as np
from midi_json import save_json, load_json
# Lokasi file MIDI
TEST_MIDI_PATH = "C:/coding/Tingkat 2/Tubes Algeo 2/Algeo02-23020/src/backend/music_retrieval/Honey.3.mid"  # Ubah sesuai lokasi file MIDI Anda
DATABASE_FOLDER = "C:/coding/Tingkat 2/Tubes Algeo 2/Algeo02-23020/src/backend/music_retrieval/database"  # Ubah ke direktori database Anda

def test_process_midi():
    try:
        result = process_midi(TEST_MIDI_PATH)
        assert isinstance(result, list), "Hasil harus berupa list"
        print("test_process_midi: PASSED")
    except Exception as e:
        print(f"test_process_midi: FAILED\n{e}")

def test_extract_features():
    try:
        notes = [(60, 480), (62, 240), (64, 240)]  # Contoh input
        result = extract_features(notes)
        assert len(result) == 638, "Ukuran hasil tidak sesuai"
        print("test_extract_features: PASSED")
    except Exception as e:
        print(f"test_extract_features: FAILED\n{e}")

def test_cosine_similarity():
    try:
        v1 = [1, 2, 3]
        v2 = [4, 5, 6]
        result = cosine_similarity(v1, v2)
        assert isinstance(result, float), "Hasil harus berupa float"
        print("test_cosine_similarity: PASSED")
    except Exception as e:
        print(f"test_cosine_similarity: FAILED\n{e}")

# def test_proses_database():
#     try:
#         if not os.path.exists(DATABASE_FOLDER):
#             os.makedirs(DATABASE_FOLDER)
#         # Tambahkan file MIDI contoh di folder database
#         result = proses_database(DATABASE_FOLDER)
#         assert isinstance(result, np.ndarray), "Hasil harus berupa numpy array"
#         print("test_proses_database: PASSED")
#     except Exception as e:
#         print(f"test_proses_database: FAILED\n{e}")

def test_query_by_humming():
    try:
        if not os.path.exists(DATABASE_FOLDER):
            os.makedirs(DATABASE_FOLDER)
        result = query_by_humming(TEST_MIDI_PATH, DATABASE_FOLDER)
        print_most_similar_song(result)
        assert isinstance(result, list), "Hasil harus berupa list"
        print("test_query_by_humming: PASSED")
    except Exception as e:
        print(f"test_query_by_humming: FAILED\n{e}")

# Jalankan semua test
# test_process_midi()
# test_extract_features()
# test_cosine_similarity()

# test_query_by_humming()


#fungsi main


v_db =proses_database(DATABASE_FOLDER)
path_json = "vektor_database.json"
save_json(v_db, path_json )

vektor_database = load_json(path_json)
result = query_by_humming(TEST_MIDI_PATH, vektor_database )


print_top_similar_song(result)