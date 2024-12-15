import json
from MIR import * 

# def save_json(vektor_database, output_path):
#     """
#     Menyimpan vektor database ke file JSON.
    
#     Args:
#         vektor_database (list): Hasil dari proses_database, berupa list tuple (filename, db_vectors).
#         output_path (str): Path untuk menyimpan file JSON.
#     """
#     # Konversi ke format yang bisa disimpan ke JSON
#     import json

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
    """
    Membaca file JSON dan mengembalikan vektor database.
    
    Args:
        input_path (str): Path file JSON yang akan dibaca.
    
    Returns:
        list: Vektor database berupa list tuple (filename, db_vectors).
    """
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

# midi_database_folder = "C:/coding/Tingkat 2/Tubes Algeo 2/Algeo02-23020/src/backend/music_retrieval/database"
# output_json = "vektor_database.json"

# vektor_database = proses_database(midi_database_folder)
# save_json(vektor_database, output_json)
