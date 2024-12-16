from flask import Flask, request, send_from_directory, jsonify
import os
import zipfile
from flask_cors import CORS
import shutil 

app = Flask(__name__)
CORS(app)  # Mengizinkan request dari React

# Konfigurasi folder
BASE_FOLDER = os.path.abspath('src/react-app/src/media')  # Path absolut ke folder media
UPLOAD_FOLDER = os.path.join(BASE_FOLDER, 'uploads')
MAPPER_FOLDER = os.path.join(BASE_FOLDER, 'mapper')
MUSIC_FOLDER = os.path.join(BASE_FOLDER, 'music')
PICTURE_FOLDER = os.path.join(BASE_FOLDER, 'picture')

# Pastikan folder ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MAPPER_FOLDER, exist_ok=True)
os.makedirs(MUSIC_FOLDER, exist_ok=True)
os.makedirs(PICTURE_FOLDER, exist_ok=True)

# Endpoint untuk mendapatkan semua media
@app.route('/media', methods=['GET'])
def get_media():
    media_files = []

    # Debug 2: Isi folder music
    print("\n=== DEBUG: Contents of MUSIC_FOLDER ===")
    if not os.path.exists(MUSIC_FOLDER):
        print("ERROR: MUSIC_FOLDER not found!")
    else:
        music_files = os.listdir(MUSIC_FOLDER)
        print("Music Files Found:", music_files)

        for filename in music_files:
            print("Processing Music File:", filename)  # Log setiap file
            media_files.append({
                "id": len(media_files) + 1,
                "name": filename,
                "type": "folder_music",  # Flagging khusus
                "url": f"/media/music/{filename}"
            })

    # Debug 3: Isi folder picture
    print("\n=== DEBUG: Contents of PICTURE_FOLDER ===")
    if not os.path.exists(PICTURE_FOLDER):
        print("ERROR: PICTURE_FOLDER not found!")
    else:
        picture_files = os.listdir(PICTURE_FOLDER)
        print("Picture Files Found:", picture_files)

        for filename in picture_files:
            print("Processing Picture File:", filename)
            media_files.append({
                "id": len(media_files) + 1,
                "name": filename,
                "type": "folder_image",  # Flagging khusus
                "url": f"/media/picture/{filename}"
            })

    # Debug 4: Isi folder mapper
    print("\n=== DEBUG: Contents of MAPPER_FOLDER ===")
    if not os.path.exists(MAPPER_FOLDER):
        print("ERROR: MAPPER_FOLDER not found!")
    else:
        mapper_files = os.listdir(MAPPER_FOLDER)
        print("Mapper Files Found:", mapper_files)

        for filename in mapper_files:
            print("Processing Mapper File:", filename)
            media_files.append({
                "id": len(media_files) + 1,
                "name": filename,
                "type": "folder_mapper",  # Flagging khusus
                "url": f"/media/mapper/{filename}"
            })

    # Debug 5: Hasil akhir media_files
    print("\n=== DEBUG: Media Files Sent to Frontend ===")
    for file in media_files:
        print(file)
    print("===========================\n")

    return jsonify(media_files)

# Endpoint untuk melayani file media
@app.route('/media/<folder>/<filename>', methods=['GET'])
def serve_media(folder, filename):
    folder_path = os.path.join(BASE_FOLDER, folder)
    file_path = os.path.join(folder_path, filename)

    # Debug 6: Log file yang dilayani
    print(f"Serving file: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")

    if os.path.exists(file_path):
        return send_from_directory(folder_path, filename)
    else:
        return jsonify({"message": "File not found", "path": file_path}), 404

# Endpoint untuk upload file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    print(f"File uploaded: {file_path}")  # Debug
    return jsonify({'message': 'File uploaded successfully'}), 200

# Endpoint untuk upload file ZIP
@app.route('/upload_zip', methods=['POST'])
def upload_zip():
    if 'file' not in request.files or 'category' not in request.form:
        return jsonify({'message': 'No file part or category'}), 400

    file = request.files['file']
    category = request.form['category']
    if category not in ['music', 'picture', 'mapper']:
        return jsonify({'message': 'Invalid category'}), 400

    category_folder = os.path.join(BASE_FOLDER, category)
    os.makedirs(category_folder, exist_ok=True)

    zip_path = os.path.join(category_folder, file.filename)
    file.save(zip_path)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(category_folder)

    os.remove(zip_path)
    print(f"ZIP file extracted to: {category_folder}")  # Debug
    return jsonify({'message': 'ZIP file uploaded and extracted successfully'}), 200

@app.route('/reset_media', methods=['POST'])
def reset_media():
    try:
        # Hapus isi folder
        for folder in [MUSIC_FOLDER, PICTURE_FOLDER, MAPPER_FOLDER, UPLOAD_FOLDER]:
            if os.path.exists(folder):
                print(f"Clearing folder: {folder}")  # Debug log
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Hapus file atau link
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Hapus subdirektori

        return jsonify({"message": "All media folders have been reset."}), 200

    except Exception as e:
        print(f"Error resetting media folders: {e}")
        return jsonify({"message": "Failed to reset media folders.", "error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Flask server is running!"})

if __name__ == '__main__':
    app.run(debug=True)
