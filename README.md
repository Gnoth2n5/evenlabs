# 🎤 Speak - Ứng dụng Text-to-Speech với ElevenLabs API

Một ứng dụng web hoàn chỉnh cho phép chuyển đổi văn bản thành giọng nói chất lượng cao sử dụng ElevenLabs API, với các tính năng nâng cao như voice cloning, audio effects và quản lý projects.

## ✨ Tính năng chính

- **Text-to-Speech (TTS)**: Chuyển văn bản thành giọng nói với 1000+ giọng nói
- **Audio Effects**: Áp dụng các hiệu ứng âm thanh cho audio files
- **Project Management**: Quản lý và tổ chức audio files theo projects
- **Multi-language Support**: Hỗ trợ 29+ ngôn ngữ
- **Real-time Streaming**: Stream audio với độ trễ thấp
- **User Authentication**: Hệ thống đăng nhập/đăng ký an toàn

## 🛠️ Công nghệ sử dụng

### Backend

- **Flask 2.3.3** - Web framework
- **SQLAlchemy 3.0.5** - ORM database
- **ElevenLabs API** - Text-to-Speech service
- **Flask-Login 0.6.3** - User authentication
- **Pydub 0.25.1** - Audio processing
- **Werkzeug 2.3.7** - WSGI utilities

### Frontend

- **Tailwind CSS** - Styling framework
- **Alpine.js** - Lightweight JavaScript
- **HTMX** - Dynamic interactions

### Database

- **SQLite** (development) - Mặc định
- **MySQL** (production) - Tùy chọn

## 🚀 Hướng dẫn cài đặt

### Yêu cầu hệ thống

- **Python 3.8+**
- **pip** (Python package manager)
- **Git** (để clone repository)
- **ElevenLabs API Key** (đăng ký tại [elevenlabs.io](https://elevenlabs.io/))

### Bước 1: Clone repository

```bash
git clone https://github.com/Gnoth2n5/evenlabs
cd speak
```

### Bước 2: Tạo virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Bước 4: Cấu hình environment

```bash
# Copy file mẫu
cp env.example .env

# Chỉnh sửa file .env với thông tin của bạn
```

**Nội dung file `.env`:**

```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development

# Database Configuration
DB_CONNECTION=mysql

# MySQL Configuration (optional)
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=speak_app
DB_USERNAME=root
DB_PASSWORD=

# ElevenLabs API Configuration (BẮT BUỘC)
ELEVENLABS_API_KEY=your-elevenlabs-api-key-here

```

### Bước 5: Tạo DB trên phpMyAdmin trùng với DB trong env

### Bước 6: Khởi tạo database

```bash
python init_db.py
```

### Bước 7: Chạy ứng dụng

```bash
python run.py
```

Ứng dụng sẽ chạy tại: **http://localhost:5000**

## 🔧 Cấu hình chi tiết

### Lấy ElevenLabs API Key

1. Truy cập [ElevenLabs](https://elevenlabs.io/)
2. Đăng ký tài khoản miễn phí
3. Vào Dashboard → Profile Settings → API Key
4. Copy API key và thêm vào file `.env`

### Cấu hình MySQL (tùy chọn)

Nếu muốn sử dụng MySQL thay vì SQLite:

1. **Cài đặt MySQL Server**
2. **Cập nhật file `.env`:**

```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=speak_app
DB_USERNAME=root
DB_PASSWORD=your-mysql-password
```

3. **Chạy lại init_db.py:**

```bash
python init_db.py
```

## 🎯 Hướng dẫn sử dụng

### 1. Đăng ký tài khoản

1. Truy cập http://localhost:5000
2. Click "Đăng ký" để tạo tài khoản mới
3. Điền thông tin và tạo tài khoản

### 2. Text-to-Speech

1. Đăng nhập vào hệ thống
2. Truy cập **Text-to-Speech** từ menu
3. Nhập văn bản cần chuyển đổi
4. Chọn giọng nói và cài đặt:
   - **Voice**: Chọn giọng nói
   - **Stability**: Độ ổn định (0-1)
   - **Similarity Boost**: Tăng độ tương tự (0-1)
5. Click **"Generate"** để tạo audio
6. Download hoặc lưu audio file

### 3. Audio Effects

1. Truy cập **Audio Effects** từ menu
2. Upload audio file (MP3, WAV, FLAC, M4A, OGG)
3. Chọn hiệu ứng âm thanh:
   - **Volume**: Âm lượng (0-100%)
   - **Speed**: Tốc độ phát (0.5-2.0x)
   - **Pitch**: Cao độ (-12 đến +12 semitones)
   - **Echo**: Hiệu ứng echo (0-100%)
   - **Reverb**: Hiệu ứng reverb (0-100%)
4. Click **"Apply Effects"** để xử lý
5. Download audio đã xử lý

## 🔐 Bảo mật

- **API Key Encryption**: ElevenLabs API key được mã hóa
- **File Upload Validation**: Kiểm tra định dạng và kích thước file
- **Input Sanitization**: Làm sạch dữ liệu đầu vào
- **Session Security**: Cấu hình session an toàn
- **Password Hashing**: Mật khẩu được mã hóa với bcrypt

## 🚀 Deployment

### Development

```bash
python run.py
```

### Production với Gunicorn

```bash
# Cài đặt Gunicorn
pip install gunicorn

# Chạy với Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Production với Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

## 🐛 Troubleshooting

### Lỗi thường gặp

1. **"Module not found"**

   ```bash
   pip install -r requirements.txt
   ```

2. **"Database error"**

   ```bash
   python init_db.py
   ```

3. **"ElevenLabs API error"**

   - Kiểm tra API key trong file `.env`
   - Đảm bảo có credit trong ElevenLabs account

4. **"Port already in use"**
   ```bash
   # Thay đổi port trong run.py
   app.run(debug=True, host="0.0.0.0", port=5001)
   ```

### Logs

Kiểm tra logs để debug:

```bash
# Development
python run.py

# Production
gunicorn -w 4 -b 0.0.0.0:5000 run:app --log-level debug
```

## 📝 API Endpoints

### Authentication

- `POST /auth/register` - Đăng ký
- `POST /auth/login` - Đăng nhập
- `GET /auth/logout` - Đăng xuất

### Text-to-Speech

- `GET /tts` - Giao diện TTS
- `POST /tts/generate` - Tạo audio từ text
- `GET /tts/voices` - Lấy danh sách voices
- `GET /tts/models` - Lấy danh sách models
- `POST /tts/stream` - Stream audio
- `GET /tts/download/<id>` - Download audio file
- `POST /tts/delete/<id>` - Xóa audio file

### Audio Effects

- `GET /audio-effects` - Giao diện audio effects
- `POST /audio-effects/apply` - Áp dụng audio effects
- `POST /audio-effects/preview` - Preview audio effects
- `GET /audio-effects/download/<id>` - Download audio file
- `GET /audio-effects/library` - Thư viện hiệu ứng

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📄 License

Dự án này được phân phối dưới MIT License. Xem file `LICENSE` để biết thêm chi tiết.

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng:

1. Kiểm tra phần Troubleshooting
2. Tạo issue trên GitHub
3. Liên hệ qua email
