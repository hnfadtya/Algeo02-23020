from flask import request, render_template
from backend.image_retrieval.pca import image_retrieval_function  # Fungsi Image Retrieval
from backend.music_retrieval.humming import music_retrieval_function  # Fungsi Music Retrieval
from backend import app

@app.route('/')
def index():
    return render_template('index.html')  # Halaman utama

@app.route('/query_image', methods=['POST'])
def query_image():
    if 'image' not in request.files:
        return "No file uploaded"
    
    image = request.files['image']
    
    # Proses gambar menggunakan Image Retrieval (PCA)
    result = image_retrieval_function(image)  # Gantilah dengan fungsi yang Anda buat
    
    return render_template('results.html', results=result)

@app.route('/query_audio', methods=['POST'])
def query_audio():
    if 'audio' not in request.files:
        return "No file uploaded"
    
    audio = request.files['audio']
    
    # Proses audio menggunakan Music Retrieval (Humming)
    result = music_retrieval_function(audio)  # Gantilah dengan fungsi yang Anda buat
    
    return render_template('results.html', results=result)
