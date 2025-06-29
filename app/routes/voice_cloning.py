import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models.audio import VoiceModel, Project, AudioFile
from app.services.elevenlabs_api import ElevenLabsService
from app.utils.helpers import allowed_file, get_file_extension

voice_cloning_bp = Blueprint("voice_cloning", __name__)


@voice_cloning_bp.route("/")
@login_required
def index():
    """Trang chính cho Voice Cloning"""
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
            "voice_cloning/index.html", voices=voices, projects=projects
        )
    except Exception as e:
        flash(f"Lỗi: {str(e)}", "error")
        return render_template("voice_cloning/index.html", voices=[], projects=[])


@voice_cloning_bp.route("/create-voice", methods=["GET", "POST"])
@login_required
def create_voice():
    """Tạo voice mới"""
    if request.method == "GET":
        return render_template("voice_cloning/create_voice.html")

    try:
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        files = request.files.getlist("audio_files")

        if not name:
            flash("Tên voice không được để trống", "error")
            return redirect(url_for("voice_cloning.create_voice"))

        if not files or all(file.filename == "" for file in files):
            flash("Vui lòng chọn ít nhất một file audio", "error")
            return redirect(url_for("voice_cloning.create_voice"))

        # Lưu files tạm thời
        temp_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                temp_path = os.path.join("/tmp", f"{uuid.uuid4()}_{filename}")
                file.save(temp_path)
                temp_files.append(temp_path)

        # Tạo ElevenLabs service
        elevenlabs_service = ElevenLabsService()

        # Clone voice
        result = elevenlabs_service.clone_voice(name, description, temp_files)

        if result["success"]:
            flash(f'Voice "{name}" đã được tạo thành công!', "success")
            return redirect(url_for("voice_cloning.index"))
        else:
            flash(f"Lỗi khi tạo voice: {result['error']}", "error")
            return redirect(url_for("voice_cloning.create_voice"))

    except Exception as e:
        flash(f"Lỗi: {str(e)}", "error")
        return redirect(url_for("voice_cloning.create_voice"))


@voice_cloning_bp.route("/voices")
@login_required
def get_voices():
    """API endpoint để lấy danh sách voices"""
    try:
        elevenlabs_service = ElevenLabsService()
        result = elevenlabs_service.get_voices()
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@voice_cloning_bp.route("/delete-voice/<voice_id>", methods=["POST"])
@login_required
def delete_voice(voice_id):
    """Xóa voice"""
    try:
        elevenlabs_service = ElevenLabsService()
        result = elevenlabs_service.delete_voice(voice_id)

        if result["success"]:
            flash("Voice đã được xóa thành công", "success")
        else:
            flash(f"Lỗi khi xóa voice: {result['error']}", "error")

        return redirect(url_for("voice_cloning.index"))

    except Exception as e:
        flash(f"Lỗi: {str(e)}", "error")
        return redirect(url_for("voice_cloning.index"))


@voice_cloning_bp.route("/<voice_id>")
@login_required
def voice_details(voice_id):
    """Chi tiết voice"""
    try:
        # Lấy thông tin voice từ ElevenLabs
        api = ElevenLabsService()
        voice_info = api.get_voice(voice_id)

        # Kiểm tra voice có thuộc user không
        voice_model = VoiceModel.query.filter_by(
            user_id=current_user.id, voice_id=voice_id
        ).first()

        if not voice_model:
            flash("Voice không tồn tại hoặc không thuộc về bạn", "error")
            return redirect(url_for("voice_cloning.index"))

        return render_template(
            "voice_cloning/details.html", voice_info=voice_info, voice_model=voice_model
        )

    except Exception as e:
        flash(f"Lỗi khi tải thông tin voice: {str(e)}", "error")
        return redirect(url_for("voice_cloning.index"))
