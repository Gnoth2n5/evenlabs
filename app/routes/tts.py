import os
import uuid
from datetime import datetime
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    send_file,
    flash,
    redirect,
    url_for,
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models.audio import Project, AudioFile
from app.services.elevenlabs_api import ElevenLabsService
from app.utils.helpers import allowed_file, get_file_extension

tts_bp = Blueprint("tts", __name__)


@tts_bp.route("/")
@login_required
def index():
    """Trang TTS chính"""
    try:
        # Lấy danh sách voices từ ElevenLabs
        elevenlabs_service = ElevenLabsService()
        voices_result = elevenlabs_service.get_voices()

        if voices_result["success"]:
            voices = voices_result["voices"]
        else:
            voices = []
            flash(f"Không thể tải voices: {voices_result['error']}", "error")

        # Lấy projects của user
        projects = Project.query.filter_by(user_id=current_user.id).all()

        return render_template("tts/index.html", voices=voices, projects=projects)
    except Exception as e:
        flash(f"Lỗi: {str(e)}", "error")
        return render_template("tts/index.html", voices=[], projects=[])


@tts_bp.route("/models")
@login_required
def get_models():
    """API endpoint để lấy danh sách models"""
    try:
        elevenlabs_service = ElevenLabsService()
        result = elevenlabs_service.get_models()
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@tts_bp.route("/generate", methods=["POST"])
@login_required
def generate_speech():
    """Tạo speech từ text"""
    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        voice_id = data.get("voice_id", "21m00Tcm4TlvDq8ikWAM")
        model_id = data.get("model_id", "eleven_multilingual_v2")
        project_id = data.get("project_id")

        if not text:
            return jsonify({"success": False, "error": "Vui lòng nhập text"})

        # Tạo ElevenLabs service
        elevenlabs_service = ElevenLabsService()

        # Generate speech
        result = elevenlabs_service.text_to_speech(text, voice_id, model_id)

        if result["success"]:
            # Lưu vào database
            audio_file = AudioFile(
                user_id=current_user.id,
                project_id=project_id,
                filename=os.path.basename(result["file_path"]),
                original_filename=f"tts_{uuid.uuid4().hex[:8]}.mp3",
                file_path=result["file_path"],
                file_size=os.path.getsize(result["file_path"]),
                format="mp3",
                duration=result["duration"],
                voice_id=voice_id,
                text_content=text,
            )

            db.session.add(audio_file)
            db.session.commit()

            return jsonify(
                {
                    "success": True,
                    "audio_id": audio_file.id,
                    "audio_url": f"/tts/download/{audio_file.id}",
                    "filename": audio_file.original_filename,
                    "duration": result["duration"],
                }
            )
        else:
            return jsonify({"success": False, "error": result["error"]})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@tts_bp.route("/stream", methods=["POST"])
@login_required
def stream_speech():
    """Stream audio từ văn bản"""
    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        voice_id = data.get("voice_id")
        settings = data.get("settings", {})

        if not text or not voice_id:
            return jsonify({"error": "Văn bản và giọng nói là bắt buộc"}), 400

        api = ElevenLabsService()
        response = api.text_to_speech_stream(text, voice_id, **settings)

        return response

    except Exception as e:
        return jsonify({"error": f"Lỗi khi stream audio: {str(e)}"}), 500


@tts_bp.route("/voices")
@login_required
def get_voices():
    """API endpoint để lấy danh sách voices"""
    try:
        elevenlabs_service = ElevenLabsService()
        result = elevenlabs_service.get_voices()
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@tts_bp.route("/download/<int:audio_id>")
@login_required
def download_audio(audio_id):
    """Download audio file"""
    try:
        audio_file = AudioFile.query.filter_by(
            id=audio_id, user_id=current_user.id
        ).first()

        if not audio_file:
            flash("Audio file không tồn tại", "error")
            return redirect(url_for("tts.index"))

        if not os.path.exists(audio_file.file_path):
            flash("File không tồn tại trên server", "error")
            return redirect(url_for("tts.index"))

        return send_file(
            audio_file.file_path,
            as_attachment=True,
            download_name=audio_file.original_filename,
        )

    except Exception as e:
        flash(f"Lỗi khi download: {str(e)}", "error")
        return redirect(url_for("tts.index"))


@tts_bp.route("/delete/<int:audio_id>", methods=["POST"])
@login_required
def delete_audio(audio_id):
    """Xóa audio file"""
    audio_file = AudioFile.query.get_or_404(audio_id)

    # Kiểm tra quyền truy cập
    if audio_file.project.user_id != current_user.id:
        return jsonify({"error": "Bạn không có quyền xóa file này"}), 403

    try:
        # Xóa file từ disk
        if os.path.exists(audio_file.file_path):
            os.remove(audio_file.file_path)

        # Xóa từ database
        db.session.delete(audio_file)
        db.session.commit()

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": f"Lỗi khi xóa file: {str(e)}"}), 500
