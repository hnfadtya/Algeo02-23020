from flask import request, render_template
from backend.image_retrieval.retrieval import image_retrieval_function
from backend.music_retrieval.humming import music_retrieval_function
from backend import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query_image', methods=['POST'])
def query_image():
    if 'image' not in request.files:
        return "No file uploaded"
    image = request.files['image']
    result = image_retrieval_function(image)
    return render_template('results.html', results=result)

@app.route('/query_audio', methods=['POST'])
def query_audio():
    if 'audio' not in request.files:
        return "No file uploaded"
    audio = request.files['audio']
    result = music_retrieval_function(audio)
    return render_template('results.html', results=result)
