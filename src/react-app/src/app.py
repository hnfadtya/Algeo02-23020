from flask import Flask, request, send_from_directory, jsonify
import os
import json
import time
import zipfile
from flask_cors import CORS
import sys
import shutil
from backend.image_retrieval.retrieval import image_retrieval_function
from backend.music_retrieval.MIR import (
    is_valid_midi,
    proses_database,
    query_by_humming,
    update_midi_database,
    process_midi,
    olah_score_song,
    save_json_in_batches,
    load_json
)

# Inisialisasi Flask
app = Flask(__name__)
CORS(app)

# Debug: Print working directory
print("Current Working Directory:", os.getcwd())
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

# Konfigurasi folder media
BASE_FOLDER = os.path.abspath('src/react-app/src/media')
UPLOAD_FOLDER = os.path.join(BASE_FOLDER, 'uploads')
PICTURE_FOLDER = os.path.join(BASE_FOLDER, 'picture')
MUSIC_FOLDER = os.path.join(BASE_FOLDER, 'music')
DATABASE_FOLDER = os.path.join(BASE_FOLDER, 'datamusic')
MIDI_DATABASE_FILE = os.path.join(DATABASE_FOLDER, 'midi_database.json')
MAPPER_FOLDER = os.path.join(BASE_FOLDER, 'mapper')
MAPPER_JSON_PATH = os.path.join(MAPPER_FOLDER, "mapper.json")

# Buat folder jika belum ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MAPPER_FOLDER, exist_ok=True)
os.makedirs(MUSIC_FOLDER, exist_ok=True)
os.makedirs(PICTURE_FOLDER, exist_ok=True)
os.makedirs(DATABASE_FOLDER, exist_ok=True)



# Fungsi tambahan untuk memastikan file database JSON tersedia
def ensure_midi_database():
    if not os.path.exists(MIDI_DATABASE_FILE):
        with open(MIDI_DATABASE_FILE, 'w') as f:
            f.write("[]")  # File JSON kosong
        print(f"Database MIDI kosong telah dibuat di: {MIDI_DATABASE_FILE}")


# Endpoint: Mendapatkan semua media
@app.route('/media', methods=['GET'])
def get_media():
    with open(MAPPER_JSON_PATH, 'r') as mapper_file:
        mapper = json.load(mapper_file)
    media_files = []

    for file in mapper:
        media_files.append({
            "id": len(media_files) + 1,
            "name": file["audio_file"],
            "type": "folder_image",
            "url": f"/media/picture/{file["pic_name"]}"
        })

    return jsonify(media_files)


# Endpoint: Melayani file media
@app.route('/media/<folder>/<filename>', methods=['GET'])
def serve_media(folder, filename):
    folder_path = os.path.join(BASE_FOLDER, folder)
    if os.path.exists(os.path.join(folder_path, filename)):
        return send_from_directory(folder_path, filename)
    return jsonify({"message": "File not found"}), 404


# Endpoint: Upload file biasa (gambar atau MIDI)
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    # Simpan file sementara di folder uploads
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    with open(MAPPER_JSON_PATH, 'r') as mapper_file:
        mapper = json.load(mapper_file)
    # MAPPER_JSON_PATH = os.path.join(MAPPER_JSON_PATH, mapper)
    media_files = []

    try:
        # 1. Image Retrieval
        if file.filename.endswith(('.png', '.jpg', '.jpeg')):  
            print(f"Processing image file: {file.filename}")
            similarities, total_images, duration = image_retrieval_function(file.filename)
            sorted_files = [
                {"filename": os.listdir(PICTURE_FOLDER)[idx], 
                 "similarity": round(100 - (distance / (3 ** 0.5) * 100), 2)}
                for idx, distance in similarities
            ]
            # print(sorted_files)
            # Update the mapper based on sorted_data (dictionary format)
            for sorted_item in sorted_files:
                for original_item in mapper:
                    if original_item["pic_name"] == sorted_item["filename"]:
                        # new_mapper.append(original_item)
                        media_files.append({
                            "audio_file": original_item['audio_file'],
                            "pic_name": original_item['pic_name'],
                        })
                        break
            for file in media_files:
                print(file)
            # Write the updated mapper.json file
            with open(MAPPER_JSON_PATH, 'w') as file:
                json.dump(media_files, file, indent=4)
            return jsonify({
                "message": "Image uploaded and similarity calculated",
                "sorted_files": sorted_files,
                "duration": duration
            }), 200

        # 2. Music Retrieval
        elif file.filename.endswith(('.mid', '.midi')):  
            print(f"Processing MIDI file: {file.filename}")
            ensure_midi_database()  # Pastikan database JSON tersedia

            # Validasi file MIDI
            if not is_valid_midi(file_path):
                return jsonify({"message": "Invalid MIDI file"}), 400

            # Ekstrak melodi dari file MIDI query
            start = time.time()
            query_window = process_midi(file_path)
            if not query_window:
                return jsonify({"message": "No melody detected in the MIDI file"}), 400

            # Load database MIDI
            database = load_json(MIDI_DATABASE_FILE)
            if not database:
                return jsonify({"message": "No songs found in the database"}), 400

            # Pencarian berbasis melodi
            print("Running query_by_humming...")
            results = query_by_humming(query_window, database)
            if not results:
                return jsonify({"message": "No matching results found"}), 400

            # Proses hasil pencarian
            sorted_songs = olah_score_song(results)
            # Update the mapper based on sorted_data (tuple format)
            end = time.time()
            duration = end - start
            for sorted_item in sorted_songs:
                audio_file, similarity = sorted_item
                for original_item in mapper:
                    if original_item["audio_file"] == audio_file:
                        # new_mapper.append(original_item)
                        media_files.append({
                            "audio_file": original_item['audio_file'],
                            "pic_name": original_item['pic_name'],
                        })
                        break

            # Write the updated mapper.json file
            with open(MAPPER_JSON_PATH, 'w') as file:
                json.dump(media_files, file, indent=4)
            return jsonify({
                "message": "MIDI file processed successfully",
                "sorted_songs": sorted_songs
            }), 200

        # 3. Format file tidak didukung
        else:
            return jsonify({"message": "Unsupported file type"}), 400

    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify({"message": "Error processing file", "error": str(e)}), 500


