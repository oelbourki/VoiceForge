"""Text-to-Speech service for VoiceForge."""

import time
import numpy as np
import torch
import soundfile as sf
from pathlib import Path
from typing import Generator, Tuple, Optional, Union

from voiceforge.config import get_settings
from voiceforge.utils import get_logger, split_text_into_chunks, format_time
from neuttsair.neutts import NeuTTSAir

logger = get_logger(__name__)


class TTSService:
    """Service for text-to-speech generation."""
    
    def __init__(self, tts_model: NeuTTSAir):
        """
        Initialize TTS service.
        
        Args:
            tts_model: Initialized NeuTTSAir model
        """
        self.tts = tts_model
        self.settings = get_settings()
        logger.info("TTS Service initialized")
    
    def generate_speech(
        self,
        text: str,
        ref_codes: Union[np.ndarray, torch.Tensor],
        ref_text: str,
        speed: float = 1.0,
    ) -> Generator[Tuple[int, Optional[str], str, Optional[str]], None, None]:
        """
        Generate speech from text using the selected voice.
        Uses generator pattern for progress updates.
        
        Args:
            text: Input text to convert to speech
            ref_codes: Encoded reference voice codes
            ref_text: Reference text for the voice
            speed: Speech speed multiplier (0.5 to 2.0)
            
        Yields:
            Tuple of (progress, audio_path, status_message, error)
        """
        try:
            start_time = time.time()
            
            # Input validations
            if not text or not text.strip():
                yield 0, None, "❌ Error: Input text cannot be empty.", None
                return

            if ref_codes is None:
                yield 0, None, "❌ Error: No voice reference provided.", None
                return
            
            # Load reference
            yield 10, None, "📥 Loading voice reference...", None
            
            # Split text into smaller chunks for better processing
            chunks = split_text_into_chunks(text, self.settings.generation.max_chunk_length)
            total_chunks = len(chunks)
            
            if total_chunks == 0:
                raise ValueError("No text to process")
            
            # Estimate total time
            estimated_time = self._estimate_generation_time(total_chunks)
            status = f"⏱️  Estimated time: {format_time(estimated_time)}\n📊 Processing {total_chunks} chunks..."
            yield 15, None, status, None
                
            # Process each chunk and store with its index
            chunk_results = []
            for i, chunk in enumerate(chunks, 1):
                chunk_start = time.time()
                
                # Update progress
                progress = int(15 + (75 * i / total_chunks))
                
                # Calculate and show time statistics
                elapsed_time = time.time() - start_time
                if i > 1:
                    avg_time_per_chunk = elapsed_time / (i - 1)
                    remaining_chunks = total_chunks - (i - 1)
                    estimated_remaining = avg_time_per_chunk * remaining_chunks
                    status = (
                        f"🔄 Processing chunk {i}/{total_chunks}\n"
                        f"📈 Progress: {progress}% complete\n"
                        f"⏱️  Est. remaining: {format_time(estimated_remaining)}"
                    )
                else:
                    status = f"🔄 Processing chunk {i}/{total_chunks}\n📈 Progress: {progress}% complete"
                
                yield progress, None, status, None
                
                # Generate audio for this chunk
                try:
                    chunk_wav = self.tts.infer(chunk, ref_codes, ref_text)
                    if chunk_wav is not None:
                        chunk_results.append((i-1, chunk_wav))
                except Exception as e:
                    logger.warning(f"Error processing chunk {i}: {e}")
                    # Continue with other chunks

            if not chunk_results:
                raise ValueError("Failed to generate any audio")

            # Update status for final processing
            yield 90, None, "🔧 Finalizing audio...\n📦 Ordering and combining chunks...", None

            # Sort chunks by their original index and extract the audio data
            chunk_results.sort(key=lambda x: x[0])
            processed_chunks = [chunk[1] for chunk in chunk_results]

            # Create silence once
            silence_duration = self.settings.generation.silence_duration
            silence = np.zeros(int(self.settings.model.sample_rate * silence_duration))

            # Concatenate all chunks with silence in between
            all_wav = processed_chunks[0]
            for chunk_wav in processed_chunks[1:]:
                all_wav = np.concatenate([all_wav, silence, chunk_wav])

            # Apply speed adjustment if needed
            if speed != 1.0:
                target_length = int(len(all_wav) / speed)
                indices = np.round(np.linspace(0, len(all_wav) - 1, target_length)).astype(int)
                all_wav = all_wav[indices]

            # Save the final audio
            temp_path = self.settings.paths.temp_dir / "output.wav"
            sf.write(str(temp_path), all_wav, self.settings.model.sample_rate)
            
            # Calculate and show total time taken
            total_time = time.time() - start_time
            final_status = f"✅ Generation complete!\n⏱️  Total time: {format_time(total_time)}"
            
            yield 100, str(temp_path), final_status, None
            
        except Exception as e:
            error_msg = f"❌ Error generating speech: {str(e)}"
            logger.error(error_msg, exc_info=True)
            yield 0, None, error_msg, str(e)
    
    def _estimate_generation_time(self, num_chunks: int) -> float:
        """Estimate the generation time based on number of chunks."""
        # Assuming average of 3 seconds per chunk plus overhead
        return num_chunks * 3 + 2
