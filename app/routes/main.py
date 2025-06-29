from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.audio import Project, AudioFile
from app.services.elevenlabs_api import ElevenLabsService

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Trang chủ"""
    return render_template("index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    """Dashboard cho user đã đăng nhập"""
    try:
        # Lấy thông tin user từ ElevenLabs
        elevenlabs_service = ElevenLabsService()
        user_info = elevenlabs_service.get_user_info()

        # Lấy projects và audio files của user
        projects = (
            Project.query.filter_by(user_id=current_user.id)
            .order_by(Project.created_at.desc())
            .limit(5)
            .all()
        )
        recent_audio = (
            AudioFile.query.filter_by(user_id=current_user.id)
            .order_by(AudioFile.created_at.desc())
            .limit(10)
            .all()
        )

        return render_template(
            "dashboard.html",
            projects=projects,
            recent_audio=recent_audio,
            user_info=user_info,
        )
    except Exception as e:
        flash(f"Lỗi khi tải dashboard: {str(e)}", "error")
        return render_template(
            "dashboard.html", projects=[], recent_audio=[], user_info={"success": False}
        )


@main_bp.route("/about")
def about():
    """Trang giới thiệu"""
    return render_template("about.html")


@main_bp.route("/contact")
def contact():
    """Trang liên hệ"""
    return render_template("contact.html")
