import mido
import numpy as np
import shutil
import os
from mido.midifiles.meta import KeySignatureError
import librosa
import pretty_midi
import sounddevice as sd
from scipy.io.wavfile import write
import json
BASE_FOLDER = os.path.abspath('src/react-app/src/media')  # Sesuaikan dengan path proyek Anda

# ========================== MIDI VALIDATION ==========================

def is_valid_midi(file_path):
    """Validasi file MIDI apakah bisa dibaca dengan benar."""
    try:
        mido.MidiFile(file_path)
        return True
    except (EOFError, OSError, ValueError, KeySignatureError) as e:
        print(f"Error saat membaca file {file_path}: {str(e)}")
        return False


# ========================== MIDI PROCESSING =========================

import mido
import numpy as np

def process_midi(audio_path):
    """Ekstraksi melodi dari file MIDI dengan pengolahan yang lebih baik."""
    try:
        mid = mido.MidiFile(audio_path)
    except (EOFError, Exception) as e:
        print(f"Error saat memproses file {audio_path}: {str(e)}")
        return None

    # Ambil semua not dari setiap track, pilih 'note_on' dari semua track
    melody_notes = []
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.channel==1:
                melody_notes.append((msg.note, msg.time))

    if not melody_notes:
        print(f"Tidak ada melodi di dalam file: {audio_path}")
        return None

    # Tentukan ukuran window dan langkah sliding
    window_size = 40  # Ukuran window untuk melodi
    slide_size = 8    # Langkah pergeseran untuk window

    # Bagi data not menjadi windows (potongan data sekuensial)
    windows = [melody_notes[i:i + window_size] for i in range(0, len(melody_notes) - window_size + 1, slide_size)]

    hasil = []
    for window in windows:
        # Pisahkan pitch (not) dan durasi dari setiap not
        pitches = np.array([note[0] for note in window])
        durations = np.array([note[1] for note in window])

        # Normalisasi pitch dan durasi
        mean_pitch = pitches.mean() if len(pitches) > 0 else 0
        std_pitch = pitches.std() if len(pitches) > 0 else 1  # Hindari pembagian dengan nol
        norm_pitches = np.round((pitches - mean_pitch) / std_pitch * 100).astype(int)

        max_duration = durations.max() if len(durations) > 0 else 1
        norm_durations = np.round((durations / max_duration) * 100).astype(int)

        # Gabungkan pitch dan durasi yang telah dinormalisasi menjadi pasangan
        numeric = list(zip(norm_pitches, norm_durations))
        hasil.append(numeric)

    return hasil



# ========================== FEATURE EXTRACTION ========================

def extract_features(notes):
    """Ekstraksi fitur dari not-not yang ada di file MIDI."""
    pitches = np.array([note[0] for note in notes])

    # ATB: Histogram distribusi pitch
    hist_atb = np.histogram(pitches, bins=128, range=(0, 128), density=True)[0]

    # RTB: Histogram distribusi perbedaan pitch
    selisih_rtb = np.diff(pitches)
    hist_rtb = np.histogram(selisih_rtb + 127, bins=255, range=(0, 255), density=True)[0]

    # FTB: Histogram perbedaan pitch dari pitch pertama
    selisih_ftb = pitches - pitches[0] if len(pitches) > 0 else np.array([0])
    hist_ftb = np.histogram(selisih_ftb + 127, bins=255, range=(0, 255), density=True)[0]

    return np.concatenate([hist_atb, hist_rtb, hist_ftb])


# ========================== SIMILARITY MEASUREMENT ====================

def cosine_similarity(v1, v2):
    """Menghitung kesamaan cosine antara dua vektor."""
    dot_product = np.dot(v1, v2)
    magnitude = np.linalg.norm(v1) * np.linalg.norm(v2)
    return dot_product / magnitude if magnitude else 0


# ========================== DATABASE HANDLING =========================

def proses_database(midi_database_folder):
    """Proses seluruh file MIDI dalam folder dan buat database vektor fitur."""
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


# ========================== QUERY HANDLING ===========================

def query_by_humming(query_window, vektor_database):
    """Melakukan pencarian berdasarkan query MIDI yang diupload."""
    if not query_window:
        print({"message": "No melody found in MIDI file"})
        return None
    
    if not vektor_database:
        print("Vektor database kosong.")
        return None

    vektor_query = [extract_features(window) for window in query_window]
    results = []

    for query_vec in vektor_query:
        file_scores = [
            (filename, max(
                (cosine_similarity(query_vec, db_vec) for db_vec in db_vectors if not np.isnan(cosine_similarity(query_vec, db_vec))),
                default=0  # Default value when iterable is empty
            ))
            for filename, db_vectors in vektor_database
        ]
        results.append(file_scores)

    return results if results else None



# ========================== RESULT PROCESSING ========================

def olah_score_song(results):
    """Mengolah hasil pencarian dan menghitung skor rata-rata untuk setiap lagu."""
    if not results:
        print("Hasil kosong, tidak ada lagu yang ditemukan.")
        return

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


