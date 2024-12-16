from flask import Flask, request, send_from_directory, jsonify
import os
import zipfile
from flask_cors import CORS
import sys
import shutil
from backend.image_retrieval.retrieval import image_retrieval_function

# Inisialisasi Flask
app = Flask(__name__)
CORS(app)  # Mengizinkan request dari React

# Debug: Print working directory dan sys.path
print("Current Working Directory:", os.getcwd())
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

# Konfigurasi folder media
BASE_FOLDER = os.path.abspath('src/react-app/src/media')
UPLOAD_FOLDER = os.path.join(BASE_FOLDER, 'uploads')
MAPPER_FOLDER = os.path.join(BASE_FOLDER, 'mapper')
MUSIC_FOLDER = os.path.join(BASE_FOLDER, 'music')
PICTURE_FOLDER = os.path.join(BASE_FOLDER, 'picture')

# Buat folder jika belum ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MAPPER_FOLDER, exist_ok=True)
os.makedirs(MUSIC_FOLDER, exist_ok=True)
os.makedirs(PICTURE_FOLDER, exist_ok=True)

# Endpoint: Mendapatkan semua media
@app.route('/media', methods=['GET'])
def get_media():
    media_files = []

    # Debug: Periksa folder music
    print("\n=== DEBUG: Contents of MUSIC_FOLDER ===")
    if os.path.exists(MUSIC_FOLDER):
        music_files = os.listdir(MUSIC_FOLDER)
        for filename in music_files:
            media_files.append({
                "id": len(media_files) + 1,
                "name": filename,
                "type": "folder_music",
                "url": f"/media/music/{filename}"
            })

    # Debug: Periksa folder picture
    print("\n=== DEBUG: Contents of PICTURE_FOLDER ===")
    if os.path.exists(PICTURE_FOLDER):
        picture_files = os.listdir(PICTURE_FOLDER)
        for filename in picture_files:
            media_files.append({
                "id": len(media_files) + 1,
                "name": filename,
                "type": "folder_image",
                "url": f"/media/picture/{filename}"
            })

    # Debug: Periksa folder mapper
    print("\n=== DEBUG: Contents of MAPPER_FOLDER ===")
    if os.path.exists(MAPPER_FOLDER):
        mapper_files = os.listdir(MAPPER_FOLDER)
        for filename in mapper_files:
            media_files.append({
                "id": len(media_files) + 1,
                "name": filename,
                "type": "folder_mapper",
                "url": f"/media/mapper/{filename}"
            })

    print("\n=== DEBUG: Media Files Sent to Frontend ===")
    for file in media_files:
        print(file)

    return jsonify(media_files)

# Endpoint: Melayani file media
@app.route('/media/<folder>/<filename>', methods=['GET'])
def serve_media(folder, filename):
    folder_path = os.path.join(BASE_FOLDER, folder)
    file_path = os.path.join(folder_path, filename)

    if os.path.exists(file_path):
        return send_from_directory(folder_path, filename)
    else:
        return jsonify({"message": "File not found", "path": file_path}), 404

# Endpoint: Upload file biasa
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # Simpan file ke folder uploads
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    print(f"File uploaded: {file_path}")

    # Proses similarity
    try:
        similarities, total_images, duration = image_retrieval_function(file.filename)
        most_similar_distance = similarities[0][1]
        similarity_percentage = 100 - (most_similar_distance / (3 ** 0.5) * 100)

        # Ambil gambar yang sudah diurutkan
        sorted_files = []
        for sim in similarities:
            idx, distance = sim
            similarity_score = 100 - (distance / (3 ** 0.5) * 100)
            sorted_files.append({
                "filename": os.listdir(PICTURE_FOLDER)[idx],
                "similarity": round(similarity_score, 2)
            })

        return jsonify({
            "message": "File uploaded and similarity calculated",
            "similarity_percentage": round(similarity_percentage, 2),
            "duration": round(duration, 2),
            "total_images": total_images,
            "sorted_files": sorted_files
        }), 200
    except Exception as e:
        print(f"Error processing similarity: {e}")
        return jsonify({"message": "Error processing retrieval", "error": str(e)}), 500


# Endpoint: Upload file ZIP
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
    print(f"ZIP file extracted to: {category_folder}")
    return jsonify({'message': 'ZIP file uploaded and extracted successfully'}), 200

# Endpoint: Reset media folder
@app.route('/reset_media', methods=['POST'])
def reset_media():
    try:
        for folder in [MUSIC_FOLDER, PICTURE_FOLDER, MAPPER_FOLDER, UPLOAD_FOLDER]:
            if os.path.exists(folder):
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
        return jsonify({"message": "All media folders have been reset."}), 200
    except Exception as e:
        print(f"Error resetting media folders: {e}")
        return jsonify({"message": "Failed to reset media folders.", "error": str(e)}), 500

# Endpoint: Homepage
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Flask server is running!"})

if __name__ == '__main__':
    app.run(debug=True)