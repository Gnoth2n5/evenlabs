from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Đăng nhập"""
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Vui lòng nhập đầy đủ thông tin", "error")
            return redirect(url_for("auth.login"))

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get("next")
            if not next_page or not next_page.startswith("/"):
                next_page = url_for("main.dashboard")
            return redirect(next_page)
        else:
            flash("Tên đăng nhập hoặc mật khẩu không đúng", "error")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    """Đăng xuất"""
    logout_user()
    flash("Bạn đã đăng xuất thành công", "success")
    return redirect(url_for("main.index"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Đăng ký"""
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Validation
        if not username or not email or not password:
            flash("Vui lòng nhập đầy đủ thông tin", "error")
            return redirect(url_for("auth.register"))

        if password != confirm_password:
            flash("Mật khẩu xác nhận không khớp", "error")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(username=username).first():
            flash("Tên đăng nhập đã tồn tại", "error")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("Email đã được sử dụng", "error")
            return redirect(url_for("auth.register"))

        # Tạo user mới
        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Đăng ký thành công! Vui lòng đăng nhập", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")