def print_top_similar_song(sorted_songs, top_n=5):
    """Menampilkan lagu-lagu yang paling mirip berdasarkan skor rata-rata."""
    if not sorted_songs:
        print("Tidak ada lagu yang ditemukan.")
        return

    top_songs = sorted_songs[:top_n]
    print(f"Top {top_n} lagu yang paling mirip:")
    for i, (song, score) in enumerate(top_songs, start=1):
        print(f"{i}. {song} - Skor similarity rata-rata: {score:.2f}")


# ========================== MIDI CONVERSION ==========================

def wav_to_midi(wav_file, midi_file, sr=22050):
    """
    Mengonversi file WAV menjadi file MIDI.

    Args:
        wav_file (str): Path ke file WAV input.
        midi_file (str): Path ke file MIDI output.
        sr (int): Sample rate untuk file WAV (default: 22050).
    """
    audio, sr = librosa.load(wav_file, sr=sr)
    
    # Deteksi pitch menggunakan fungsi librosa
    pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
    
    # Buat objek PrettyMIDI
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)  # Piano
    
    for time_idx in range(pitches.shape[1]):
        pitch_col = pitches[:, time_idx]
        if np.max(pitch_col) > 0:  # Ada pitch yang terdeteksi
            pitch_idx = np.argmax(pitch_col)
            pitch_hz = librosa.midi_to_hz(pitch_idx)
            pitch_midi = librosa.hz_to_midi(pitch_hz)  # Convert Hz to MIDI
            
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


# ========================== AUDIO RECORDING ==========================

def rekam_audio(durasi, nama_file, sample_rate=44100, channels=2):
    """Rekam audio dan simpan sebagai file WAV."""
    audio_data = sd.rec(int(durasi * sample_rate), samplerate=sample_rate, channels=channels, dtype='int16')
    sd.wait()  # Tunggu hingga rekaman selesai
    
    print("Rekaman selesai. Menyimpan file...")
    write(nama_file, sample_rate, audio_data)
    print(f"File rekaman tersimpan sebagai '{nama_file}'")


# ========================== DATABASE HANDLING (JSON) ==================

def save_json_in_batches(vektor_database, output_path, batch_size=100):
    """Menyimpan vektor database dalam format JSON secara bertahap."""
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
    """Memuat vektor database dari file JSON."""
    try:
        with open(input_path, 'r') as json_file:
            json_data = json.load(json_file)
        
        # Konversi kembali ke format list of tuples
        vektor_database = []
        for entry in json_data:
            filename = entry["filename"]
            vectors = []

            for vector in entry["vectors"]:
                vector_array = np.array(vector)
                vector_array = np.nan_to_num(vector_array, nan=0.0)
                vectors.append(vector_array)
            
            vektor_database.append((filename, vectors))
        
        print(f"Vektor database berhasil dibaca dari {input_path}")
        return vektor_database
    except Exception as e:
        print(f"Error saat membaca file JSON: {e}")
        return None


def update_midi_database(json_path, new_file_path):
    """
    Perbarui database MIDI dengan file baru.
    File baru akan dipindahkan ke folder music untuk memastikan integritas database.

    Args:
        json_path (str): Path ke file JSON database.
        new_file_path (str): Path ke file MIDI baru yang akan ditambahkan.

    Returns:
        None
    """
    # Pastikan folder `music` ada
    music_folder = os.path.join(BASE_FOLDER, 'music')
    if not os.path.exists(music_folder):
        os.makedirs(music_folder)

    # Pindahkan file MIDI yang di-upload ke folder `music`
    new_filename = os.path.basename(new_file_path)
    target_path = os.path.join(music_folder, new_filename)

    try:
        shutil.copy(new_file_path, target_path)
        print(f"File {new_filename} telah dipindahkan ke folder music.")
    except Exception as e:
        print(f"Error saat memindahkan file ke folder music: {e}")
        return

    # Muat database JSON jika ada, atau buat baru
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as f:
                vektor_database = json.load(f)
        except Exception as e:
            print(f"Error saat membaca file JSON: {e}")
            return
    else:
        vektor_database = []

    # Validasi file MIDI
    if not is_valid_midi(target_path):
        print("File MIDI tidak valid atau tidak dapat diproses.")
        return

    # Proses file MIDI untuk ekstraksi fitur
    processed_windows = process_midi(target_path)
    if not processed_windows:
        print("Tidak ada melodi yang terdeteksi dalam file MIDI.")
        return

    # Ekstrak fitur dari setiap window
    feature_vectors = [extract_features(window) for window in processed_windows]

    # Tambahkan entri baru ke database
    new_entry = {
        "filename": new_filename,
        "vectors": [vector.tolist() if isinstance(vector, np.ndarray) else vector for vector in feature_vectors]
    }
    vektor_database.append(new_entry)

    # Simpan database yang telah diperbarui kembali ke file JSON
    try:
        with open(json_path, 'w') as f:
            json.dump(vektor_database, f, indent=4)
        print(f"Database berhasil diperbarui dan disimpan ke {json_path}")
    except Exception as e:
        print(f"Error saat menyimpan database JSON: {e}")
