"""System utilities for VoiceForge."""

import os
import shutil
import torch
from typing import Literal


def check_espeak_installed() -> bool:
    """
    Check if eSpeak-ng is installed and accessible.
    
    Returns:
        True if espeak is found, False otherwise
    """
    # First, check if espeak-ng or espeak is in PATH
    espeak_path = shutil.which('espeak-ng') or shutil.which('espeak')
    
    if espeak_path:
        return True
    
    # Check common Linux installation paths
    linux_paths = [
        '/usr/bin/espeak-ng',
        '/usr/local/bin/espeak-ng',
        '/usr/bin/espeak',
        '/usr/local/bin/espeak',
        '/opt/homebrew/bin/espeak-ng',  # macOS Homebrew
    ]
    
    for path in linux_paths:
        if os.path.exists(path):
            return True
    
    # Check for shared library (Linux .so files)
    so_paths = [
        '/usr/lib/libespeak-ng.so',
        '/usr/lib/libespeak-ng.so.1',
        '/usr/local/lib/libespeak-ng.so',
        '/usr/lib/x86_64-linux-gnu/libespeak-ng.so',
        '/usr/lib/x86_64-linux-gnu/libespeak-ng.so.1',
        '/usr/lib64/libespeak-ng.so',
        '/opt/homebrew/lib/libespeak-ng.so',  # macOS Homebrew
    ]
    
    for so_path in so_paths:
        if os.path.exists(so_path):
            os.environ['PHONEMIZER_ESPEAK_LIBRARY'] = so_path
            return True
    
    return False


def detect_device(preferred: Literal["auto", "cuda", "cpu"] = "auto") -> str:
    """
    Detect and return the appropriate device for model inference.
    
    Args:
        preferred: Preferred device type
        
    Returns:
        Device string ("cuda" or "cpu")
    """
    if preferred == "cuda":
        if torch.cuda.is_available():
            return "cuda"
        return "cpu"
    elif preferred == "cpu":
        return "cpu"
    else:  # auto
        return "cuda" if torch.cuda.is_available() else "cpu"
