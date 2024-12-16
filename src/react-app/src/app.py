from flask import Flask, request, send_from_directory, jsonify
import os
import zipfile
from flask_cors import CORS
<<<<<<< Updated upstream
from backend.image_retrieval.retrieval import image_retrieval_function
from backend.music_retrieval.MIR import query_by_humming
=======
import shutil 
from backend.retrieval import image_retrieval_function
# from backend.MIR import query_by_humming
>>>>>>> Stashed changes

app = Flask(__name__)
CORS(app)  # Mengizinkan request dari React

# Konfigurasi folder
<<<<<<< Updated upstream
BASE_FOLDER = os.path.abspath('media')  # Path absolut ke folder media
=======
BASE_FOLDER = os.path.abspath('src/react-app/src/media')  # Path absolut ke folder media
>>>>>>> Stashed changes
UPLOAD_FOLDER = os.path.join(BASE_FOLDER, 'uploads')
MAPPER_FOLDER = os.path.join(BASE_FOLDER, 'mapper')
MUSIC_FOLDER = os.path.join(BASE_FOLDER, 'music')
PICTURE_FOLDER = os.path.join(BASE_FOLDER, 'picture')

<<<<<<< Updated upstream
BASE_RETRIEVAL_FOLDER = os.path.abspath('retrieval')  # Path absolut ke folder media
RETRIEVAL_UPLOAD_FOLDER = os.path.join(BASE_FOLDER, 'uploads')
RETRIEVAL_MAPPER_FOLDER = os.path.join(BASE_FOLDER, 'mapper')
RETRIEVAL_MUSIC_FOLDER = os.path.join(BASE_FOLDER, 'music')
RETRIEVAL_PICTURE_FOLDER = os.path.join(BASE_FOLDER, 'picture')
=======
BASE_RETRIEVAL_FOLDER = os.path.abspath('src/react-app/src/media')  # Path absolut ke folder media
RETRIEVAL_UPLOAD_FOLDER = os.path.join(BASE_RETRIEVAL_FOLDER, 'test_uploads') 
RETRIEVAL_MAPPER_FOLDER = os.path.join(BASE_RETRIEVAL_FOLDER, 'test_mapper') 
RETRIEVAL_MUSIC_FOLDER = os.path.join(BASE_RETRIEVAL_FOLDER, 'test_music') 
RETRIEVAL_PICTURE_FOLDER = os.path.join(BASE_RETRIEVAL_FOLDER, 'test_picture') 
>>>>>>> Stashed changes
# Pastikan folder ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MAPPER_FOLDER, exist_ok=True)
os.makedirs(MUSIC_FOLDER, exist_ok=True)
os.makedirs(PICTURE_FOLDER, exist_ok=True)

os.makedirs(RETRIEVAL_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RETRIEVAL_MAPPER_FOLDER, exist_ok=True)
os.makedirs(RETRIEVAL_MUSIC_FOLDER, exist_ok=True)
os.makedirs(RETRIEVAL_PICTURE_FOLDER, exist_ok=True)

<<<<<<< Updated upstream
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
=======
# Endpoint untuk mendapatkan semua media
@app.route('/media', methods=['GET'])
def get_media():
    media_files = []
    # Menambahkan file dari folder mapper
    # for mapper in os.listdir(MAPPER_FOLDER):
    #     if mapper.endswith('.txt'):
    # if not os.path.exists(MUSIC_FOLDER):
    #     print("ERROR: MUSIC_FOLDER not found!")
    # else: 
    #     media_items = []
    #     try:
    #         file_path = os.path.join(MAPPER_FOLDER, 'mapper')
    #         with open(file_path, 'r') as file:
    #             for line in file:
    #                 parts = line.strip().split()  # Pisahkan baris menjadi bagian
    #                 if len(parts) == 2:  # hanya dua elemen per baris
    #                     media_items.append({
    #                         "audio_file": parts[0],
    #                         "pic_name": parts[1]
    #                     })
    #     except Exception as e:
    #         print(f"Error reading file {file_path}: {e}")
    #     media_items

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
    if not os.path.exists(RETRIEVAL_PICTURE_FOLDER):
        print("ERROR: RETRIEVAL_PICTURE_FOLDER notfound!")
    else:
        picture_files = os.listdir(RETRIEVAL_PICTURE_FOLDER)
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

>>>>>>> Stashed changes

# Endpoint untuk melayani file media
@app.route('/media/<folder>/<filename>', methods=['GET'])
def serve_media(folder, filename):
    folder_path = os.path.join(BASE_FOLDER, folder)
    file_path = os.path.join(folder_path, filename)

<<<<<<< Updated upstream
    # Log path untuk debugging
    print(f"Serving file from: {file_path}")
=======
    # Debug 6: Log file yang dilayani
    print(f"Serving file: {file_path}")
>>>>>>> Stashed changes
    print(f"File exists: {os.path.exists(file_path)}")

    if os.path.exists(file_path):
        return send_from_directory(folder_path, filename)
    else:
        return jsonify({"message": "File not found", "path": file_path}), 404

<<<<<<< Updated upstream
# Endpoint untuk mengunggah file umum
=======
# Endpoint untuk upload file
>>>>>>> Stashed changes
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'category' not in request.form:
        return jsonify({'message': 'No file part or category'}), 400

    file = request.files['file']
<<<<<<< Updated upstream
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
=======
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    query_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(query_file_path)
    result = image_retrieval_function(query_file_path)
    dataset_image = os.listdir(PICTURE_FOLDER)

    for i in range(len(result)):
        file_path = os.path.join(RETRIEVAL_PICTURE_FOLDER, dataset_image[result[i][0]])
        file.save(file_path)
    return jsonify({'message': 'File uploaded successfully'}), 200
    # if file:
>>>>>>> Stashed changes
    # elif file and category == 'music':
        # query_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        # result = image_retrieval_function(query_file_path)
        # for i in range(len(result)):
        #     query_file_path = os.path.join(BASE_RETRIEVAL_FOLDER, result[i][0])
        #     file.save(query_file_path)
        # return jsonify({'message': 'File uploaded successfully'}), 200
<<<<<<< Updated upstream


# Endpoint untuk mengunggah file ZIP berdasarkan kategori
=======
        
# Endpoint untuk upload file ZIP
>>>>>>> Stashed changes
@app.route('/upload_zip', methods=['POST'])
def upload_zip():
    if 'file' not in request.files or 'category' not in request.form:
        return jsonify({'message': 'No file part or category'}), 400

    file = request.files['file']
    category = request.form['category']
<<<<<<< Updated upstream

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
=======
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
>>>>>>> Stashed changes

if __name__ == '__main__':
    app.run(debug=True)
