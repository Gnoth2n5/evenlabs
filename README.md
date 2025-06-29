# 🎤 Speak - Web App Text-to-Speech với ElevenLabs API

Một web application hoàn chỉnh cho phép chuyển đổi văn bản thành giọng nói chất lượng cao sử dụng ElevenLabs API, với các tính năng nâng cao như voice cloning, voice changer và quản lý projects.

## ✨ Tính năng chính

- **Text-to-Speech (TTS)**: Chuyển văn bản thành giọng nói với 1000+ giọng nói
- **Voice Cloning**: Tạo giọng nói cá nhân từ audio sample
- **Voice Changer**: Chuyển đổi giọng nói trong audio files
- **Project Management**: Quản lý và tổ chức audio files
- **Multi-language Support**: Hỗ trợ 29+ ngôn ngữ
- **Real-time Streaming**: Stream audio với độ trễ thấp
- **User Authentication**: Hệ thống đăng nhập/đăng ký

## 🛠️ Công nghệ sử dụng

### Backend

- **Flask** - Web framework
- **SQLAlchemy** - ORM database
- **ElevenLabs API** - Text-to-Speech service
- **Flask-Login** - User authentication
- **Pydub** - Audio processing

### Frontend

- **Tailwind CSS** - Styling framework
- **Alpine.js** - Lightweight JavaScript
- **HTMX** - Dynamic interactions

### Database

- **SQLite** (development)
- **PostgreSQL** (production)

## 🚀 Cài đặt và chạy

### 1. Clone repository

```bash
git clone <repository-url>
cd speak
```

### 2. Tạo virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu hình environment

```bash
cp env.example .env
# Chỉnh sửa file .env với API key của bạn
```

### 5. Khởi tạo database

```bash
flask init-db
```

### 6. Tạo admin user (tùy chọn)

```bash
flask create-admin
```

### 7. Chạy ứng dụng

```bash
python run.py
# hoặc
flask run
```

Ứng dụng sẽ chạy tại `http://localhost:5000`

## 🔧 Cấu hình

### Environment Variables

Tạo file `.env` với các biến sau:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key
FLASK_APP=run.py
FLASK_ENV=development

# Database Configuration
DATABASE_URL=sqlite:///app.db

# ElevenLabs API Configuration
ELEVENLABS_API_KEY=your-elevenlabs-api-key

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379/0
```

### ElevenLabs API Key

1. Đăng ký tài khoản tại [ElevenLabs](https://elevenlabs.io/)
2. Lấy API key từ dashboard
3. Thêm API key vào file `.env`

## 📁 Cấu trúc dự án

```
speak/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes/              # Blueprint routes
│   │   ├── main.py         # Main routes
│   │   ├── tts.py          # Text-to-Speech routes
│   │   ├── voice_cloning.py # Voice cloning routes
│   │   ├── voice_changer.py # Voice changer routes
│   │   └── audio_effects.py # Audio effects routes
│   ├── models/              # Database models
│   │   ├── user.py         # User model
│   │   └── audio.py        # Audio models
│   ├── services/            # Business logic
│   │   └── elevenlabs_api.py # ElevenLabs API service
│   ├── static/              # Static files
│   │   ├── css/
│   │   ├── js/
│   │   ├── audio/          # Generated audio files
│   │   └── uploads/        # Uploaded files
│   ├── templates/           # HTML templates
│   └── utils/               # Utility functions
├── config.py               # Configuration
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🎯 Sử dụng

### Text-to-Speech

1. Đăng nhập vào hệ thống
2. Truy cập `/tts`
3. Nhập văn bản cần chuyển đổi
4. Chọn giọng nói và cài đặt
5. Click "Generate" để tạo audio

### Voice Cloning

1. Truy cập `/voice-cloning`
2. Upload audio samples (1-5 phút)
3. Đặt tên và mô tả cho voice
4. Click "Create Voice"

### Voice Changer

1. Truy cập `/voice-changer`
2. Upload audio file cần chuyển đổi
3. Chọn giọng nói đích
4. Click "Convert"

## 🔐 Security

- API key encryption
- File upload validation
- Rate limiting
- Input sanitization
- CORS configuration

## 🚀 Deployment

### Development

```bash
python run.py
```

### Production

```bash
# Sử dụng Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Với Docker
docker build -t speak-app .
docker run -p 5000:5000 speak-app
```

## 📊 API Endpoints

### Text-to-Speech

- `POST /tts/generate` - Tạo audio từ văn bản
- `POST /tts/stream` - Stream audio
- `GET /tts/voices` - Lấy danh sách giọng nói

### Voice Cloning

- `POST /voice-cloning/create` - Tạo voice mới
- `GET /voice-cloning/voices` - Lấy voice của user
- `DELETE /voice-cloning/delete/<voice_id>` - Xóa voice

### Voice Changer

- `POST /voice-changer/convert` - Chuyển đổi giọng nói
- `POST /voice-changer/preview` - Preview conversion

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Tạo Pull Request

## 📝 License

Dự án này được phát hành dưới MIT License. Xem file `LICENSE` để biết thêm chi tiết.

## 🆘 Support

Nếu gặp vấn đề, vui lòng:

1. Kiểm tra [Issues](https://github.com/your-repo/issues)
2. Tạo issue mới với mô tả chi tiết
3. Liên hệ qua email: support@example.com

## 🙏 Acknowledgments

- [ElevenLabs](https://elevenlabs.io/) - Cung cấp API Text-to-Speech
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework
