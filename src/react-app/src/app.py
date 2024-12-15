from flask import Flask, request, send_from_directory, jsonify
import os
import zipfile
from flask_cors import CORS

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

    # Menambahkan file audio dari folder music
    for filename in os.listdir(MUSIC_FOLDER):
        if filename.endswith(('.mp3', '.wav', '.mid')):
            media_files.append({
                "id": len(media_files) + 1,
                "name": filename,
                "type": "audio",
                "url": f"/media/music/{filename}"
            })

    # Menambahkan file gambar dari folder picture
    for filename in os.listdir(PICTURE_FOLDER):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            media_files.append({
                "id": len(media_files) + 1,
                "name": filename,
                "type": "image",
                "url": f"/media/picture/{filename}"
            })

    # Menambahkan file dari folder mapper
    for filename in os.listdir(MAPPER_FOLDER):
        if filename.endswith(('.txt', '.zip')):
            media_files.append({
                "id": len(media_files) + 1,
                "name": filename,
                "type": "mapper",
                "url": f"/media/mapper/{filename}"
            })

    return jsonify(media_files)

# Endpoint untuk melayani file media
@app.route('/media/<folder>/<filename>', methods=['GET'])
def serve_media(folder, filename):
    folder_path = os.path.join(BASE_FOLDER, folder)
    file_path = os.path.join(folder_path, filename)

    # Log path untuk debugging
    print(f"Serving file from: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")

    if os.path.exists(file_path):
        return send_from_directory(folder_path, filename)
    else:
        return jsonify({"message": "File not found", "path": file_path}), 404

if __name__ == '__main__':
    app.run(debug=True)
