from flask import Flask

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Konfigurasi tambahan (opsional)
app.config['UPLOAD_FOLDER'] = 'dataset/query/'  # Tempat penyimpanan file yang diunggah
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Maksimal ukuran file 16 MB

# Import rute setelah aplikasi diinisialisasi
from backend import routes
