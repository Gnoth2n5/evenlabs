import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name="default"):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Configure MySQL engine if using MySQL
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("mysql://"):
        import pymysql

        pymysql.install_as_MySQLdb()

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)

    # Configure login manager
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Vui lòng đăng nhập để truy cập trang này."
    login_manager.login_message_category = "info"

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.tts import tts_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)
    app.register_blueprint(tts_bp, url_prefix="/tts")

    # Create upload directories if they don't exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["AUDIO_FOLDER"], exist_ok=True)

    # Import models to ensure they are registered with SQLAlchemy
    from app.models import user, audio

    return app


from app.models import user, audio
