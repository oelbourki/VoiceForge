"""Model loading utilities for VoiceForge."""

import os
import torch
from pathlib import Path

from voiceforge.config import get_settings
from voiceforge.utils import get_logger, detect_device
from neuttsair.neutts import NeuTTSAir

logger = get_logger(__name__)


def _resolve_hf_snapshot(root_path: str) -> str:
    """
    Resolve HuggingFace model snapshot path from cache structure.
    
    Args:
        root_path: Root path to check
        
    Returns:
        Resolved model path
    """
    try:
        # Check for HuggingFace cache structure
        if not os.path.isdir(root_path):
            return root_path
            
        for name in os.listdir(root_path):
            if name.startswith("models--"):
                models_dir = os.path.join(root_path, name)
                snapshots_dir = os.path.join(models_dir, "snapshots")
                if os.path.isdir(snapshots_dir):
                    for snap in os.listdir(snapshots_dir):
                        snap_path = os.path.join(snapshots_dir, snap)
                        cfg = os.path.join(snap_path, "config.json")
                        if os.path.exists(cfg):
                            logger.info(f"Found model in snapshots: {snap_path}")
                            return snap_path
    except Exception as e:
        logger.warning(f"Error resolving model path: {e}")
        pass
    return root_path


def load_tts_model() -> NeuTTSAir:
    """
    Load and initialize the TTS model.
    
    Returns:
        Initialized NeuTTSAir model
        
    Raises:
        RuntimeError: If model initialization fails
    """
    settings = get_settings()
    logger.info("Initializing TTS model...")
    
    # Resolve model paths
    local_backbone = settings.paths.models_dir / "neutts-air"
    
    if local_backbone.exists():
        backbone_arg = _resolve_hf_snapshot(str(local_backbone))
    else:
        backbone_arg = settings.model.backbone_repo
        logger.info("Local model not found, will download from HuggingFace")
    
    logger.info(f"Using backbone: {backbone_arg}")
    logger.info(f"Using codec: {settings.model.codec_repo}")
    
    # Detect and set device
    backbone_device = detect_device(settings.model.backbone_device)
    codec_device = detect_device(settings.model.codec_device)
    
    logger.info(f"Using device: {backbone_device} (backbone), {codec_device} (codec)")
    if backbone_device == "cpu":
        logger.warning("CUDA not available, using CPU (slower)")
    
    try:
        tts = NeuTTSAir(
            backbone_repo=backbone_arg,
            backbone_device=backbone_device,
            codec_repo=settings.model.codec_repo,
            codec_device=codec_device,
        )
        logger.info("Model initialized successfully!")
        return tts
    except Exception as e:
        error_msg = f"Error initializing TTS model: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise RuntimeError(error_msg) from e
