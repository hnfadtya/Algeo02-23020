
import mido
import numpy as np
import math
import os

def process_midi (audio_path):
    # Load MIDI
    mid = mido.MidiFile(audio_path)
    melody_notes = []
    window_size = 40
    slide_size = 8
    
    for track in mid.tracks:
        for msg in track:
            # print (msg)
            if msg.type == 'note_on' and msg.channel == 2:  # Ngambil channel 1 doang
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
            norm_pitch = round(norm_pitch *100)
            
            # Tambahkan hasil ke daftar
            norm_window.append((norm_pitch, duration))

        
        # Konversi ke representasi numerik
        durasi = [note[1] for note in norm_window]

        if durasi :
            max_durasi = max(durasi)
        else:
            max_durasi = 1
        
        numeric = []  

        # Iterasi setiap not dalam normalized_window
        for note, duration in zip(norm_window, durasi):
            norm_pitch = note[0]  
            norm_duration = round((duration / max_durasi) * 100) 
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
    else:
        hist_atb
    
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

def cosine_similarity (v1,v2):

    if len(v1) != len(v2):
        print ("beda panjang")

    dot = 0
    for i in range (len (v1)):
        dot += v1[i] * v2[i]

    pjg_v1 = 0
    pjg_v2 = 0

    for v in v1:
        pjg_v1 += v**2
    pjg_v1 = math.sqrt(pjg_v1)

    for v in v2:
        pjg_v2 += v**2
    pjg_v2 = math.sqrt(pjg_v2)

    if (pjg_v1 ==0 or pjg_v2 == 0 ):
        print ("error panjang vektor")
        return 0

    hasil = dot / (pjg_v1 * pjg_v2)
    return (hasil)



def proses_database (midi_database_folder):

    vektor_database_gab =[]

    for filename in os.listdir(midi_database_folder):
        file_path = os.path.join (midi_database_folder,filename)

        if os.path.isfile(file_path) and filename.endswith('.mid'):
            print ("judul file yang diproses adalah: ")
            print (file_path)
            db_vektor = []
            database_window = process_midi (file_path)
            for window in database_window:
                vektor = extract_features(window)
                db_vektor.append(vektor)

            vektor_database_gab.append (db_vektor)
        

    return vektor_database_gab

def query_by_humming(midi_query_path, midi_database_folder):

    vektor_query = []
    query_window = process_midi (midi_query_path)

    for window in query_window:
        vektor = extract_features(window)
        vektor_query.append(vektor)
    print(f'vektor query = {vektor_query}')
    vektor_database = proses_database(midi_database_folder)
    print (f'vektor database = {vektor_database}')
    results = []
    for query in vektor_query:
        scores = []
        for db_vec in vektor_database:
            score = cosine_similarity(query, db_vec)
            scores.append(score)
        results.append(scores)

    # for query in vektor_query:
    #     score_similarity = cosine_similarity ( query.reshape(1, -1), vektor_database )
    #     results.append(score_similarity)

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


