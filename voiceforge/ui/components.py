"""UI components for VoiceForge."""

import gradio as gr
from typing import List, Optional

from voiceforge.config import get_settings

settings = get_settings()


def create_header() -> gr.HTML:
    """Create the application header with branding."""
    html_content = """
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 3.5em; margin-bottom: 0.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 700;">
            🎙️ VoiceForge
        </h1>
        <p style="font-size: 1.2em; color: #666; margin-top: 0.5rem;">
            Professional Voice Cloning & Text-to-Speech
        </p>
        <p style="font-size: 0.9em; color: #999; margin-top: 0.5rem;">
            Transform text into natural speech with instant voice cloning
        </p>
    </div>
    """
    return gr.HTML(html_content)


def create_generation_tab(
    voice_choices: List[str],
    voice_service,
    tts_service
) -> gr.Tab:
    """Create the speech generation tab."""
    with gr.Tab("🎤 Generate Speech") as tab:
        with gr.Row():
            with gr.Column(scale=1):
                text_input = gr.Textbox(
                    label="Input Text",
                    lines=6,
                    placeholder="Enter the text you want to convert to speech...",
                    info="Type or paste your text here. Long texts will be automatically split into chunks."
                )
                
                with gr.Row():
                    voice_select = gr.Dropdown(
                        label=f"Select Voice ({len(voice_choices)} available)",
                        choices=voice_choices,
                        value=voice_choices[0] if voice_choices else None,
                        interactive=True,
                        allow_custom_value=False,
                        info="Choose a cloned voice to use for speech generation"
                    )
                    reload_btn = gr.Button("🔄 Reload", variant="secondary", size="sm")
                    delete_btn = gr.Button("🗑️ Delete", variant="secondary", size="sm")
                
                speed_slider = gr.Slider(
                    label="Speech Speed",
                    minimum=settings.generation.min_speed,
                    maximum=settings.generation.max_speed,
                    value=settings.generation.default_speed,
                    step=settings.generation.speed_step,
                    info="Adjust the playback speed of generated speech"
                )
                
                generate_btn = gr.Button(
                    "🎙️ Generate Speech",
                    variant="primary",
                    size="lg"
                )
            
            with gr.Column(scale=1):
                progress_bar = gr.Slider(
                    label="Progress",
                    minimum=0,
                    maximum=100,
                    value=0,
                    interactive=False,
                    info="Generation progress"
                )
                status_box = gr.Textbox(
                    label="Status",
                    value="Ready to generate speech...",
                    lines=4,
                    interactive=False,
                    info="Current generation status and information"
                )
                audio_output = gr.Audio(
                    label="Generated Audio",
                    autoplay=True,
                    type="filepath"
                )
                gr.Markdown("<small><em>Generated speech audio will appear here</em></small>")
                delete_status = gr.Textbox(label="Status", visible=False)
        
        # Event handlers will be attached in the main app
        return {
            "tab": tab,
            "text_input": text_input,
            "voice_select": voice_select,
            "speed_slider": speed_slider,
            "generate_btn": generate_btn,
            "progress_bar": progress_bar,
            "status_box": status_box,
            "audio_output": audio_output,
            "delete_btn": delete_btn,
            "reload_btn": reload_btn,
            "delete_status": delete_status,
        }


def create_clone_tab(voice_service, tts_service) -> gr.Tab:
    """Create the voice cloning tab."""
    with gr.Tab("🧬 Clone Voice") as tab:
        gr.Markdown("### Create a New Voice Clone")
        gr.Markdown(
            "Upload a reference audio file (3-15 seconds) and provide the exact text "
            "spoken in the audio. The system will create a voice clone that can be "
            "used for speech generation."
        )
        
        with gr.Row():
            with gr.Column(scale=1):
                new_voice_name = gr.Textbox(
                    label="Voice Name",
                    placeholder="e.g., my_voice, narrator, character_1",
                    info="Choose a unique name for your voice clone"
                )
                ref_text_input = gr.Textbox(
                    label="Reference Text",
                    lines=4,
                    placeholder="Enter the exact text that is spoken in the reference audio...",
                    info="Must match exactly what is spoken in the audio file"
                )
                ref_audio_input = gr.Audio(
                    label="Reference Audio",
                    type="filepath"
                )
                gr.Markdown("<small><em>Upload a WAV file (3-15 seconds, clear audio, minimal background noise)</em></small>")
                clone_btn = gr.Button(
                    "🧬 Clone Voice",
                    variant="primary",
                    size="lg"
                )
            
            with gr.Column(scale=1):
                clone_status = gr.Textbox(
                    label="Status",
                    value="Ready to clone a voice...",
                    lines=8,
                    interactive=False,
                    info="Cloning status and information"
                )
        
        gr.Markdown("### Tips for Best Results")
        gr.Markdown("""
        - **Audio Quality**: Use clear, high-quality audio with minimal background noise
        - **Duration**: 3-15 seconds works best
        - **Format**: WAV format, mono channel, 16-44 kHz sample rate
        - **Text Match**: The reference text must match exactly what is spoken
        - **Voice Clarity**: Use a single speaker with clear pronunciation
        """)
        
        return {
            "tab": tab,
            "new_voice_name": new_voice_name,
            "ref_text_input": ref_text_input,
            "ref_audio_input": ref_audio_input,
            "clone_btn": clone_btn,
            "clone_status": clone_status,
        }
