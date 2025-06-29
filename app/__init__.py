import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_name="default"):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Configure login manager
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Vui lòng đăng nhập để truy cập trang này."
    login_manager.login_message_category = "info"

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.tts import tts_bp
    from app.routes.voice_cloning import voice_cloning_bp
    from app.routes.voice_changer import voice_changer_bp
    from app.routes.audio_effects import audio_effects_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)
    app.register_blueprint(tts_bp, url_prefix="/tts")
    app.register_blueprint(voice_cloning_bp, url_prefix="/voice-cloning")
    app.register_blueprint(voice_changer_bp, url_prefix="/voice-changer")
    app.register_blueprint(audio_effects_bp, url_prefix="/audio-effects")

    # Create upload directories if they don't exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["AUDIO_FOLDER"], exist_ok=True)

    # Import models to ensure they are registered with SQLAlchemy
    from app.models import user, audio

    return app


from app.models import user, audio
