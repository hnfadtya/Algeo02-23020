from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'src/uploads'  # Folder tempat menyimpan file yang diunggah
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Endpoint untuk API upload file
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return {"message": "File uploaded successfully!"}, 200

# Menyajikan React dari root folder
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    # Jika path mengarah ke file statis (misalnya vite.svg), kembalikan file tersebut
    if path != "" and os.path.exists(f"react-app/{path}"):
        return send_from_directory('react-app', path)
    # Default: kirimkan index.html
    return send_from_directory('react-app', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
