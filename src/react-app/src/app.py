from flask import Flask, request, send_from_directory, jsonify
import os
import zipfile
from flask_cors import CORS
from backend.image_retrieval.retrieval import image_retrieval_function
from backend.music_retrieval.MIR import query_by_humming

app = Flask(__name__)
CORS(app)  # Mengizinkan request dari React

# Konfigurasi folder
BASE_FOLDER = os.path.abspath('media')  # Path absolut ke folder media
UPLOAD_FOLDER = os.path.join(BASE_FOLDER, 'uploads')
MAPPER_FOLDER = os.path.join(BASE_FOLDER, 'mapper')
MUSIC_FOLDER = os.path.join(BASE_FOLDER, 'music')
PICTURE_FOLDER = os.path.join(BASE_FOLDER, 'picture')

BASE_RETRIEVAL_FOLDER = os.path.abspath('retrieval')  # Path absolut ke folder media
RETRIEVAL_UPLOAD_FOLDER = os.path.join(BASE_FOLDER, 'uploads')
RETRIEVAL_MAPPER_FOLDER = os.path.join(BASE_FOLDER, 'mapper')
RETRIEVAL_MUSIC_FOLDER = os.path.join(BASE_FOLDER, 'music')
RETRIEVAL_PICTURE_FOLDER = os.path.join(BASE_FOLDER, 'picture')
# Pastikan folder ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MAPPER_FOLDER, exist_ok=True)
os.makedirs(MUSIC_FOLDER, exist_ok=True)
os.makedirs(PICTURE_FOLDER, exist_ok=True)

os.makedirs(RETRIEVAL_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RETRIEVAL_MAPPER_FOLDER, exist_ok=True)
os.makedirs(RETRIEVAL_MUSIC_FOLDER, exist_ok=True)
os.makedirs(RETRIEVAL_PICTURE_FOLDER, exist_ok=True)

# audio_file pic_name
# audio_1.mid pic_1.png
# audio_2.mid pic_2.png
# audio_3.mid pic_3.png
# audio_4.mid pic_4.png
# Endpoint untuk mendapatkan semua media
@app.route('/media', methods=['GET'])
def get_media():
    mapper = []
    # picture = []
    audio = []

    # Menambahkan file dari folder mapper
    for mapper in os.listdir(MAPPER_FOLDER):
        if mapper.endswith('.txt'):
            media_items = []
            try:
                file_path = os.path.join(MAPPER_FOLDER, mapper)
                with open(file_path, 'r') as file:
                    for line in file:
                        parts = line.strip().split()  # Pisahkan baris menjadi bagian
                        if len(parts) == 2:  # hanya dua elemen per baris
                            media_items.append({
                                "audio_file": parts[0],
                                "pic_name": parts[1]
                            })
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
            media_items

    # Menambahkan file gambar dari folder picture
    for filename in os.listdir(PICTURE_FOLDER):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            picture.append({
                "id": len(mapper) + 1,
                "name": filename,
                "type": "image",
                "url": f"/media/picture/{filename}"
            })
    # # Menambahkan file audio dari folder music
    # for filename in os.listdir(MUSIC_FOLDER):
    #     if filename.endswith(('.mp3', '.wav', '.mid')):
    #         audio.append({
    #             "id": len(mapper) + 1,
    #             "name": filename,
    #             "type": "audio",
    #             "url": f"/media/music/{filename}"
    #         })
    return jsonify(mapper)

@app.get("/delete-dataset/")
async def deleteDataSet():
    if os.path.isfile("./hasil.json"):
        os.remove("./hasil.json")
    if os.path.isdir("static/dataset"):
        shutil.rmtree("static/dataset")
    if os.path.isfile("cache.txt"):
        os.remove("cache.txt")
    return {"deleteStatus":"Complete"}

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

# Endpoint untuk mengunggah file umum
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'category' not in request.form:
        return jsonify({'message': 'No file part or category'}), 400

    file = request.files['file']
    category = request.form['category']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if category not in ['music', 'picture']:
        return jsonify({'message': 'Invalid category'}), 400

    if file and category == 'picture':
        query_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        result = image_retrieval_function(query_file_path)
        for i in range(len(result)):
            query_file_path = os.path.join(BASE_RETRIEVAL_FOLDER, result[i][0])
            file.save(query_file_path)
        return jsonify({'message': 'File uploaded successfully'}), 200
    # elif file and category == 'music':
        # query_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        # result = image_retrieval_function(query_file_path)
        # for i in range(len(result)):
        #     query_file_path = os.path.join(BASE_RETRIEVAL_FOLDER, result[i][0])
        #     file.save(query_file_path)
        # return jsonify({'message': 'File uploaded successfully'}), 200


# Endpoint untuk mengunggah file ZIP berdasarkan kategori
@app.route('/upload_zip', methods=['POST'])
def upload_zip():
    if 'file' not in request.files or 'category' not in request.form:
        return jsonify({'message': 'No file part or category'}), 400

    file = request.files['file']
    category = request.form['category']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if category not in ['music', 'picture', 'mapper']:
        return jsonify({'message': 'Invalid category'}), 400

    if file:
        # Tentukan folder untuk menyimpan file ZIP sesuai kategori
        category_folder = os.path.join(BASE_FOLDER, category)
        os.makedirs(category_folder, exist_ok=True)

        # Tentukan path untuk file ZIP
        zip_path = os.path.join(category_folder, file.filename)
        file.save(zip_path)

        # Ekstrak file ZIP
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(category_folder)

        # Hapus file ZIP setelah ekstraksi
        os.remove(zip_path)

        return jsonify({'message': 'ZIP file uploaded and extracted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
