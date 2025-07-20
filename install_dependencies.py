#!/usr/bin/env python3
"""
Installation script for cosmic civilization game dependencies
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is adequate"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required Python packages"""
    try:
        print("📦 Installing Python dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def verify_pillow():
    """Verify Pillow installation"""
    try:
        from PIL import Image, ImageDraw
        print("✅ Pillow (PIL) is working correctly")
        return True
    except ImportError:
        print("❌ Pillow (PIL) not found")
        return False

def check_godot():
    """Check if Godot is available"""
    try:
        result = subprocess.run(["godot", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Godot found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("⚠️  Godot not found in PATH (you'll need to open the project manually)")
    return False

def main():
    print("🚀 Setting up Cosmic Civilization Game Development Environment")
    print("=" * 60)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Install dependencies
    if not install_dependencies():
        success = False
    
    # Verify Pillow
    if not verify_pillow():
        success = False
    
    # Check Godot (optional)
    check_godot()
    
    print("\n" + "=" * 60)
    
    if success:
        print("🎉 Setup complete!")
        print("\nNext steps:")
        print("1. Generate sprites: python3 sprite_generator.py")
        print("2. Test sprites: python3 test_sprites.py")
        print("3. Open oneiric-parallax/ in Godot 4.4")
        print("4. Run the Main scene to see your cosmic world!")
    else:
        print("❌ Setup incomplete - please fix the issues above")

if __name__ == "__main__":
    main()