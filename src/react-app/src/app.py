from flask import Flask, request, send_from_directory, jsonify
import os
import zipfile

app = Flask(__name__)

# Konfigurasi folder
BASE_FOLDER = 'src/database'
UPLOAD_FOLDER = os.path.join(BASE_FOLDER, 'uploads')
MAPPER_FOLDER = os.path.join(BASE_FOLDER, 'mapper')
MUSIC_FOLDER = os.path.join(BASE_FOLDER, 'music')
PICTURE_FOLDER = os.path.join(BASE_FOLDER, 'picture')

# Pastikan folder ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MAPPER_FOLDER, exist_ok=True)
os.makedirs(MUSIC_FOLDER, exist_ok=True)
os.makedirs(PICTURE_FOLDER, exist_ok=True)

# Endpoint untuk mengunggah file umum (Tombol Upload)
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        return jsonify({"message": "No file provided"}), 400
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({"message": "File uploaded successfully to uploads folder!"}), 200

# Endpoint untuk mengunggah file ZIP ke kategori (Tombol Music, Picture, Mapper)
@app.route('/upload_zip', methods=['POST'])
def upload_zip():
    file = request.files.get('file')
    category = request.form.get('category')

    if not file:
        return jsonify({"message": "No file provided"}), 400
    if not category:
        return jsonify({"message": "No category provided"}), 400

    # Tentukan folder berdasarkan kategori
    if category == 'mapper':
        folder = MAPPER_FOLDER
    elif category == 'music':
        folder = MUSIC_FOLDER
    elif category == 'picture':
        folder = PICTURE_FOLDER
    else:
        return jsonify({"message": "Invalid category"}), 400

    file_path = os.path.join(folder, file.filename)
    file.save(file_path)

    # Jika file adalah ZIP, ekstrak isinya
    if file.filename.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(folder)
        os.remove(file_path)

    return jsonify({"message": f"ZIP file uploaded successfully to {category} folder!"}), 200

# Menyajikan React dari root folder
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path != "" and os.path.exists(f"react-app/{path}"):
        return send_from_directory('react-app', path)
    return send_from_directory('react-app', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
