
import mido
import numpy as np
import math
import os
def process_midi(audio_path):
    # Load MIDI
    try:
        mid = mido.MidiFile(audio_path)
    except Exception as e:
        raise ValueError(f"Error loading MIDI file: {e}")

    melody_notes = []
    window_size = 40
    slide_size = 8

    # Ekstraksi note dari channel tertentu
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.channel == 1:  # Channel 1 digunakan
                melody_notes.append((msg.note, msg.time))

    if not melody_notes:
        raise ValueError("No melody notes found in the given MIDI file.")

    # Bagi melodi jadi segmen 20-40 beat
    windows = [
        melody_notes[i: i + window_size]
        for i in range(0, len(melody_notes) - window_size + 1, slide_size)
    ]

    hasil = []

    # Proses setiap window
    for window in windows:
        pitches = [note[0] for note in window]
        mean_pitch = np.mean(pitches)
        std_pitch = np.std(pitches) or 1  # Supaya tidak nol

        norm_window = [
            ((note[0] - mean_pitch) / std_pitch * 100, note[1])
            for note in window
        ]

        # Konversi ke representasi numerik
        durasi = [note[1] for note in norm_window]
        max_durasi = max(durasi) if durasi else 1

        numeric = [
            (round(norm_pitch), round((duration / max_durasi) * 100))
            for norm_pitch, duration in norm_window
        ]
        hasil.append(numeric)

    return hasil


def extract_features(notes):
    pitches = [note[0] for note in notes]

    # Histogram Absolute Tone Bins (ATB)
    hist_atb = np.zeros(128)
    for pitch in pitches:
        if 0 <= pitch < 128:
            hist_atb[pitch] += 1
    hist_atb /= sum(hist_atb) or 1

    # Histogram Relative Tone Bins (RTB)
    selisih_rtb = [pitches[i] - pitches[i - 1] for i in range(1, len(pitches))]
    hist_rtb = np.zeros(255)
    for diff in selisih_rtb:
        index = diff + 127
        if 0 <= index < 255:
            hist_rtb[index] += 1
    hist_rtb /= sum(hist_rtb) or 1

    # Histogram First Tone Bins (FTB)
    first_tone = pitches[0] if pitches else 0
    selisih_ftb = [pitch - first_tone for pitch in pitches]
    hist_ftb = np.zeros(255)
    for diff in selisih_ftb:
        index = diff + 127
        if 0 <= index < 255:
            hist_ftb[index] += 1
    hist_ftb /= sum(hist_ftb) or 1

    return np.concatenate([hist_atb, hist_rtb, hist_ftb])

def cosine_similarity(v1, v2):
    # Memastikan kedua vektor memiliki panjang yang sama
    if len(v1) != len(v2):
        raise ValueError(f"Vectors must have the same length. Got {len(v1)} and {len(v2)}.")

    dot_product = np.dot(v1, v2)
    magnitude_v1 = np.linalg.norm(v1)
    magnitude_v2 = np.linalg.norm(v2)

    if magnitude_v1 == 0 or magnitude_v2 == 0:
        raise ValueError("Zero vector found; cannot compute cosine similarity.")

    return dot_product / (magnitude_v1 * magnitude_v2)





def proses_database(midi_database_folder):
    if not os.path.isdir(midi_database_folder):
        raise ValueError("Invalid database folder path.")

    vektor_database_gab = []

    for filename in os.listdir(midi_database_folder):
        file_path = os.path.join(midi_database_folder, filename)

        if os.path.isfile(file_path) and filename.endswith('.mid'):
            print(f"Processing file: {file_path}")
            db_vektor = []
            try:
                database_window = process_midi(file_path)
                for window in database_window:
                    vektor = extract_features(window)
                    db_vektor.append(vektor)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue

            # Mengubah db_vektor menjadi array NumPy
            db_vektor = np.array(db_vektor, dtype=object)  # Memastikan array seragam
            vektor_database_gab.append(db_vektor)

    # Mengonversi vektor database menjadi array NumPy
    vektor_database_gab = np.array(vektor_database_gab, dtype=object)  # pastikan array ini seragam

    return vektor_database_gab



def query_by_humming(midi_query_path, midi_database_folder):
    try:
        query_window = process_midi(midi_query_path)
    except Exception as e:
        raise ValueError(f"Error processing query MIDI: {e}")

    vektor_query = [extract_features(window) for window in query_window]
    vektor_database = proses_database(midi_database_folder)

    results = []
    for query in vektor_query:
        scores = []
        for db_vec in vektor_database:
            # Memastikan db_vec adalah array 1D atau list untuk setiap vektor dalam database
            for vec in db_vec:  # Karena database adalah list of lists
                score = cosine_similarity(query, vec)
                scores.append(score)
        results.append(max(scores))  # Simpan skor tertinggi untuk setiap window query

    return results



# def similarity(query, database):
#     vektor_query= extract_features(process_midi (query))
#     vektor_database= extract_features(process_midi (database))
#     sim = cosine_similarity (vektor_query.reshape(1, -1),vektor_database)

#     return (sim)


# def compute_similarity(query_features, database_features):
#     """
#     Menghitung similaritas antara vektor fitur query dan database menggunakan cosine similarity.
#     """
#     similarities = cosine_similarity(query_features.reshape(1, -1), database_features)
#     return similarities.flatten()



    # Proses query
    # query_windows = process_midi(midi_query)
    # query_features = [extract_features(window) for window in query_windows]
    
    # Proses database
    # database_features = []
    # for midi_data in midi_database:
    #     db_windows = process_midi(midi_data)
    #     db_features = [extract_features(window) for window in db_windows]
    #     database_features.extend(db_features)
    
    # database_features = np.array(database_features)
    
    # Hitung Similaritas
    # results = []
    # for query in query_features:
    #     similarity_scores = compute_similarity query, database_features)
    #     results.append(similarity_scores)
    
    # return results

#---------------------------------------------------------------------------


midi_query_path = r"C:/coding/Tingkat 2/Tubes Algeo 2/Algeo02-23020/src/backend/music_retrieval/database/file1.mid"
midi_database_folder = r"C:/coding/Tingkat 2/Tubes Algeo 2/Algeo02-23020/src/backend/music_retrieval/database"
# Eksekusi
try:
    
    result = proses_database (midi_database_folder)
    print (result)


except FileNotFoundError:
    print(f"File MIDI tidak ditemukan: {midi_path}")
except Exception as e:
    print(f"Terjadi kesalahan: {e}")


