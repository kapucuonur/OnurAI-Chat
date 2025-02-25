from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# .env dosyasındaki çevresel değişkenleri yükle
load_dotenv()

# Veritabanı nesnesi
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Veritabanını başlat
    db.init_app(app)

    # Blueprint'leri kaydet
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app