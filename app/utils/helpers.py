import os
from flask import current_app
from werkzeug.utils import secure_filename


def allowed_file(filename):
    """Kiểm tra file extension có được phép không"""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


def get_file_extension(filename):
    """Lấy extension của file"""
    if "." in filename:
        return filename.rsplit(".", 1)[1].lower()
    return ""


def secure_filename_with_path(filename, folder="uploads"):
    """Tạo secure filename với path"""
    filename = secure_filename(filename)
    return os.path.join(folder, filename)


def format_file_size(size_bytes):
    """Format file size thành human readable"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math

    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"


def format_duration(seconds):
    """Format duration thành human readable"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.1f}s"
    else:
        hours = int(seconds // 3600)
        remaining_minutes = int((seconds % 3600) // 60)
        remaining_seconds = seconds % 60
        return f"{hours}h {remaining_minutes}m {remaining_seconds:.1f}s"


def get_voice_display_name(voice):
    """Lấy tên hiển thị cho voice"""
    if voice.get("labels"):
        return voice["labels"].get("name", voice.get("name", "Unknown"))
    return voice.get("name", "Unknown")


def get_voice_language(voice):
    """Lấy ngôn ngữ của voice"""
    if voice.get("labels"):
        return voice["labels"].get("language", "Unknown")
    return "Unknown"


def get_voice_gender(voice):
    """Lấy giới tính của voice"""
    if voice.get("labels"):
        return voice["labels"].get("gender", "Unknown")
    return "Unknown"


def validate_text_length(text, max_length=5000):
    """Validate độ dài text"""
    if not text or len(text.strip()) == 0:
        return False, "Văn bản không được để trống"

    if len(text) > max_length:
        return False, f"Văn bản quá dài (tối đa {max_length} ký tự)"

    return True, "OK"


def sanitize_filename(filename):
    """Sanitize filename để tránh path traversal"""
    # Loại bỏ các ký tự nguy hiểm
    dangerous_chars = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]
    for char in dangerous_chars:
        filename = filename.replace(char, "_")

    # Giới hạn độ dài
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[: 255 - len(ext)] + ext

    return filename
