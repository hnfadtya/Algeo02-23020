from flask import Flask, request, send_from_directory, jsonify
import os
import zipfile
from flask_cors import CORS
import sys
import shutil
import json
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
MAPPER_FOLDER = os.path.join(BASE_FOLDER, 'mapper')
MUSIC_FOLDER = os.path.join(BASE_FOLDER, 'music')
PICTURE_FOLDER = os.path.join(BASE_FOLDER, 'picture')
DATABASE_FOLDER = os.path.join(BASE_FOLDER, 'datamusic')
MAPPER_JSON_PATH = os.path.join(MAPPER_FOLDER, "mapper.json")

# Buat folder jika belum ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MAPPER_FOLDER, exist_ok=True)
os.makedirs(MUSIC_FOLDER, exist_ok=True)
os.makedirs(PICTURE_FOLDER, exist_ok=True)
os.makedirs(DATABASE_FOLDER, exist_ok=True)

MIDI_DATABASE_FILE = os.path.join(DATABASE_FOLDER, 'midi_database.json')


# Fungsi tambahan untuk memastikan file database JSON tersedia
def ensure_midi_database():
    if not os.path.exists(MIDI_DATABASE_FILE):
        with open(MIDI_DATABASE_FILE, 'w') as f:
            f.write("[]")  # File JSON kosong
        print(f"Database MIDI kosong telah dibuat di: {MIDI_DATABASE_FILE}")


# Endpoint: Mendapatkan semua media
@app.route('/media', methods=['GET'])
def get_media():
    media_files = []

    # for folder_name, folder_path, folder_type in [
    #     ("folder_music", MUSIC_FOLDER, "music"),
    #     ("folder_image", PICTURE_FOLDER, "picture"),
    #     ("folder_mapper", MAPPER_FOLDER, "mapper")
    # ]:
    #     if os.path.exists(folder_path):
    #         for filename in os.listdir(folder_path):
    #             media_files.append({
    #                 "id": len(media_files) + 1,
    #                 "name": filename,
    #                 "type": folder_name,
    #                 "url": f"/media/{folder_type}/{filename}"
    #             })

    with open(MAPPER_JSON_PATH, 'r') as file:
        new_mapper = json.load(file)

    # Tambahkan data dari new_mapper ke media_files
    for item in new_mapper:
        # Pastikan data memiliki kunci 'audio_file' dan 'pic_name'
        if 'audio_file' in item and 'pic_name' in item:
            media_files.append({
                "id": len(media_files) + 1,
                "audio_file": item['audio_file'],
                "pic_name": item['pic_name'],
                "url": f"/media/picture/{item['pic_name']}"  # Path ke mapper.json
            })
    for data in media_files:
        print(data)

    return jsonify(media_files)


# Endpoint: Melayani file media
@app.route('/media/<folder>/<filename>', methods=['GET'])
def serve_media(folder, filename):
    folder_path = os.path.join(BASE_FOLDER, folder)
    if os.path.exists(os.path.join(folder_path, filename)):
        return send_from_directory(folder_path, filename)
    return jsonify({"message": "File not found"}), 404

def update_mapper_json(mapper_path, sorted_data):
    try:
        # Baca file mapper.json
        with open(mapper_path, 'r') as file:
            mapper = json.load(file)

        # Perbarui urutan mapper.json berdasarkan sorted_data
        new_mapper = []
        media_files = []
        for sorted_item in sorted_data:
            for original_item in mapper:
                # Cocokkan sorted_data["filename"] dengan mapper["pic_name"]
                if original_item["pic_name"] == sorted_item["filename"]:
                    new_mapper.append(original_item)
                    media_files.append({
                        "id": len(media_files) + 1,
                        "audio_file": original_item['audio_file'],
                        "pic_name": original_item['pic_name'],
                        "similarity": sorted_item['similarity'],
                        "url": f"/media/picture/{original_item['pic_name']}"  # Path ke mapper.json
                    })
                    break
        # Tulis ulang mapper.json dengan urutan yang baru
        with open(mapper_path, 'w') as file:
            json.dump(media_files, file, indent=4)

        print("mapper.json updated successfully")
        return media_files
    except Exception as e:
        print(f"Failed to update mapper.json: {e}")
        raise


# Endpoint: Upload file biasa (gambar atau MIDI)
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        if file.filename.endswith(('.png', '.jpg', '.jpeg')):  # Image Retrieval
            similarities, total_images, duration = image_retrieval_function(file.filename)
            sorted_files = [
                {"filename": os.listdir(PICTURE_FOLDER)[idx], "similarity": round(100 - (distance / (3 ** 0.5) * 100), 2)}
                for idx, distance in similarities
            ]
            # for file in sorted_files:
            #     print(file)
            media_files = update_mapper_json(MAPPER_JSON_PATH, sorted_files)
            # with open(MAPPER_JSON_PATH, 'r') as file:
            #     newMapper = json.load(file)
            # for data in newMapper:
            #     print(data)
            return jsonify({
                "message": "Image uploaded and similarity calculated",
                "sorted_files": media_files
            }), 200


        elif file.filename.endswith(('.mid', '.midi')):  # Music Retrieval
            ensure_midi_database()

            if not is_valid_midi(file_path):
                return jsonify({"message": "Invalid MIDI file"}), 400

            update_midi_database(MIDI_DATABASE_FILE, file_path)
            query_window = process_midi(file_path)
            database = load_json(MIDI_DATABASE_FILE)

            if not database:
                return jsonify({"message": "No songs found in database"}), 400

            results = query_by_humming(query_window, database)
            sorted_songs = olah_score_song(results)

            return jsonify({
                "message": "MIDI file processed successfully",
                "sorted_songs": sorted_songs
            }), 200

        else:
            return jsonify({"message": "Unsupported file type"}), 400

    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify({"message": "Error processing file", "error": str(e)}), 500


# Endpoint: Upload file ZIP
@app.route('/upload_zip', methods=['POST'])
def upload_dataset():
    if 'file' not in request.files or 'category' not in request.form:
        return jsonify({'message': 'No file part or category'}), 400

    file = request.files['file']
    category = request.form['category']

    # Untuk mapper.json
    if file.filename == "mapper.json" and category == "mapper":
        file_path = os.path.join(MAPPER_FOLDER, "mapper.json")
        file.save(file_path)
        print(f"Mapper.json uploaded to: {file_path}")
        return jsonify({'message': 'mapper.json uploaded successfully'}), 200

    # Untuk ZIP files
    elif category in ['music', 'picture', 'mapper'] and file.filename.endswith('.zip'):
        category_folder = os.path.join(BASE_FOLDER, category)
        os.makedirs(category_folder, exist_ok=True)

        # Simpan dan ekstrak file ZIP
        zip_path = os.path.join(category_folder, file.filename)
        file.save(zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(category_folder)

        os.remove(zip_path)
        print(f"ZIP file extracted to: {category_folder}")
        return jsonify({'message': 'ZIP file uploaded and extracted successfully'}), 200

    else:
        return jsonify({'message': 'Invalid file type or category'}), 400

# Endpoint: Reset media folder
@app.route('/reset_media', methods=['POST'])
def reset_media():
    try:
        for folder in [UPLOAD_FOLDER, MUSIC_FOLDER, PICTURE_FOLDER, MAPPER_FOLDER]:
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


# Endpoint: Homepage
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Flask server is running!"})


if __name__ == '__main__':
    app.run(debug=True)