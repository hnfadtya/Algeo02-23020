
import mido
import numpy as np


def process_midi (audio_path):
    # Load MIDI
    mid = mido.MidiFile(audio_path)
    melody_notes = []
    window_size = 40
    slide_size = 8
    
    for track in mid.tracks:
        for msg in track:
            print (msg)
            if msg.type == 'note_on' and msg.channel == 1:  # Ngambil channel 1 doang
                melody_notes.append((msg.note, msg.time))
    #melody_note [(note, time)]
    # Bagi Melofi jadi segmen 20-40 beat
    windows = []
    for i in range (0, len(melody_notes) - window_size + 1, slide_size):
        windows.append(melody_notes[i: i + window_size])
    
    # Proses setiap window
    hasil = []

    for window in windows:
        # Normalisasi pitch
        #ngambil notes doang timenya ga
        pitches = [note[0] for note in window]
        
        mean_pitch = np.mean(pitches)
        std_pitch = np.std(pitches)

        #supaya std tidak 0 kalau seragam
        if std_pitch == 0:
            std_pitch = 1 

        norm_window = []  

        for note in window:
            pitch = note[0]  
            duration = note[1] 
            
            # Hitung pitch yang dinormalisasi
            norm_pitch = (pitch - mean_pitch) / std_pitch  
            norm_pitch = round(norm_pitch, 2)
            
            # Tambahkan hasil ke daftar
            norm_window.append((norm_pitch, duration))

        
        # Konversi ke representasi numerik
        durasi = [note[1] for note in norm_window]

        if duration :
            max_durasi = max(durasi)
        else:
            max_durasi = 1
        
        numeric = []  

        # Iterasi setiap not dalam normalized_window
        for note, duration in zip(norm_window, durasi):
            norm_pitch = note[0]  
            norm_duration = duration / max_durasi  
            numeric.append((norm_pitch, norm_duration))  

        hasil.append(numeric)
    
    return hasil

def extract_features(notes):

    pitches = [note[0] for note in notes]
    
    # ATB
    hist_atb = [0 for i in range (128)]
    count_atb = 0
    for pitch in pitches:
        if pitch >=0 and pitch<128:
            hist_atb[pitch] +=1
            count_atb +=1
    
    if count_atb >0:
        for i in range (128):
            hist_atb[i] =( hist_atb[i] / count_atb)
    
    # RTB
    selisih_rtb = []
    for i in range(1, len(pitches)):
        selisih_rtb.append(pitches[i] - pitches[i - 1])
    
    hist_rtb = [0 for _ in range (255)]
    count_rtb = 0
    for beda in selisih_rtb:
        index = beda + 127
        if index>=0 and index < 255: 
            hist_rtb [index] += 1
            count_rtb +=1

    if count_rtb > 0:  
        for i in range (255):
            hist_rtb[i] = hist_rtb[i] / count_rtb
    
    # FTB

    first_tone = pitches[0]

    selisih_ftb = []
    for pitch in pitches:
        selisih_ftb.append(pitch - first_tone)


    hist_ftb = [0 for _ in range(255)]
    count_ftb = 0
    
    for beda in selisih_ftb:
        index = beda + 127  
        if index >=0 and index < 255:
            hist_ftb[index] += 1
            count_ftb += 1

    if count_ftb > 0:  
        for i in range(255):  
            hist_ftb[i] = hist_ftb[i] / count_ftb
    
    return np.concatenate([hist_atb, hist_rtb, hist_ftb])

# def compute_similarity(query_features, database_features):
#     """
#     Menghitung similaritas antara vektor fitur query dan database menggunakan cosine similarity.
#     """
#     similarities = cosine_similarity(query_features.reshape(1, -1), database_features)
#     return similarities.flatten()

# # Contoh Pipeline
# def query_by_humming(midi_query, midi_database):
#     """
#     Pipeline utama untuk query by humming.
#     """
#     # Proses query
#     query_windows = process_midi(midi_query)
#     query_features = [extract_features(window) for window in query_windows]
    
#     # Proses database
#     database_features = []
#     for midi_data in midi_database:
#         db_windows = process_midi(midi_data)
#         db_features = [extract_features(window) for window in db_windows]
#         database_features.extend(db_features)
    
#     database_features = np.array(database_features)
    
#     # Hitung Similaritas
#     results = []
#     for query_vector in query_features:
#         similarity_scores = compute_similarity(query_vector, database_features)
#         results.append(similarity_scores)
    
#     return results

midi_path = r"C:/coding/Tingkat 2/Tubes Algeo 2/x(45).mid"

# Eksekusi
try:
    arr = process_midi(midi_path)
    print(arr)
except FileNotFoundError:
    print(f"File MIDI tidak ditemukan: {midi_path}")
except Exception as e:
    print(f"Terjadi kesalahan: {e}")


