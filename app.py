#!/usr/bin/env python3
"""
NeuTTS Air - Linux-Compatible Voice Cloning Application
A Gradio-based web interface for instant voice cloning and speech generation.
"""

import os
import sys
import torch
import numpy as np
import soundfile as sf
import shutil
from pathlib import Path
from neuttsair.neutts import NeuTTSAir
import gradio as gr

# ---------------------------
# eSpeak check (Linux-compatible)
# ---------------------------
def check_espeak_installed():
    """
    Check if eSpeak-ng is installed and accessible on Linux.
    Returns True if found, False otherwise.
    """
    # First, check if espeak-ng or espeak is in PATH
    espeak_path = shutil.which('espeak-ng') or shutil.which('espeak')
    
    if espeak_path:
        print(f"✓ Found espeak at: {espeak_path}")
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
            print(f"✓ Found espeak at: {path}")
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
            print(f"✓ Found espeak library at: {so_path}")
            return True
    
    # If not found, provide helpful error message
    print("\n✗ Error: espeak-ng not found!")
    print("\nInstallation instructions:")
    print("  Ubuntu/Debian: sudo apt install espeak-ng espeak-data libespeak1 libespeak-dev")
    print("  Arch Linux:   sudo pacman -S espeak-ng")
    print("  Fedora:       sudo dnf install espeak-ng")
    print("  macOS:        brew install espeak-ng")
    print("\nOr build from source:")
    print("  https://github.com/espeak-ng/espeak-ng")
    return False


if not check_espeak_installed():
    sys.exit(1)