# Endpoint: Upload file ZIP
@app.route('/upload_zip', methods=['POST'])
def upload_zip():
    if 'file' not in request.files or 'category' not in request.form:
        return jsonify({'message': 'Missing file or category'}), 400

    file = request.files['file']
    category = request.form['category']
    if category not in ['music', 'picture', 'mapper']:
        return jsonify({'message': 'Invalid category'}), 400

    category_folder = os.path.join(BASE_FOLDER, category)
    for filename in os.listdir(category_folder):
        file_path = os.path.join(category_folder, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    zip_path = os.path.join(category_folder, file.filename)        

    try:
        file.save(zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.mid')):
                    # Hilangkan folder "AlbumDataset/" dari nama file
                    clean_name = os.path.basename(file_name)
                    destination_path = os.path.join(category_folder, clean_name)
                    
                    with zip_ref.open(file_name) as source, open(destination_path, 'wb') as target:
                        target.write(source.read())        
        os.remove(zip_path)

        if category == 'music':  # Update MIDI database
            print("Updating MIDI database...")
            database = proses_database(MUSIC_FOLDER)
            save_json_in_batches(database, MIDI_DATABASE_FILE)
            print("MIDI database updated successfully.")
        return jsonify({'message': 'ZIP file uploaded and processed successfully'}), 200

    except Exception as e:
        print(f"Error processing ZIP file: {e}")
        return jsonify({'message': 'Error processing ZIP file', 'error': str(e)}), 500


# Endpoint: Reset media folder
@app.route('/reset_media', methods=['POST'])
def reset_media():
    try:
        for folder in [UPLOAD_FOLDER, MUSIC_FOLDER, PICTURE_FOLDER, MAPPER_FOLDER, DATABASE_FOLDER]:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        return jsonify({"message": "All media folders have been reset."}), 200
    except Exception as e:
        print(f"Error resetting media: {e}")
        return jsonify({"message": "Failed to reset media", "error": str(e)}), 500


# Endpoint: Update MIDI database manually
@app.route('/update_midi_database', methods=['POST'])
def update_midi_database_endpoint():
    try:
        print("Updating MIDI database...")
        database = proses_database(MUSIC_FOLDER)
        save_json_in_batches(database, MIDI_DATABASE_FILE)
        return jsonify({"message": "MIDI database updated successfully."}), 200
    except Exception as e:
        print(f"Error updating MIDI database: {e}")
        return jsonify({"message": "Error updating MIDI database.", "error": str(e)}), 500

@app.route('/update_midi_database', methods=['POST'])
def update_database():
    try:
        print("Updating MIDI database from folder 'music'...")
        update_midi_database(MIDI_DATABASE_FILE, MUSIC_FOLDER)
        return jsonify({"message": "MIDI database updated successfully."}), 200
    except Exception as e:
        print(f"Error updating MIDI database: {e}")
        return jsonify({"message": "Failed to update database", "error": str(e)}), 500

# Endpoint: Homepage
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Flask server is running!"})


if __name__ == '__main__':
    app.run(debug=True)
