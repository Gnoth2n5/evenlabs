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
from app.models.audio import AudioFile, Project
from app.services.elevenlabs_api import ElevenLabsService
from app.utils.helpers import allowed_file, get_file_extension

voice_changer_bp = Blueprint("voice_changer", __name__)


@voice_changer_bp.route("/")
@login_required
def index():
    """Trang chính cho Voice Changer"""
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

        return render_template(
            "voice_changer/index.html", voices=voices, projects=projects
        )
    except Exception as e:
        flash(f"Lỗi: {str(e)}", "error")
        return render_template("voice_changer/index.html", voices=[], projects=[])


@voice_changer_bp.route("/convert", methods=["POST"])
@login_required
def convert_voice():
    """Chuyển đổi voice trong audio file"""
    try:
        if "audio_file" not in request.files:
            return jsonify({"success": False, "error": "Không có file được chọn"})

        file = request.files["audio_file"]
        voice_id = request.form.get("voice_id")
        project_id = request.form.get("project_id")

        if file.filename == "":
            return jsonify({"success": False, "error": "Không có file được chọn"})

        if not voice_id:
            return jsonify({"success": False, "error": "Vui lòng chọn voice đích"})

        if not allowed_file(file.filename):
            return jsonify({"success": False, "error": "File type không được hỗ trợ"})

        # Lưu file tạm thời
        filename = secure_filename(file.filename)
        temp_path = os.path.join("/tmp", f"{uuid.uuid4()}_{filename}")
        file.save(temp_path)

        # Tạo ElevenLabs service
        elevenlabs_service = ElevenLabsService()

        # Chuyển đổi voice
        result = elevenlabs_service.voice_conversion(temp_path, voice_id)

        if result["success"]:
            # Lưu vào database
            audio_file = AudioFile(
                user_id=current_user.id,
                project_id=project_id,
                filename=os.path.basename(result["file_path"]),
                original_filename=f"voice_changed_{uuid.uuid4().hex[:8]}.mp3",
                file_path=result["file_path"],
                file_size=os.path.getsize(result["file_path"]),
                format="mp3",
                voice_id=voice_id,
            )

            db.session.add(audio_file)
            db.session.commit()

            return jsonify(
                {
                    "success": True,
                    "audio_id": audio_file.id,
                    "audio_url": f"/voice-changer/download/{audio_file.id}",
                    "filename": audio_file.original_filename,
                }
            )
        else:
            return jsonify({"success": False, "error": result["error"]})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@voice_changer_bp.route("/preview", methods=["POST"])
@login_required
def preview_voice():
    """Preview voice conversion"""
    try:
        if "audio_file" not in request.files:
            return jsonify({"success": False, "error": "Không có file được chọn"})

        file = request.files["audio_file"]
        voice_id = request.form.get("voice_id")

        if file.filename == "":
            return jsonify({"success": False, "error": "Không có file được chọn"})

        if not voice_id:
            return jsonify({"success": False, "error": "Vui lòng chọn voice đích"})

        # Lưu file tạm thời
        filename = secure_filename(file.filename)
        temp_path = os.path.join("/tmp", f"preview_{uuid.uuid4()}_{filename}")
        file.save(temp_path)

        # Tạo ElevenLabs service
        elevenlabs_service = ElevenLabsService()

        # Preview voice conversion
        result = elevenlabs_service.voice_conversion(temp_path, voice_id)

        if result["success"]:
            return jsonify(
                {
                    "success": True,
                    "preview_url": f'/voice-changer/preview/{os.path.basename(result["file_path"])}',
                }
            )
        else:
            return jsonify({"success": False, "error": result["error"]})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@voice_changer_bp.route("/download/<int:audio_id>")
@login_required
def download_audio(audio_id):
    """Download audio file"""
    try:
        audio_file = AudioFile.query.filter_by(
            id=audio_id, user_id=current_user.id
        ).first()

        if not audio_file:
            flash("Audio file không tồn tại", "error")
            return redirect(url_for("voice_changer.index"))

        if not os.path.exists(audio_file.file_path):
            flash("File không tồn tại trên server", "error")
            return redirect(url_for("voice_changer.index"))

        return send_file(
            audio_file.file_path,
            as_attachment=True,
            download_name=audio_file.original_filename,
        )

    except Exception as e:
        flash(f"Lỗi khi download: {str(e)}", "error")
        return redirect(url_for("voice_changer.index"))


@voice_changer_bp.route("/voices")
@login_required
def get_voices():
    """API endpoint để lấy danh sách voices"""
    try:
        elevenlabs_service = ElevenLabsService()
        result = elevenlabs_service.get_voices()
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
