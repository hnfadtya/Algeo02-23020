from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

# Mengaktifkan CORS untuk frontend yang berjalan di localhost:5173
CORS(app, resources={r"/media/*": {"origins": "http://localhost:5173"}})

# Folder untuk file media (pastikan sesuai dengan folder yang ada)
BASE_FOLDER = 'src/media'
MUSIC_FOLDER = os.path.join(BASE_FOLDER, 'music')
PICTURE_FOLDER = os.path.join(BASE_FOLDER, 'picture')
MAPPER_FOLDER = os.path.join(BASE_FOLDER, 'mapper')

# Pastikan folder ada
os.makedirs(MUSIC_FOLDER, exist_ok=True)
os.makedirs(PICTURE_FOLDER, exist_ok=True)
os.makedirs(MAPPER_FOLDER, exist_ok=True)

# Endpoint untuk mengakses data media (audio, gambar, dan file lainnya)
@app.route('/media', methods=['GET'])
def get_media():
    media_files = []

    for filename in os.listdir(MUSIC_FOLDER):
        if filename.endswith(('.mp3', '.wav', '.mid')):
            media_files.append({
                'id': len(media_files) + 1,
                'name': filename,
                'type': 'audio',
                'url': f'/media/music/{filename}'
            })

    for filename in os.listdir(PICTURE_FOLDER):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            media_files.append({
                'id': len(media_files) + 1,
                'name': filename,
                'type': 'image',
                'url': f'/media/picture/{filename}'
            })

    for filename in os.listdir(MAPPER_FOLDER):
        if filename.endswith(('.txt', '.zip')):
            media_files.append({
                'id': len(media_files) + 1,
                'name': filename,
                'type': 'mapper',
                'url': f'/media/mapper/{filename}'
            })

    return jsonify(media_files)

# Endpoint untuk meng-upload file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Tentukan folder tujuan berdasarkan tipe file
    folder = request.form.get('folder', '')
    if folder == 'music':
        save_path = MUSIC_FOLDER
    elif folder == 'picture':
        save_path = PICTURE_FOLDER
    elif folder == 'mapper':
        save_path = MAPPER_FOLDER
    else:
        return jsonify({'error': 'Invalid folder'}), 400

    # Simpan file
    file.save(os.path.join(save_path, file.filename))
    return jsonify({'message': f'File {file.filename} uploaded successfully'}), 200

# Endpoint untuk melayani file statis
@app.route('/media/<folder>/<filename>', methods=['GET'])
def serve_media(folder, filename):
    folder_path = os.path.join(BASE_FOLDER, folder)
    try:
        return send_from_directory(folder_path, filename)
    except FileNotFoundError:
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
