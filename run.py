import os
from app import create_app, db
from app.models.user import User
from app.models.audio import Project, AudioFile, VoiceModel

app = create_app(os.getenv("FLASK_ENV") or "default")


@app.shell_context_processor
def make_shell_context():
    """Tạo context cho Flask shell"""
    return {
        "db": db,
        "User": User,
        "Project": Project,
        "AudioFile": AudioFile,
        "VoiceModel": VoiceModel,
    }


@app.cli.command()
def init_db():
    """Khởi tạo database"""
    db.create_all()
    print("Database đã được khởi tạo!")


@app.cli.command()
def create_admin():
    """Tạo admin user"""
    username = input("Nhập username: ")
    email = input("Nhập email: ")
    password = input("Nhập password: ")

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    print(f"Admin user {username} đã được tạo!")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
