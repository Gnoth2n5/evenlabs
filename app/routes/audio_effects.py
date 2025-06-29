import os
import uuid
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    flash,
    redirect,
    url_for,
    send_file,
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models.audio import Project, AudioFile
from app.services.elevenlabs_api import ElevenLabsService
from app.utils.helpers import allowed_file, get_file_extension

audio_effects_bp = Blueprint("audio_effects", __name__)


@audio_effects_bp.route("/")
@login_required
def index():
    """Trang chính cho Audio Effects"""
    try:
        # Lấy projects của user
        projects = Project.query.filter_by(user_id=current_user.id).all()

        return render_template("audio_effects/index.html", projects=projects)
    except Exception as e:
        flash(f"Lỗi: {str(e)}", "error")
        return render_template("audio_effects/index.html", projects=[])


@audio_effects_bp.route("/apply", methods=["POST"])
@login_required
def apply_effects():
    """Áp dụng hiệu ứng âm thanh"""
    try:
        if "audio_file" not in request.files:
            return jsonify({"success": False, "error": "Không có file được chọn"})

        file = request.files["audio_file"]
        project_id = request.form.get("project_id")

        # Lấy các tham số hiệu ứng
        volume = float(request.form.get("volume", 100)) / 100
        speed = float(request.form.get("speed", 1.0))
        pitch = int(request.form.get("pitch", 0))
        echo = float(request.form.get("echo", 0)) / 100
        reverb = float(request.form.get("reverb", 0)) / 100

        if file.filename == "":
            return jsonify({"success": False, "error": "Không có file được chọn"})

        if not allowed_file(file.filename):
            return jsonify({"success": False, "error": "File type không được hỗ trợ"})

        # Lưu file tạm thời
        filename = secure_filename(file.filename)
        temp_path = os.path.join("/tmp", f"{uuid.uuid4()}_{filename}")
        file.save(temp_path)

        # Tạo ElevenLabs service
        elevenlabs_service = ElevenLabsService()

        # Áp dụng hiệu ứng (sử dụng voice conversion với voice gốc)
        result = elevenlabs_service.voice_conversion(temp_path, "21m00Tcm4TlvDq8ikWAM")

        if result["success"]:
            # Lưu vào database
            audio_file = AudioFile(
                user_id=current_user.id,
                project_id=project_id,
                filename=os.path.basename(result["file_path"]),
                original_filename=f"effects_{uuid.uuid4().hex[:8]}.mp3",
                file_path=result["file_path"],
                file_size=os.path.getsize(result["file_path"]),
                format="mp3",
                settings={
                    "volume": volume,
                    "speed": speed,
                    "pitch": pitch,
                    "echo": echo,
                    "reverb": reverb,
                },
            )

            db.session.add(audio_file)
            db.session.commit()

            return jsonify(
                {
                    "success": True,
                    "audio_id": audio_file.id,
                    "audio_url": f"/audio-effects/download/{audio_file.id}",
                    "filename": audio_file.original_filename,
                }
            )
        else:
            return jsonify({"success": False, "error": result["error"]})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@audio_effects_bp.route("/preview", methods=["POST"])
@login_required
def preview_effects():
    """Preview audio effects"""
    try:
        if "audio_file" not in request.files:
            return jsonify({"success": False, "error": "Không có file được chọn"})

        file = request.files["audio_file"]

        # Lấy các tham số hiệu ứng
        volume = float(request.form.get("volume", 100)) / 100
        speed = float(request.form.get("speed", 1.0))
        pitch = int(request.form.get("pitch", 0))
        echo = float(request.form.get("echo", 0)) / 100
        reverb = float(request.form.get("reverb", 0)) / 100

        if file.filename == "":
            return jsonify({"success": False, "error": "Không có file được chọn"})

        # Lưu file tạm thời
        filename = secure_filename(file.filename)
        temp_path = os.path.join("/tmp", f"preview_{uuid.uuid4()}_{filename}")
        file.save(temp_path)

        # Tạo ElevenLabs service
        elevenlabs_service = ElevenLabsService()

        # Preview effects
        result = elevenlabs_service.voice_conversion(temp_path, "21m00Tcm4TlvDq8ikWAM")

        if result["success"]:
            return jsonify(
                {
                    "success": True,
                    "preview_url": f'/audio-effects/preview/{os.path.basename(result["file_path"])}',
                }
            )
        else:
            return jsonify({"success": False, "error": result["error"]})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@audio_effects_bp.route("/download/<int:audio_id>")
@login_required
def download_audio(audio_id):
    """Download audio file"""
    try:
        audio_file = AudioFile.query.filter_by(
            id=audio_id, user_id=current_user.id
        ).first()

        if not audio_file:
            flash("Audio file không tồn tại", "error")
            return redirect(url_for("audio_effects.index"))

        if not os.path.exists(audio_file.file_path):
            flash("File không tồn tại trên server", "error")
            return redirect(url_for("audio_effects.index"))

        return send_file(
            audio_file.file_path,
            as_attachment=True,
            download_name=audio_file.original_filename,
        )

    except Exception as e:
        flash(f"Lỗi khi download: {str(e)}", "error")
        return redirect(url_for("audio_effects.index"))


@audio_effects_bp.route("/library")
@login_required
def effects_library():
    """Thư viện hiệu ứng âm thanh"""
    # TODO: Implement effects library
    effects = [
        {"id": 1, "name": "Nature Sounds", "category": "ambient"},
        {"id": 2, "name": "City Sounds", "category": "urban"},
        {"id": 3, "name": "Music Elements", "category": "music"},
        {"id": 4, "name": "SFX", "category": "effects"},
    ]

    return render_template("audio_effects/library.html", effects=effects)
