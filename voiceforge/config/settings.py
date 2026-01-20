"""Application settings and configuration."""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class ModelConfig:
    """Model configuration settings."""
    backbone_repo: str = "neuphonic/neutts-air"
    codec_repo: str = "neuphonic/neucodec"
    backbone_device: str = "auto"  # auto, cuda, cpu
    codec_device: str = "auto"
    max_context: int = 2048
    sample_rate: int = 24000


@dataclass
class PathConfig:
    """Path configuration settings."""
    project_root: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent)
    samples_dir: Path = field(init=False)
    models_dir: Path = field(init=False)
    temp_dir: Path = field(init=False)
    logs_dir: Path = field(init=False)
    
    def __post_init__(self):
        """Initialize derived paths."""
        self.samples_dir = self.project_root / "samples"
        self.models_dir = self.project_root / "Models"
        self.temp_dir = self.project_root / "temp"
        self.logs_dir = self.project_root / "logs"
        
        # Create directories if they don't exist
        for dir_path in [self.samples_dir, self.models_dir, self.temp_dir, self.logs_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)


@dataclass
class UIConfig:
    """UI configuration settings."""
    title: str = "VoiceForge"
    subtitle: str = "Voice Cloning & Text-to-Speech"
    server_name: str = "0.0.0.0"
    server_port: int = 7860
    share: bool = False
    inbrowser: bool = True
    show_error: bool = True
    theme: str = "soft"  # soft, default, monochrome, glass


@dataclass
class GenerationConfig:
    """Text generation configuration."""
    max_chunk_length: int = 150
    silence_duration: float = 0.25  # seconds between chunks
    min_speed: float = 0.5
    max_speed: float = 2.0
    default_speed: float = 1.0
    speed_step: float = 0.1


@dataclass
class Settings:
    """Main application settings."""
    model: ModelConfig = field(default_factory=ModelConfig)
    paths: PathConfig = field(default_factory=PathConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    generation: GenerationConfig = field(default_factory=GenerationConfig)
    
    def __post_init__(self):
        """Auto-detect device if set to auto."""
        import torch
        
        if self.model.backbone_device == "auto":
            self.model.backbone_device = "cuda" if torch.cuda.is_available() else "cpu"
        
        if self.model.codec_device == "auto":
            self.model.codec_device = "cuda" if torch.cuda.is_available() else "cpu"


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
