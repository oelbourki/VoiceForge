#!/usr/bin/env python3
"""
VoiceForge - Professional Voice Cloning Application
Main entry point for the application.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from voiceforge.config import get_settings
from voiceforge.utils import setup_logger, check_espeak_installed
from voiceforge.models import load_tts_model
from voiceforge.services import TTSService, VoiceService
from voiceforge.ui import create_app


def main():
    """Main application entry point."""
    settings = get_settings()
    
    # Setup logging
    logger = setup_logger(
        name="voiceforge",
        log_dir=settings.paths.logs_dir,
        level=20,  # INFO level
        console=True
    )
    
    logger.info("=" * 60)
    logger.info("🚀 Starting VoiceForge")
    logger.info("=" * 60)
    
    # Check eSpeak installation
    logger.info("Checking eSpeak installation...")
    if not check_espeak_installed():
        logger.error("✗ Error: espeak-ng not found!")
        logger.error("\nInstallation instructions:")
        logger.error("  Ubuntu/Debian: sudo apt install espeak-ng espeak-data libespeak1 libespeak-dev")
        logger.error("  Arch Linux:   sudo pacman -S espeak-ng")
        logger.error("  Fedora:       sudo dnf install espeak-ng")
        logger.error("  macOS:        brew install espeak-ng")
        sys.exit(1)
    logger.info("✓ eSpeak found")
    
    # Load TTS model
    try:
        tts_model = load_tts_model()
    except RuntimeError as e:
        logger.error(f"Failed to initialize TTS model: {e}")
        logger.error("\nTroubleshooting:")
        logger.error("  1. Check internet connection (first run downloads models)")
        logger.error("  2. Verify CUDA installation if using GPU")
        logger.error("  3. Check disk space (models are ~2-4 GB)")
        sys.exit(1)
    
    # Initialize services
    logger.info("Initializing services...")
    tts_service = TTSService(tts_model)
    voice_service = VoiceService()
    
    # Create and launch app
    logger.info("Creating UI...")
    app = create_app(tts_service, voice_service)
    
    logger.info("=" * 60)
    logger.info(f"🌐 Web interface will open at: http://localhost:{settings.ui.server_port}")
    logger.info("=" * 60)
    logger.info("")
    
    app.launch(
        server_name=settings.ui.server_name,
        server_port=settings.ui.server_port,
        share=settings.ui.share,
        inbrowser=settings.ui.inbrowser,
        show_error=settings.ui.show_error,
    )


if __name__ == "__main__":
    main()
