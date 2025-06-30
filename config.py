import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    """Base configuration class"""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"

    # Database configuration - đơn giản hóa
    DB_CONNECTION = os.environ.get("DB_CONNECTION", "sqlite")

    if DB_CONNECTION == "mysql":
        # MySQL configuration
        DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
        DB_PORT = int(os.environ.get("DB_PORT", 3306))
        DB_DATABASE = os.environ.get("DB_DATABASE", "speak_app")
        DB_USERNAME = os.environ.get("DB_USERNAME", "root")
        DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

        SQLALCHEMY_DATABASE_URI = (
            f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
        )
    else:
        # SQLite configuration (default) - luôn sử dụng SQLite nếu không có .env
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ElevenLabs API Configuration
    ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
    ELEVENLABS_BASE_URL = "https://api.elevenlabs.io/v1"

    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(basedir, "app/static/uploads")
    AUDIO_FOLDER = os.path.join(basedir, "app/static/audio")
    ALLOWED_EXTENSIONS = {"mp3", "wav", "flac", "m4a", "ogg"}

    # Redis configuration (optional)
    REDIS_URL = os.environ.get("REDIS_URL") or "redis://localhost:6379/0"

    # Pagination
    POSTS_PER_PAGE = 10

    # Security
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Email configuration (optional)
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 587)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in ["true", "on", "1"]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    # Logging
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
