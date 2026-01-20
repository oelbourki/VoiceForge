#!/usr/bin/env python3
"""
VoiceForge Test Script
Quick test to verify the application setup and basic functionality.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported."""
    print("=" * 60)
    print("Testing Imports...")
    print("=" * 60)
    
    errors = []
    
    # Test basic Python modules
    try:
        import torch
        print(f"✓ PyTorch: {torch.__version__}")
        if torch.cuda.is_available():
            print(f"  CUDA available: {torch.version.cuda}")
        else:
            print("  CUDA not available (will use CPU)")
    except ImportError as e:
        errors.append(f"✗ PyTorch: {e}")
    
    try:
        import gradio
        print(f"✓ Gradio: {gradio.__version__}")
    except ImportError as e:
        errors.append(f"✗ Gradio: {e}")
    
    try:
        import librosa
        print(f"✓ Librosa: {librosa.__version__}")
    except ImportError as e:
        errors.append(f"✗ Librosa: {e}")
    
    try:
        import numpy
        print(f"✓ NumPy: {numpy.__version__}")
    except ImportError as e:
        errors.append(f"✗ NumPy: {e}")
    
    try:
        from phonemizer.backend import EspeakBackend
        print("✓ Phonemizer")
    except ImportError as e:
        errors.append(f"✗ Phonemizer: {e}")
    
    try:
        from neucodec import NeuCodec
        print("✓ NeuCodec")
    except ImportError as e:
        errors.append(f"✗ NeuCodec: {e}")
    
    try:
        import perth
        print("✓ Perth (watermarker)")
    except ImportError as e:
        errors.append(f"✗ Perth: {e}")
    
    # Test VoiceForge modules
    print("\nTesting VoiceForge modules...")
    try:
        from voiceforge.config import get_settings
        print("✓ VoiceForge config")
    except ImportError as e:
        errors.append(f"✗ VoiceForge config: {e}")
    
    try:
        from voiceforge.utils import check_espeak_installed
        print("✓ VoiceForge utils")
    except ImportError as e:
        errors.append(f"✗ VoiceForge utils: {e}")
    
    try:
        from neuttsair import NeuTTSAir
        print("✓ NeuTTS Air")
    except ImportError as e:
        errors.append(f"✗ NeuTTS Air: {e}")
    
    if errors:
        print("\n" + "=" * 60)
        print("IMPORT ERRORS FOUND:")
        print("=" * 60)
        for error in errors:
            print(f"  {error}")
        return False
    
    print("\n✓ All imports successful!")
    return True


def test_system_checks():
    """Test system requirements."""
    print("\n" + "=" * 60)
    print("Testing System Requirements...")
    print("=" * 60)
    
    try:
        from voiceforge.utils import check_espeak_installed
        if check_espeak_installed():
            print("✓ eSpeak-ng is installed")
        else:
            print("✗ eSpeak-ng not found!")
            print("  Install with: sudo apt install espeak-ng")
            return False
    except Exception as e:
        print(f"✗ Error checking eSpeak: {e}")
        return False
    
    return True


def test_configuration():
    """Test configuration loading."""
    print("\n" + "=" * 60)
    print("Testing Configuration...")
    print("=" * 60)
    
    try:
        from voiceforge.config import get_settings
        settings = get_settings()
        print(f"✓ Configuration loaded")
        print(f"  Sample rate: {settings.model.sample_rate}")
        print(f"  Backbone device: {settings.model.backbone_device}")
        print(f"  Codec device: {settings.model.codec_device}")
        print(f"  Server port: {settings.ui.server_port}")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False


def test_voice_service():
    """Test voice service initialization."""
    print("\n" + "=" * 60)
    print("Testing Voice Service...")
    print("=" * 60)
    
    try:
        from voiceforge.services import VoiceService
        voice_service = VoiceService()
        voices = voice_service.get_voices()
        print(f"✓ Voice service initialized")
        print(f"  Found {len(voices)} voice(s)")
        if voices:
            print(f"  Voices: {', '.join(voices[:5])}")
            if len(voices) > 5:
                print(f"  ... and {len(voices) - 5} more")
        return True
    except ImportError as e:
        print(f"✗ Voice service error: Missing dependencies")
        print(f"  Run: source .venv/bin/activate && pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"✗ Voice service error: {e}")
        return False


def test_directory_structure():
    """Test directory structure."""
    print("\n" + "=" * 60)
    print("Testing Directory Structure...")
    print("=" * 60)
    
    project_root = Path(__file__).parent
    required_dirs = [
        "voiceforge",
        "neuttsair",
        "samples",
    ]
    
    all_ok = True
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"✓ {dir_name}/ exists")
        else:
            print(f"✗ {dir_name}/ not found")
            all_ok = False
    
    # Check for optional directories
    optional_dirs = ["Models", "temp", "logs"]
    for dir_name in optional_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"✓ {dir_name}/ exists")
        else:
            print(f"  {dir_name}/ will be created automatically")
    
    return all_ok


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("VoiceForge Application Test")
    print("=" * 60)
    print()
    
    results = []
    
    # Test directory structure
    results.append(("Directory Structure", test_directory_structure()))
    
    # Test imports
    results.append(("Imports", test_imports()))
    
    # Test system requirements
    results.append(("System Requirements", test_system_checks()))
    
    # Test configuration
    results.append(("Configuration", test_configuration()))
    
    # Test voice service
    results.append(("Voice Service", test_voice_service()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All tests passed! Application is ready to run.")
        print("\nTo start the application:")
        print("  ./run_neutts.sh")
        print("  or")
        print("  source .venv/bin/activate && python main.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\nTo set up the environment:")
        print("  ./setup_linux.sh")
        return 1


if __name__ == "__main__":
    sys.exit(main())
