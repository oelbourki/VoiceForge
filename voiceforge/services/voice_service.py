"""Voice management service for VoiceForge."""

import os
import shutil
import torch
from pathlib import Path
from typing import Dict, Tuple, List, Optional

from voiceforge.config import get_settings
from voiceforge.utils import get_logger

logger = get_logger(__name__)


class VoiceService:
    """Service for managing voice clones."""
    
    def __init__(self):
        """Initialize voice service."""
        self.settings = get_settings()
        self.voices: Dict[str, Tuple[Path, Path]] = {}
        self._load_voices()
        logger.info(f"Voice Service initialized with {len(self.voices)} voices")
    
    def _load_voices(self) -> None:
        """Load all voices from the samples directory."""
        self.voices = {}
        voice_dir = self.settings.paths.samples_dir
        
        if not voice_dir.exists():
            voice_dir.mkdir(parents=True, exist_ok=True)
            return
        
        for name in os.listdir(voice_dir):
            if name.endswith(".txt"):
                base = os.path.splitext(name)[0]
                txt_path = voice_dir / f"{base}.txt"
                wav_path = voice_dir / f"{base}.wav"
                pt_path = voice_dir / f"{base}.pt"

                if txt_path.exists() and (wav_path.exists() or pt_path.exists()):
                    self.voices[base] = (
                        txt_path,
                        pt_path if pt_path.exists() else wav_path
                    )
        
        logger.info(f"Loaded {len(self.voices)} voice(s): {list(self.voices.keys())}")
    
    def get_voices(self) -> List[str]:
        """
        Get list of available voice names.
        
        Returns:
            Sorted list of voice names
        """
        return sorted(list(self.voices.keys()))
    
    def voice_exists(self, voice_name: str) -> bool:
        """
        Check if a voice exists.
        
        Args:
            voice_name: Name of the voice
            
        Returns:
            True if voice exists
        """
        return voice_name in self.voices
    
    def load_reference(self, voice_name: str, tts_model=None) -> Tuple[str, torch.Tensor]:
        """
        Load reference text and encoded codes for a voice.
        
        Args:
            voice_name: Name of the voice
            tts_model: Optional TTS model for encoding WAV files
            
        Returns:
            Tuple of (reference_text, reference_codes)
            
        Raises:
            ValueError: If voice not found or encoding fails
        """
        if voice_name not in self.voices:
            raise ValueError(f"Voice '{voice_name}' not found")
        
        txt_path, audio_or_pt = self.voices[voice_name]
        ref_text = txt_path.read_text(encoding='utf-8').strip()

        if str(audio_or_pt).endswith(".pt"):
            ref_codes = torch.load(audio_or_pt, map_location='cpu')
        else:
            # Need to encode from WAV
            if tts_model is None:
                raise ValueError("TTS model required to encode WAV file")
            ref_codes = tts_model.encode_reference(str(audio_or_pt))
        
        return ref_text, ref_codes
    
    def clone_voice(
        self,
        voice_name: str,
        ref_text: str,
        audio_file_path: str,
        tts_model
    ) -> str:
        """
        Clone a new voice from reference audio.
        
        Args:
            voice_name: Name for the new voice
            ref_text: Reference text (exact text spoken in audio)
            audio_file_path: Path to reference audio file
            tts_model: TTS model for encoding
            
        Returns:
            Success message
            
        Raises:
            ValueError: If validation fails
        """
        # Input validations
        if not voice_name or not voice_name.strip():
            raise ValueError("Voice name cannot be empty")
        
        if not ref_text or not ref_text.strip():
            raise ValueError("Reference text cannot be empty")
            
        if not audio_file_path or not os.path.exists(audio_file_path):
            raise ValueError("Reference audio file not found")
            
        if voice_name in self.voices:
            raise ValueError(f"Voice '{voice_name}' already exists")
        
        # Prepare paths
        samples_dir = self.settings.paths.samples_dir
        txt_path = samples_dir / f"{voice_name}.txt"
        wav_path = samples_dir / f"{voice_name}.wav"
        pt_path = samples_dir / f"{voice_name}.pt"

        # Save reference text and audio
        txt_path.write_text(ref_text.strip(), encoding='utf-8')
        shutil.copy(audio_file_path, wav_path)

        # Encode voice
        logger.info(f"Encoding voice '{voice_name}'...")
        ref_codes = tts_model.encode_reference(str(wav_path))
        torch.save(ref_codes, pt_path)

        # Update voices dictionary
        self.voices[voice_name] = (txt_path, pt_path)
        
        logger.info(f"Voice '{voice_name}' cloned successfully")
        return f"✅ Voice '{voice_name}' cloned and saved successfully!"
    
    def delete_voice(self, voice_name: str) -> None:
        """
        Delete a voice and its associated files.
        
        Args:
            voice_name: Name of the voice to delete
            
        Raises:
            ValueError: If voice not found
        """
        if voice_name not in self.voices:
            raise ValueError(f"Voice '{voice_name}' not found")

        samples_dir = self.settings.paths.samples_dir
        txt_path = samples_dir / f"{voice_name}.txt"
        wav_path = samples_dir / f"{voice_name}.wav"
        pt_path = samples_dir / f"{voice_name}.pt"

        # Remove files if they exist
        for path in [txt_path, wav_path, pt_path]:
            if path.exists():
                path.unlink()

        # Remove from voices dictionary
        del self.voices[voice_name]
        
        logger.info(f"Voice '{voice_name}' deleted")
    
    def reload(self) -> List[str]:
        """
        Reload voices from the samples directory.
        
        Returns:
            Updated list of voice names
        """
        self._load_voices()
        return self.get_voices()
