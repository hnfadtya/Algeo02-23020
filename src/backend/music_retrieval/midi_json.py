import json
from MIR import * 

def save_json(vektor_database, output_path):
    """
    Menyimpan vektor database ke file JSON.
    
    Args:
        vektor_database (list): Hasil dari proses_database, berupa list tuple (filename, db_vectors).
        output_path (str): Path untuk menyimpan file JSON.
    """
    # Konversi ke format yang bisa disimpan ke JSON
    json_data = [
        {
            "filename": filename,
            "vectors": [vector.tolist() if isinstance(vector, np.ndarray) else vector for vector in db_vectors]
        }
        for filename, db_vectors in vektor_database
    ]
    
    try:
        with open(output_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
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
        vektor_database = [
            (
                entry["filename"],
                [np.array(vector) for vector in entry["vectors"]]
            )
            for entry in json_data
        ]
        print(f"Vektor database berhasil dibaca dari {input_path}")
        return vektor_database
    except Exception as e:
        print(f"Error saat membaca file JSON: {e}")
        return None


# midi_database_folder = "C:/coding/Tingkat 2/Tubes Algeo 2/Algeo02-23020/src/backend/music_retrieval/database"
# output_json = "vektor_database.json"

# vektor_database = proses_database(midi_database_folder)
# save_json(vektor_database, output_json)