# ---------------------------
# Model initialization
# ---------------------------
print("\n🚀 Initializing TTS model...")
try:
    project_root = os.path.abspath(os.path.dirname(__file__))
    local_backbone = os.path.join(project_root, "Models", "neutts-air")

    def _resolve_hf_snapshot(root_path: str) -> str:
        """
        Resolve HuggingFace model snapshot path from cache structure.
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
                                print(f"✓ Found model in snapshots: {snap_path}")
                                return snap_path
        except Exception as e:
            print(f"⚠ Warning: Error resolving model path: {e}")
            pass
        return root_path

    # Check if local model exists, otherwise use remote
    if os.path.isdir(local_backbone):
        backbone_arg = _resolve_hf_snapshot(local_backbone)
    else:
        # Use remote model (will download on first run)
        backbone_arg = "neuphonic/neutts-air"
        print("⚠ Local model not found, will download from HuggingFace")

    print(f"📦 Using backbone: {backbone_arg}")
    print(f"📦 Using codec: neuphonic/neucodec")
    
    # Detect CUDA availability
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🖥️  Using device: {device}")
    if device == "cpu":
        print("⚠ Warning: CUDA not available, using CPU (slower)")

    tts = NeuTTSAir(
        backbone_repo=backbone_arg,
        backbone_device=device,
        codec_repo="neuphonic/neucodec",
        codec_device=device,
    )
    print("✅ Model initialized successfully!")
except Exception as e:
    print(f"\n✗ Error initializing TTS model: {str(e)}")
    print("\nTroubleshooting:")
    print("  1. Check internet connection (first run downloads models)")
    print("  2. Verify CUDA installation if using GPU")
    print("  3. Check disk space (models are ~2-4 GB)")
    sys.exit(1)

# ---------------------------
# Voice loading logic
# ---------------------------
VOICES = {"samples": {}}
voice_dir = "samples"
os.makedirs(voice_dir, exist_ok=True)

# Load voices from samples directory
for name in os.listdir(voice_dir):
    if name.endswith(".txt"):
        base = os.path.splitext(name)[0]
        txt_path = os.path.join(voice_dir, f"{base}.txt")
        wav_path = os.path.join(voice_dir, f"{base}.wav")
        pt_path = os.path.join(voice_dir, f"{base}.pt")

        if os.path.exists(txt_path) and (os.path.exists(wav_path) or os.path.exists(pt_path)):
            VOICES["samples"][base] = (txt_path, wav_path if os.path.exists(wav_path) else pt_path)

# Print loaded voices for debugging
if VOICES["samples"]:
    print(f"\n✅ Loaded {len(VOICES['samples'])} voice(s):")
    for voice_name in VOICES["samples"].keys():
        print(f"   - {voice_name}")
else:
    print("\n⚠ No voices found in samples directory")
    print("   Add voice files (.txt + .wav/.pt) to the 'samples' folder")

def format_voice_choice(name):
    return f"Voice: {name}"

def reload_voices():
    """Reload voices from samples directory and return updated choices."""
    global VOICES
    VOICES["samples"] = {}
    voice_dir = "samples"
    
    if not os.path.exists(voice_dir):
        os.makedirs(voice_dir, exist_ok=True)
        return []
    
    for name in os.listdir(voice_dir):
        if name.endswith(".txt"):
            base = os.path.splitext(name)[0]
            txt_path = os.path.join(voice_dir, f"{base}.txt")
            wav_path = os.path.join(voice_dir, f"{base}.wav")
            pt_path = os.path.join(voice_dir, f"{base}.pt")

            if os.path.exists(txt_path) and (os.path.exists(wav_path) or os.path.exists(pt_path)):
                VOICES["samples"][base] = (txt_path, wav_path if os.path.exists(wav_path) else pt_path)
    
    return sorted(list(VOICES["samples"].keys()))

# ---------------------------
# Core functions
# ---------------------------
def load_reference(voice_name):
    """Load reference text and encoded codes for a voice."""
    txt_path, audio_or_pt = VOICES["samples"][voice_name]
    ref_text = open(txt_path, "r", encoding='utf-8').read().strip()

    if audio_or_pt.endswith(".pt"):
        ref_codes = torch.load(audio_or_pt, map_location='cpu')
    else:
        ref_codes = tts.encode_reference(audio_or_pt)
    return ref_text, ref_codes


def split_text_into_chunks(text, max_length=150):
    """
    Split text into smaller chunks preserving sentence and punctuation structure.
    """
    import re
    
    # Clean up the text first
    text = text.strip()
    if not text:
        return []

    # Split by sentence-ending punctuation while preserving the punctuation
    sentence_pattern = r'([.!?]+)'
    parts = re.split(sentence_pattern, text)

    # Reconstruct sentences with their punctuation
    sentences = []
    i = 0
    while i < len(parts):
        if parts[i].strip():
            sentence = parts[i].strip()
            # Add punctuation if it exists
            if i + 1 < len(parts) and parts[i + 1].strip():
                sentence += parts[i + 1]
                i += 2
            else:
                # If no punctuation follows, add a period (only once)
                if not sentence.endswith(('.', '!', '?')):
                    sentence += '.'
                i += 1
            sentences.append(sentence)
        else:
            i += 1

    # Handle last part if not already included
    if len(parts) > 0 and parts[-1].strip():
        last_part = parts[-1].strip()
        if not any(last_part in s or s.startswith(last_part) for s in sentences):
            if not last_part.endswith(('.', '!', '?')):
                last_part += '.'
            sentences.append(last_part)

    # Group sentences into chunks
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # If single sentence exceeds max_length, split by commas
        if len(sentence) > max_length:
            comma_parts = re.split(r'(,)', sentence)
            temp_sentence = ""
            
            i = 0
            while i < len(comma_parts):
                part = comma_parts[i].strip()
                comma = comma_parts[i + 1] if i + 1 < len(comma_parts) else ''
                
                # If part is still too long, split by words
                if len(part) > max_length:
                    words = part.split()
                    temp_words = []
                    
                    for word in words:
                        test_chunk = ' '.join(temp_words + [word])
                        if len(test_chunk) > max_length and temp_words:
                            if current_chunk:
                                chunks.append(current_chunk.strip())
                                current_chunk = ""
                            chunks.append(' '.join(temp_words))
                            temp_words = [word]
                        else:
                            temp_words.append(word)
                    
                    if temp_words:
                        part = ' '.join(temp_words) + comma
                        if current_chunk and len(current_chunk + ' ' + part) > max_length:
                            chunks.append(current_chunk.strip())
                            current_chunk = part
                        else:
                            current_chunk += (' ' if current_chunk else '') + part
                else:
                    part_with_comma = part + comma
                    if current_chunk and len(current_chunk + ' ' + part_with_comma) > max_length:
                        chunks.append(current_chunk.strip())
                        current_chunk = part_with_comma
                    else:
                        current_chunk += (' ' if current_chunk else '') + part_with_comma
                
                i += 2 if i + 1 < len(comma_parts) else 1
        else:
            # Normal sentence that fits within limit
            if current_chunk and len(current_chunk + ' ' + sentence) > max_length:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += (' ' if current_chunk else '') + sentence

    # Always add remaining chunk at the end
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # Filter out empty or duplicate chunks
    final_chunks = []
    for chunk in chunks:
        if chunk.strip() and (not final_chunks or chunk.strip() != final_chunks[-1]):
            final_chunks.append(chunk.strip())

    return final_chunks


def process_chunk(chunk, ref_codes, ref_text, tts_model):
    """Process a single chunk of text and return the audio."""
    try:
        return tts_model.infer(chunk, ref_codes, ref_text)
    except Exception as e:
        # Swallow individual chunk errors and return None to let caller handle it
        print(f"⚠ Error processing chunk: {e}")
        return None

def estimate_generation_time(num_chunks):
    """Estimate the generation time based on number of chunks."""
    # Assuming average of 3 seconds per chunk plus overhead
    return num_chunks * 3 + 2

def format_time(seconds):
    """Format seconds into a readable time string."""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes} minute{'s' if minutes != 1 else ''} {seconds:.1f} seconds"

def generate_speech(text, voice_name, speed=1.0):
    """
    Generate speech from text using the selected voice.
    Uses generator pattern for progress updates.
    """
    try:
        import time

        # Input validations
        if not text or not text.strip():
            yield 0, None, "❌ Error: Input text cannot be empty.", None
            return

        if not voice_name:
            yield 0, None, "❌ Error: No voice selected. Please select a voice.", None
            return

        if voice_name not in VOICES["samples"]:
            yield 0, None, f"❌ Error: Voice '{voice_name}' not found.", None
            return
        
        start_time = time.time()
        
        # Load reference only once
        yield 10, None, "📥 Loading voice reference...", None
        ref_text, ref_codes = load_reference(voice_name)
        
        # Split text into smaller chunks for better processing
        chunks = split_text_into_chunks(text)
        total_chunks = len(chunks)
        
        if total_chunks == 0:
            raise ValueError("No text to process")
        
        # Estimate total time
        estimated_time = estimate_generation_time(total_chunks)
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
            chunk_wav = process_chunk(chunk, ref_codes, ref_text, tts)
            if chunk_wav is not None:
                # Store chunk with its index to maintain order
                chunk_results.append((i-1, chunk_wav))

        if not chunk_results:
            raise ValueError("Failed to generate any audio")

        # Update status for final processing
        yield 90, None, "🔧 Finalizing audio...\n📦 Ordering and combining chunks...", None

        # Sort chunks by their original index and extract the audio data
        chunk_results.sort(key=lambda x: x[0])  # Sort by index
        processed_chunks = [chunk[1] for chunk in chunk_results]  # Extract audio data in order

        # Create silence once
        silence = np.zeros(int(24000 * 0.25))  # 0.25 seconds silence between chunks

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
        temp_path = "temp_output.wav"
        sf.write(temp_path, all_wav, 24000)
        
        # Calculate and show total time taken
        total_time = time.time() - start_time
        final_status = f"✅ Generation complete!\n⏱️  Total time: {format_time(total_time)}"
        
        yield 100, temp_path, final_status, None
    except Exception as e:
        error_status = f"❌ Error generating speech: {str(e)}"
        yield 0, None, error_status, None


def delete_voice(voice_name):
    """Deletes a voice and its associated files."""
    try:
        if voice_name not in VOICES["samples"]:
            return f"❌ Voice '{voice_name}' not found!", gr.update()

        txt_path = f"samples/{voice_name}.txt"
        wav_path = f"samples/{voice_name}.wav"
        pt_path = f"samples/{voice_name}.pt"

        # Remove files if they exist
        for path in [txt_path, wav_path, pt_path]:
            if os.path.exists(path):
                os.remove(path)

        # Remove from VOICES dictionary
        del VOICES["samples"][voice_name]
        
        remaining_voices = list(VOICES["samples"].keys())
        new_selected = remaining_voices[0] if remaining_voices else None
        
        return f"✅ Voice '{voice_name}' deleted successfully!", gr.update(choices=remaining_voices, value=new_selected)
    except Exception as e:
        return f"❌ Error deleting voice: {e}", gr.update()

def clone_voice(new_name, txt, audio_file):
    """Encodes a new reference voice and saves its embedding."""
    try:
        # Input validations
        if not new_name or not new_name.strip():
            return "❌ Error: New Voice name cannot be empty.", gr.update()
        
        if not txt or not txt.strip():
            return "❌ Error: Reference text cannot be empty.", gr.update()
            
        if not audio_file:
            return "❌ Error: No reference audio file provided.", gr.update()
            
        if new_name in VOICES["samples"]:
            return f"❌ Error: Voice '{new_name}' already exists. Please choose a different name.", gr.update()
            
        os.makedirs("samples", exist_ok=True)
        txt_path = f"samples/{new_name}.txt"
        wav_path = f"samples/{new_name}.wav"
        pt_path = f"samples/{new_name}.pt"

        # Save reference text and audio
        with open(txt_path, "w", encoding='utf-8') as f:
            f.write(txt.strip())
        shutil.copy(audio_file, wav_path)

        print(f"🔄 Encoding voice '{new_name}'...")
        ref_codes = tts.encode_reference(wav_path)
        torch.save(ref_codes, pt_path)

        VOICES["samples"][new_name] = (txt_path, pt_path)
        return f"✅ Voice '{new_name}' cloned and saved successfully!", gr.update(choices=list(VOICES["samples"].keys()), value=new_name)
    except Exception as e:
        return f"❌ Error cloning voice: {e}", gr.update()


# ---------------------------
# UI
# ---------------------------
with gr.Blocks(title="NeuTTS Voice Cloning - Linux") as app:
    gr.HTML("""<h1 style="font-size: 2.5em; margin-bottom: 0.5rem;text-align:center;">🎙️ NeuTTS Voice Cloning</h1><p style='text-align:center;'>Generate or clone voices in seconds - Linux Edition</p>""")

    with gr.Tab("Generate Speech"):
        with gr.Row():
            with gr.Column():
                text_input = gr.Textbox(label="Input Text", lines=4, placeholder="Enter the text you want to convert to speech...")
                with gr.Row():
                    # Sort voices alphabetically for better UX
                    voice_choices = sorted(list(VOICES["samples"].keys()))
                    voice_select = gr.Dropdown(
                        label=f"Select Voice ({len(voice_choices)} available)",
                        choices=voice_choices,
                        value=voice_choices[0] if voice_choices else None,
                        interactive=True,
                        allow_custom_value=False
                    )
                    reload_btn = gr.Button("🔄 Reload", variant="secondary", size="sm")
                    delete_btn = gr.Button("🗑️ Delete Voice", variant="secondary", size="sm")
                speed_slider = gr.Slider(label="Speed", minimum=0.5, maximum=2.0, value=1.0, step=0.1)
                generate_btn = gr.Button("🎙️ Generate Speech", variant="primary")
            with gr.Column():
                progress_bar = gr.Slider(label="Progress", minimum=0, maximum=100, value=0, interactive=False)
                status_box = gr.Textbox(label="Generation Status", value="", lines=3, interactive=False)
                delete_status = gr.Textbox(label="Status", visible=False)
                audio_output = gr.Audio(label="Output", autoplay=True)

        generate_btn.click(
            fn=generate_speech,
            inputs=[text_input, voice_select, speed_slider],
            outputs=[progress_bar, audio_output, status_box, delete_status]
        )

        delete_btn.click(
            fn=delete_voice,
            inputs=[voice_select],
            outputs=[delete_status, voice_select]
        )
        
        reload_btn.click(
            fn=lambda: gr.update(choices=reload_voices(), value=reload_voices()[0] if reload_voices() else None),
            outputs=[voice_select]
        )

    with gr.Tab("Instantly Clone New Voice"):
        with gr.Row():
            with gr.Column():
                new_voice_name = gr.Textbox(label="New Voice Name", placeholder="e.g., my_voice")
                ref_text_input = gr.Textbox(label="Reference Text (same text spoken in sample)", lines=3, placeholder="Enter the exact text that is spoken in the reference audio...")
                ref_audio_input = gr.Audio(label="Reference Audio (.wav)", type="filepath")
                clone_btn = gr.Button("🧬 Clone Voice", variant="primary")
            with gr.Column():
                clone_status = gr.Textbox(label="Status", lines=5)

        clone_btn.click(
            fn=clone_voice,
            inputs=[new_voice_name, ref_text_input, ref_audio_input],
            outputs=[clone_status, voice_select]
        )

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 Starting NeuTTS Air - Linux Edition")
    print("="*60)
    print(f"🌐 Web interface will open at: http://localhost:7860")
    print("="*60 + "\n")
    
    app.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,
        share=False,
        inbrowser=True,
        show_error=True,
        theme=gr.themes.Soft()
    )
