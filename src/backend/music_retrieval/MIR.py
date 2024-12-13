
import mido
import numpy as np
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
            if msg.type == 'note_on' and msg.channel == 1 :  # Sementara kita ambil dari smua channel
                melody_notes.append((msg.note, msg.time))

    if not melody_notes :
        raise ValueError ("Tidak ada melody di dalamnya")
    
    # melody_note [(note, time)]
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
        durasi = [note[1] for note in norm_window if note[1] > 0]

        if durasi :
            max_durasi = max(durasi)
        else:
            max_durasi = 1
        
        numeric = [
            (round(norm_pitch), round((duration / max_durasi) * 100))
            for norm_pitch, duration in norm_window
        ]
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
    if pitches:
        first_tone = pitches[0]
    else:
        first_tone = 0

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



def proses_database (midi_database_folder):

    if not os.path.isdir(midi_database_folder):
        raise ValueError("Invalid database folder path.")
    
    vektor_database_gab =[]

    for filename in os.listdir(midi_database_folder):
        file_path = os.path.join (midi_database_folder,filename)

        if os.path.isfile(file_path) and filename.endswith('.mid'):
            print (f"judul file yang diproses adalah: {file_path} ")

            db_vektor = []
            database_window = process_midi (file_path)
            #--
            if database_window is None or len(database_window) == 0:  # Cek jika hasil kosong
                print(f"Channel 1 tidak ditemukan atau file database kosong: {file_path}, dilewati.")
                continue
            #--

            for window in database_window:
                vektor = extract_features(window)
                db_vektor.append(vektor)
            if len(db_vektor) > 0:
                vektor_database_gab.append ((filename,db_vektor))
            else:
                print(f"Tidak ada vektor fitur yang dihasilkan untuk file database: {file_path}, dilewati.")

    return vektor_database_gab

def query_by_humming(query_window, vektor_database):

    vektor_query = []

    if query_window is None or len(query_window) == 0:  # Cek jika hasil kosong
        print(f"Channel 1 tidak ditemukan atau file query kosong: ")
        return None
    
    for window in query_window:
        vektor = extract_features(window)
        vektor_query.append(vektor)

    if len(vektor_query) == 0:
        print(f"Tidak ada vektor fitur yang dihasilkan untuk query: ")
        return None
    
    # print(f'vektor query = {vektor_query}')
    # vektor_database = proses_database(midi_database_folder)
    # print (f'vektor database = {vektor_database}')


    results = []

    for query_vec in vektor_query:
        file_scores = []
        for filename, db_vectors in vektor_database:
            scores = [cosine_similarity(query_vec, db_vec) for db_vec in db_vectors]
            if scores:
                file_scores.append((filename, max(scores)))
        if file_scores:
            results.append(file_scores)


    if not results:
        print("Tidak ada similarity yang dihitung karena semua data kosong.")
        return None
    # for query in vektor_query:
    #     score_similarity = cosine_similarity ( query.reshape(1, -1), vektor_database )
    #     results.append(score_similarity)

    return results

 
def olah_score_song (results):
    if not results:
        print("Hasil kosong, tidak ada lagu yang ditemukan.")
        return

    # Gabungkan skor untuk setiap file
    similarity_scores = {}
    for window_scores in results:
        for filename, score in window_scores:
            if filename not in similarity_scores:
                similarity_scores[filename] = []
            similarity_scores[filename].append(score)

    # Hitung rata-rata skor untuk setiap file
    average_scores = {filename: sum(scores) / len(scores) for filename, scores in similarity_scores.items()}
    sorted_songs = sorted(average_scores.items(), key=lambda x: x[1], reverse=True)

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
    # Ambil top N hasil
    top_songs = sorted_songs[:top_n]

    # Cetak hasil
    print(f"Top {top_n} lagu yang paling mirip:")
    for i, (song, score) in enumerate(top_songs, start=1):
        print(f"{i}. {song} - Skor similarity rata-rata: {score:.2f}")




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


# midi_query_path = r"C:/coding/Tingkat 2/Tubes Algeo 2/Algeo02-23020/src/backend/music_retrieval/database/Remember_the_Time.mid"
# midi_database_folder = r"C:/coding/Tingkat 2/Tubes Algeo 2/Algeo02-23020/src/backend/music_retrieval/database"
# # Eksekusi
# try:

# result = process_midi(midi_query_path)
# print (result)
#     print

#     vektor_query = []


#     for window in result:
#         vektor = extract_features(window)
#         vektor_query.append(vektor)
#     print(f'vektor query = {vektor_query}')


# except FileNotFoundError:
#     print(f"File MIDI tidak ditemukan: {midi_query_path}")
# except Exception as e:
#     print(f"Terjadi kesalahan: {e}")
