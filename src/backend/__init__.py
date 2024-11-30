from flask import Flask

app = Flask(__name__)

# Import route setelah aplikasi Flask diinisialisasi
from backend import routes
