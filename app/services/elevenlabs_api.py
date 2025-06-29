import os
import logging
from elevenlabs import generate, save, set_api_key, voices, Voice, VoiceSettings
from elevenlabs.api import History
from elevenlabs import clone
import tempfile
import uuid
import requests

logger = logging.getLogger(__name__)


class ElevenLabsService:
    """Service để tương tác với ElevenLabs API"""

    def __init__(self):
        """Khởi tạo service với API key"""
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            raise ValueError("ELEVENLABS_API_KEY không được cấu hình")

        set_api_key(api_key)
        self.api_key = api_key

    def get_user_info(self):
        """Lấy thông tin user"""
        try:
            # Sử dụng API call trực tiếp để lấy user info
            url = "https://api.elevenlabs.io/v1/user"
            headers = {"Accept": "application/json", "xi-api-key": self.api_key}

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                user_data = response.json()
                return {
                    "success": True,
                    "data": {
                        "subscription_tier": user_data.get("subscription", {}).get(
                            "tier", "free"
                        ),
                        "character_count": user_data.get("subscription", {}).get(
                            "character_count", 0
                        ),
                        "character_limit": user_data.get("subscription", {}).get(
                            "character_limit", 10000
                        ),
                    },
                }
            else:
                logger.error(
                    f"ElevenLabs API error: {response.status_code} - {response.text}"
                )
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                }

        except Exception as e:
            logger.error(f"ElevenLabs API error: {e}")
            return {"success": False, "error": str(e)}

    def get_voices(self):
        """Lấy danh sách voices có sẵn"""
        try:
            available_voices = voices()
            return {
                "success": True,
                "voices": [
                    {
                        "voice_id": voice.voice_id,
                        "name": voice.name,
                        "category": voice.category,
                        "description": voice.description,
                        "labels": voice.labels,
                        "preview_url": voice.preview_url,
                    }
                    for voice in available_voices
                ],
            }
        except Exception as e:
            logger.error(f"ElevenLabs API error: {e}")
            return {"success": False, "error": str(e)}

    def get_models(self):
        """Lấy danh sách các model có sẵn"""
        try:
            url = "https://api.elevenlabs.io/v1/models"
            headers = {"Accept": "application/json", "xi-api-key": self.api_key}

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                models_data = response.json()
                return {"success": True, "models": models_data}
            else:
                logger.error(
                    f"ElevenLabs models API error: {response.status_code} - {response.text}"
                )
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                }

        except Exception as e:
            logger.error(f"ElevenLabs models API error: {e}")
            return {"success": False, "error": str(e)}

    def text_to_speech(
        self, text, voice_id="21m00Tcm4TlvDq8ikWAM", model_id="eleven_multilingual_v2"
    ):
        """Chuyển text thành speech"""
        try:
            # Tạo file tạm để lưu audio
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_path = temp_file.name
            temp_file.close()

            # Generate audio
            audio = generate(text=text, voice=voice_id, model=model_id)

            # Lưu audio
            save(audio, temp_path)

            return {
                "success": True,
                "file_path": temp_path,
                "duration": len(audio) / 22050,  # Ước tính duration
            }

        except Exception as e:
            logger.error(f"ElevenLabs TTS error: {e}")
            return {"success": False, "error": str(e)}

    def clone_voice(self, name, description, files):
        """Clone voice từ audio files"""
        try:
            # Clone voice
            voice = clone(name=name, description=description, files=files)

            return {
                "success": True,
                "voice_id": voice.voice_id,
                "name": voice.name,
                "description": voice.description,
            }

        except Exception as e:
            logger.error(f"ElevenLabs voice cloning error: {e}")
            return {"success": False, "error": str(e)}

    def voice_conversion(self, input_audio_path, voice_id):
        """Chuyển đổi voice trong audio file"""
        try:
            # ElevenLabs có API voice conversion
            url = f"https://api.elevenlabs.io/v1/voice-conversion/{voice_id}"
            headers = {"Accept": "audio/mpeg", "xi-api-key": self.api_key}

            with open(input_audio_path, "rb") as audio_file:
                files = {"audio": audio_file}
                response = requests.post(url, headers=headers, files=files)

            if response.status_code == 200:
                # Tạo file tạm cho output
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                temp_path = temp_file.name
                temp_file.close()

                # Lưu audio đã chuyển đổi
                with open(temp_path, "wb") as f:
                    f.write(response.content)

                return {
                    "success": True,
                    "file_path": temp_path,
                    "message": "Voice conversion completed",
                }
            else:
                logger.error(
                    f"Voice conversion error: {response.status_code} - {response.text}"
                )
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                }

        except Exception as e:
            logger.error(f"ElevenLabs voice conversion error: {e}")
            return {"success": False, "error": str(e)}

    def get_voice_by_id(self, voice_id):
        """Lấy thông tin voice theo ID"""
        try:
            available_voices = voices()
            for voice in available_voices:
                if voice.voice_id == voice_id:
                    return {
                        "success": True,
                        "voice": {
                            "voice_id": voice.voice_id,
                            "name": voice.name,
                            "category": voice.category,
                            "description": voice.description,
                            "labels": voice.labels,
                            "preview_url": voice.preview_url,
                        },
                    }

            return {"success": False, "error": "Voice không tồn tại"}

        except Exception as e:
            logger.error(f"ElevenLabs API error: {e}")
            return {"success": False, "error": str(e)}

    def delete_voice(self, voice_id):
        """Xóa voice"""
        try:
            url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"
            headers = {"Accept": "application/json", "xi-api-key": self.api_key}

            response = requests.delete(url, headers=headers)

            if response.status_code == 200:
                return {"success": True, "message": "Voice đã được xóa"}
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                }

        except Exception as e:
            logger.error(f"ElevenLabs delete voice error: {e}")
            return {"success": False, "error": str(e)}
