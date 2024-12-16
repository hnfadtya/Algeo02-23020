import mido
import numpy as np
import os
from mido.midifiles.meta import KeySignatureError
import librosa
import pretty_midi
import sounddevice as sd
from scipy.io.wavfile import write
import json

def is_valid_midi(file_path):
    try:
        mido.MidiFile(file_path)
        return True
    except (EOFError, OSError, ValueError, KeySignatureError) as e:
        print(f"Error saat membaca file {file_path}: {str(e)}")
        return False

def process_midi(audio_path):
    try:
        mid = mido.MidiFile(audio_path)
    except (EOFError, Exception) as e:
        print(f"Error saat memproses file {audio_path}: {str(e)}")
        return None

    melody_notes = [(msg.note, msg.time) for track in mid.tracks for msg in track \
                    if msg.type == 'note_on' and msg.channel == 1]

    if not melody_notes:
        print(f"Tidak ada melodi di dalam file: {audio_path}")
        return None

    window_size = 40
    slide_size = 8
    windows = [melody_notes[i:i + window_size] \
               for i in range(0, len(melody_notes) - window_size + 1, slide_size)]

    hasil = []
    for window in windows:
        pitches = np.array([note[0] for note in window])
        durations = np.array([note[1] for note in window])

        mean_pitch = pitches.mean()
        std_pitch = pitches.std() or 1  # Avoid division by zero

        norm_pitches = np.round((pitches - mean_pitch) / std_pitch * 100).astype(int)
        max_duration = durations.max() or 1

        numeric = list(zip(norm_pitches, np.round((durations / max_duration) * 100).astype(int)))
        hasil.append(numeric)

    return hasil


def extract_features(notes):
    pitches = np.array([note[0] for note in notes])

    # ATB
    hist_atb = np.histogram(pitches, bins=128, range=(0, 128), density=True)[0]

    # RTB
    selisih_rtb = np.diff(pitches)
    hist_rtb = np.histogram(selisih_rtb + 127, bins=255, range=(0, 255), density=True)[0]

    # FTB
    selisih_ftb = pitches - pitches[0] if len(pitches) > 0 else np.array([0])
    hist_ftb = np.histogram(selisih_ftb + 127, bins=255, range=(0, 255), density=True)[0]

    return np.concatenate([hist_atb, hist_rtb, hist_ftb])

def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    magnitude = np.linalg.norm(v1) * np.linalg.norm(v2)
    return dot_product / magnitude if magnitude else 0

def proses_database(midi_database_folder):
    if not os.path.isdir(midi_database_folder):
        raise ValueError("Invalid database folder path.")

    vektor_database_gab = []
    for filename in os.listdir(midi_database_folder):
        file_path = os.path.join(midi_database_folder, filename)

        if os.path.isfile(file_path) and filename.endswith('.mid'):
            print(f"Memproses file: {file_path}")

            if not is_valid_midi(file_path):
                continue

            database_window = process_midi(file_path)
            if not database_window:
                continue

            db_vektor = [extract_features(window) for window in database_window]
            if db_vektor:
                vektor_database_gab.append((filename, db_vektor))

    return vektor_database_gab

def query_by_humming(query_window, vektor_database):
    if not query_window:
        print("Query kosong.")
        return None
    
    if not vektor_database:
        print("Vektor database kosong.")
        return None

    vektor_query = [extract_features(window) for window in query_window]
    results = []

    for query_vec in vektor_query:
        file_scores = [
            (filename, max(
                cosine_similarity(query_vec, db_vec) 
                for db_vec in db_vectors 
                if not np.isnan(cosine_similarity(query_vec, db_vec))  # Skip NaN values
            ))
            for filename, db_vectors in vektor_database
        ]
        results.append(file_scores)

    return results if results else None


def olah_score_song (results):
    if not results:
        print("Hasil kosong, tidak ada lagu yang ditemukan.")
        return

    # Gabungkan skor untuk setiap file
    similarity_scores = {}
    for window_scores in results:
        for filename, score in window_scores:
            if np.isnan(score):  # Skip NaN values
                continue
            if filename not in similarity_scores:
                similarity_scores[filename] = []
            similarity_scores[filename].append(score)

    # Hitung rata-rata skor untuk setiap file
    average_scores = {filename: sum(scores) / len(scores) for filename, scores in similarity_scores.items()}
    sorted_songs = sorted(
        average_scores.items(), 
        key=lambda x: x[1] if not np.isnan(x[1]) else float('-inf'), 
        reverse=True
    )

    return sorted_songs

def print_score_song(sorted_songs):
    print("Daftar lagu dengan skor similarity rata-rata:")
    for filename, avg_score in sorted_songs:
        print(f"{filename}: {avg_score:.2f}")

    # most_similar_song = max(average_scores, key=average_scores.get)
    # highest_score = average_scores[most_similar_song]

    # # Cetak hasil
    # print(f"Lagu yang paling mirip: {most_similar_song} dengan skor similarity rata-rata: {highest_score:.2f}")

def print_most_similar_song(sorted_songs):
    if sorted_songs:
        # Ambil lagu dengan skor tertinggi (top 1)
        song, score = sorted_songs[0]
        print(f"1. {song} - Skor similarity rata-rata: {score:.2f}")
    else:
        print("Tidak ada lagu yang ditemukan.")

def print_top_similar_song(sorted_songs, top_n):
    if not sorted_songs:  # Cek jika sorted_songs kosong atau None
        print("Tidak ada lagu yang ditemukan.")
        return
    # Ambil top N hasil
    top_songs = sorted_songs[:top_n]

    # Cetak hasil
    print(f"Top {top_n} lagu yang paling mirip:")
    for i, (song, score) in enumerate(top_songs, start=1):
        print(f"{i}. {song} - Skor similarity rata-rata: {score:.2f}")


#==========================convert to midi ===================================
def wav_to_midi(wav_file, midi_file, sr=22050):
    """
    Mengonversi file WAV menjadi file MIDI.

    Args:
        wav_file (str): Path ke file WAV input.
        midi_file (str): Path ke file MIDI output.
        sr (int): Sample rate untuk file WAV (default: 22050).
    """
    # Load file WAV
    audio, sr = librosa.load(wav_file, sr=sr)
    
    # Deteksi pitch menggunakan fungsi librosa
    pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
    
    # Buat objek PrettyMIDI
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)  # Piano
    
    # Iterasi setiap frame untuk mendeteksi pitch
    for time_idx in range(pitches.shape[1]):
        pitch_col = pitches[:, time_idx]
        if np.max(pitch_col) > 0:  # Ada pitch yang terdeteksi
            pitch_idx = np.argmax(pitch_col)
            # Konversi pitch ke MIDI note
            pitch_hz = librosa.midi_to_hz(pitch_idx)  # Dari index ke Hz
            pitch_midi = librosa.hz_to_midi(pitch_hz)  # Dari Hz ke MIDI
            
            # Pastikan pitch berada dalam rentang MIDI (0..127)
            if 0 <= pitch_midi <= 127:
                note = pretty_midi.Note(
                    velocity=100, 
                    pitch=int(pitch_midi), 
                    start=time_idx * librosa.frames_to_time(1, sr=sr),
                    end=(time_idx + 1) * librosa.frames_to_time(1, sr=sr)
                )
                instrument.notes.append(note)
    
    midi.instruments.append(instrument)
    midi.write(midi_file)
    print(f"MIDI file saved to {midi_file}")

#==========================mic to wav
def rekam_audio(durasi, nama_file, sample_rate=44100, channels=2):
    audio_data = sd.rec(int(durasi * sample_rate), samplerate=sample_rate, channels=channels, dtype='int16')
    sd.wait()  # Tunggu hingga rekaman selesai
    
    print("Rekaman selesai. Menyimpan file...")
    
    # Simpan ke file WAV
    write(nama_file, sample_rate, audio_data)
    
    print(f"File rekaman tersimpan sebagai '{nama_file}'")

#======================== midi to json =======================
def save_json_in_batches(vektor_database, output_path, batch_size=100):
    try:
        with open(output_path, 'w') as json_file:
            json_file.write('[')  # Mulai array JSON
            
            for i in range(0, len(vektor_database), batch_size):
                batch = vektor_database[i:i + batch_size]
                json_data = [
                    {
                        "filename": filename,
                        "vectors": [vector.tolist() if isinstance(vector, np.ndarray) else vector for vector in db_vectors]
                    }
                    for filename, db_vectors in batch
                ]
                
                json_file.write(json.dumps(json_data, indent=4)[1:-1])  # Hindari menulis array pembuka/tutup
                if i + batch_size < len(vektor_database):
                    json_file.write(',')  # Tambahkan koma di antara batch
                
            json_file.write(']')  # Akhiri array JSON
            
        print(f"Vektor database berhasil disimpan ke {output_path}")
    except Exception as e:
        print(f"Error saat menyimpan file JSON: {e}")


def load_json(input_path):

    try:
        with open(input_path, 'r') as json_file:
            json_data = json.load(json_file)
        
        # Konversi kembali ke format list of tuples
        vektor_database = []
        for entry in json_data:
            filename = entry["filename"]
            vectors = []

            for vector in entry["vectors"]:
                # Mengubah list ke np.array dan menangani NaN
                vector_array = np.array(vector)
                # Gantilah NaN dengan nilai default, misalnya 0 atau angka lain
                vector_array = np.nan_to_num(vector_array, nan=0.0)  # Mengganti NaN dengan 0

                vectors.append(vector_array)
            
            vektor_database.append((filename, vectors))
        
        print(f"Vektor database berhasil dibaca dari {input_path}")
        return vektor_database
    except Exception as e:
        print(f"Error saat membaca file JSON: {e}")
        return None

def update_midi_database(json_path, new_file_path):
    """
    Update the JSON database with a new file's vectors.

    Args:
        json_path (str): Path to the JSON database file.
        new_file_path (str): Path to the new MIDI file to be added.

    Returns:
        None
    """
    # Load existing JSON database
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as f:
                vektor_database = json.load(f)
        except Exception as e:
            print(f"Error saat membaca file JSON: {e}")
            return
    else:
        vektor_database = []

    # Validate and process new MIDI file
    if not is_valid_midi(new_file_path):
        print("File MIDI tidak valid atau tidak dapat diproses.")
        return

    processed_windows = process_midi(new_file_path)
    if not processed_windows:
        print("Tidak ada melodi yang terdeteksi dalam file MIDI.")
        return

    # Extract features from processed windows
    feature_vectors = [extract_features(window) for window in processed_windows]

    # Add new entry to database
    new_entry = {
        "filename": os.path.basename(new_file_path),
        "vectors": [vector.tolist() if isinstance(vector, np.ndarray) else vector for vector in feature_vectors]
    }
    vektor_database.append(new_entry)

    # Save updated database back to JSON
    try:
        with open(json_path, 'w') as f:
            json.dump(vektor_database, f, indent=4)
        print(f"Database berhasil diperbarui dan disimpan ke {json_path}")
    except Exception as e:
        print(f"Error saat menyimpan database JSON: {e}")
