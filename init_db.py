#!/usr/bin/env python3
"""
Script đơn giản để khởi tạo database
"""

import os


def create_mysql_database_if_not_exists():
    from sqlalchemy.engine import create_engine
    from sqlalchemy.exc import OperationalError

    db_connection = os.environ.get("DB_CONNECTION", "sqlite")
    if db_connection != "mysql":
        return

    db_host = os.environ.get("DB_HOST", "127.0.0.1")
    db_port = int(os.environ.get("DB_PORT", 3306))
    db_database = os.environ.get("DB_DATABASE", "speak_app")
    db_username = os.environ.get("DB_USERNAME", "root")
    db_password = os.environ.get("DB_PASSWORD", "")

    # Kết nối tới MySQL mà không chỉ định database
    url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/"
    engine = create_engine(url)
    try:
        with engine.connect() as conn:
            conn.execute(
                f"CREATE DATABASE IF NOT EXISTS `{db_database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            )
            print(f"✅ Đã tạo database `{db_database}` (nếu chưa có)")
    except OperationalError as e:
        print("❌ Không thể kết nối MySQL để tạo database:", e)
    finally:
        engine.dispose()


create_mysql_database_if_not_exists()

from app import create_app, db
from app.models.user import User


def init_database():
    """Khởi tạo database và tạo tables"""
    app = create_app()

    with app.app_context():
        print("🔧 Đang tạo database...")

        # Tạo tất cả tables
        db.create_all()

        print("✅ Database đã được khởi tạo thành công!")
        print("📝 Bước tiếp theo:")
        print("1. Chạy: python run.py")
        print("2. Truy cập: http://localhost:5000")
        print("3. Đăng ký tài khoản mới")


if __name__ == "__main__":
    init_database()
