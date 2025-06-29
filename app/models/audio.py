from datetime import datetime
from app import db


class Project(db.Model):
    """Project model for organizing audio files"""

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    audio_files = db.relationship(
        "AudioFile", backref="project", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Project {self.name}>"


class AudioFile(db.Model):
    """Audio file model for storing generated audio"""

    __tablename__ = "audio_files"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255))
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    duration = db.Column(db.Float)  # Duration in seconds
    format = db.Column(db.String(10))  # mp3, wav, flac, etc.
    voice_id = db.Column(db.String(100))  # ElevenLabs voice ID
    voice_name = db.Column(db.String(100))
    text_content = db.Column(db.Text)  # Original text used for TTS
    settings = db.Column(db.JSON)  # TTS settings (speed, pitch, etc.)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AudioFile {self.filename}>"


class VoiceModel(db.Model):
    """Voice model for storing voice information"""

    __tablename__ = "voice_models"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    voice_id = db.Column(db.String(100), nullable=False)  # ElevenLabs voice ID
    is_cloned = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    language = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    age_group = db.Column(db.String(20))
    accent = db.Column(db.String(50))
    sample_file_path = db.Column(db.String(500))  # Path to sample audio file
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<VoiceModel {self.name}>"
