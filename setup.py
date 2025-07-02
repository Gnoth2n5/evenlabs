#!/usr/bin/env python3
"""
Setup script for Speak - Text-to-Speech Web App
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def create_env_file():
    """Create .env file from template"""
    if not os.path.exists(".env"):
        print("📝 Creating .env file...")
        try:
            with open("env.example", "r") as f:
                content = f.read()

            with open(".env", "w") as f:
                f.write(content)

            print("✅ .env file created successfully")
            print("⚠️  Please update .env file with your ElevenLabs API key")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
        return True


def main():
    """Main setup function"""
    print("🚀 Setting up Speak - Text-to-Speech Web App")
    print("=" * 50)

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)

    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

    # Create virtual environment
    if not os.path.exists("venv"):
        if not run_command("python -m venv venv", "Creating virtual environment"):
            sys.exit(1)
    else:
        print("✅ Virtual environment already exists")

    # Activate virtual environment and install dependencies
    if os.name == "nt":  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"

    # Install dependencies
    if not run_command(
        f"{pip_cmd} install -r requirements.txt", "Installing dependencies"
    ):
        sys.exit(1)

    # Create .env file
    if not create_env_file():
        sys.exit(1)

    # Create necessary directories
    directories = [
        "app/static/audio",
        "app/static/uploads",
        "app/templates/tts",
    ]

    print("📁 Creating directories...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✅ Directories created successfully")

    # Initialize database
    if not run_command(f"{activate_cmd} && flask init-db", "Initializing database"):
        print("⚠️  Database initialization failed, but you can continue")

    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update .env file with your ElevenLabs API key")
    print("2. Activate virtual environment:")
    if os.name == "nt":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("3. Run the application:")
    print("   python run.py")
    print("4. Open http://localhost:5000 in your browser")
    print("\n📚 For more information, see README.md")


if __name__ == "__main__":
    main()
