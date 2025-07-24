#!/usr/bin/env python3
"""
Quick setup script for Zoobae LLM Chat System
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_path = Path(".env")
    
    if env_path.exists():
        print("✅ .env file already exists")
        return
    
    env_content = """# Google AI Studio API Configuration (FREE!)
# Get your API key from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_google_ai_studio_api_key_here

# MongoDB Configuration (optional, defaults to localhost)
MONGO_URL=mongodb://localhost:27017/

# Server Configuration
HOST=0.0.0.0
PORT=8001
"""
    
    with open(env_path, "w") as f:
        f.write(env_content)
    
    print("✅ Created .env file")
    print("📝 Please edit .env and add your Google AI Studio API key")

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "pymongo",
        "python-multipart",
        "python-jose",
        "passlib",
        "bcrypt",
        "python-dotenv"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages are installed")
        return True

def check_llm_dependencies():
    """Check if LLM packages are installed"""
    llm_packages = [
        "google.generativeai",
        "langchain_google_genai"
    ]
    
    missing_llm_packages = []
    
    for package in llm_packages:
        try:
            __import__(package)
        except ImportError:
            missing_llm_packages.append(package)
    
    if missing_llm_packages:
        print(f"⚠️  LLM packages not installed: {', '.join(missing_llm_packages)}")
        print("📦 Run: pip install -r requirements.txt")
        print("ℹ️  The system will use simple fallback responses")
        return False
    else:
        print("✅ LLM packages are installed")
        return True

def main():
    print("🚀 Zoobae LLM Chat System Setup")
    print("=" * 40)
    
    # Create .env file
    create_env_file()
    
    # Check dependencies
    deps_ok = check_dependencies()
    llm_ok = check_llm_dependencies()
    
    print("\n📋 Next Steps:")
    print("1. Get a FREE Google AI Studio API key:")
    print("   https://makersuite.google.com/app/apikey")
    print("2. Add your API key to the .env file")
    print("3. Start the server:")
    print("   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001")
    
    if not deps_ok:
        print("\n❌ Please install missing dependencies first")
        sys.exit(1)
    
    if not llm_ok:
        print("\n⚠️  LLM features will use simple fallback responses")
        print("   Install LLM packages for full AI capabilities")
    
    print("\n✅ Setup complete! You can now start the server.")

if __name__ == "__main__":
    main() 