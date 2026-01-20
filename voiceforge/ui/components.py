"""UI components for VoiceForge."""

import gradio as gr
from typing import List, Optional

from voiceforge.config import get_settings

settings = get_settings()


def create_header() -> gr.HTML:
    """Create the application header with branding."""
    html_content = """
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="font-size: 3.5em; margin-bottom: 0.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            🎙️ VoiceForge
        </h1>
        <p style="font-size: 1.2em; color: #4a5568; margin-top: 0.5rem; font-weight: 500;">
            Professional Voice Cloning & Text-to-Speech
        </p>
        <p style="font-size: 0.95em; color: #718096; margin-top: 0.5rem;">
            Powered by <strong>NeuTTS Air</strong> • Transform text into natural speech with instant voice cloning
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
        gr.Markdown("### Convert Text to Speech")
        gr.Markdown("Select a voice and enter text to generate natural-sounding speech.")
        
        with gr.Row():
            with gr.Column(scale=1):
                text_input = gr.Textbox(
                    label="📝 Input Text",
                    lines=8,
                    placeholder="Enter the text you want to convert to speech...\n\nLong texts will be automatically split into chunks for optimal quality.",
                    info="💡 Tip: Use clear, well-punctuated text for best results"
                )
                
                with gr.Group():
                    with gr.Row():
                        voice_select = gr.Dropdown(
                            label=f"🎙️ Select Voice ({len(voice_choices)} available)",
                            choices=voice_choices,
                            value=voice_choices[0] if voice_choices else None,
                            interactive=True,
                            allow_custom_value=False,
                            info="Choose a cloned voice to use for speech generation",
                            scale=3
                        )
                        reload_btn = gr.Button("🔄", variant="secondary", size="sm", scale=1, tooltip="Reload voice list")
                        delete_btn = gr.Button("🗑️", variant="secondary", size="sm", scale=1, tooltip="Delete selected voice")
                
                speed_slider = gr.Slider(
                    label="⚡ Speech Speed",
                    minimum=settings.generation.min_speed,
                    maximum=settings.generation.max_speed,
                    value=settings.generation.default_speed,
                    step=settings.generation.speed_step,
                    info=f"Adjust playback speed ({settings.generation.min_speed}x - {settings.generation.max_speed}x)"
                )
                
                generate_btn = gr.Button(
                    "🎙️ Generate Speech",
                    variant="primary",
                    size="lg",
                    scale=1
                )
            
            with gr.Column(scale=1):
                progress_bar = gr.Slider(
                    label="⏳ Generation Progress",
                    minimum=0,
                    maximum=100,
                    value=0,
                    interactive=False,
                    info="Generation progress percentage"
                )
                status_box = gr.Textbox(
                    label="📊 Status",
                    value="✅ Ready to generate speech...",
                    lines=5,
                    interactive=False,
                    info="Current generation status and information"
                )
                audio_output = gr.Audio(
                    label="🎵 Generated Audio",
                    autoplay=True,
                    type="filepath",
                    show_download_button=True
                )
                gr.Markdown("""
                <div style="text-align: center; color: #718096; font-size: 0.9em; margin-top: 0.5rem;">
                    <em>Generated speech audio will appear here</em>
                </div>
                """)
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
                    label="📛 Voice Name",
                    placeholder="e.g., my_voice, narrator, character_1",
                    info="Choose a unique name for your voice clone (alphanumeric and underscores only)"
                )
                ref_text_input = gr.Textbox(
                    label="📝 Reference Text",
                    lines=5,
                    placeholder="Enter the exact text that is spoken in the reference audio...\n\n⚠️ Important: This must match exactly what is spoken in the audio file.",
                    info="The text must match exactly what is spoken in the audio"
                )
                ref_audio_input = gr.Audio(
                    label="🎵 Reference Audio",
                    type="filepath",
                    info="Upload a WAV file (3-15 seconds, clear audio, minimal background noise)"
                )
                gr.Markdown("""
                <div style="background: #f7fafc; padding: 1rem; border-radius: 5px; margin: 1rem 0;">
                    <strong>📋 Audio Requirements:</strong>
                    <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                        <li>Format: WAV</li>
                        <li>Duration: 3-15 seconds</li>
                        <li>Sample rate: 16-44 kHz</li>
                        <li>Channels: Mono</li>
                        <li>Quality: Clear, minimal background noise</li>
                    </ul>
                </div>
                """)
                clone_btn = gr.Button(
                    "🧬 Clone Voice",
                    variant="primary",
                    size="lg"
                )
            
            with gr.Column(scale=1):
                clone_status = gr.Textbox(
                    label="📊 Status",
                    value="✅ Ready to clone a voice...",
                    lines=10,
                    interactive=False,
                    info="Cloning status and information"
                )
        
        with gr.Accordion("💡 Tips for Best Results", open=False):
            gr.Markdown("""
            ### Audio Quality Guidelines
            
            - **Clear Audio**: Use high-quality recordings with minimal background noise
            - **Single Speaker**: Ensure only one person is speaking
            - **Natural Speech**: Use conversational, naturally-paced speech
            - **Good Pronunciation**: Clear enunciation works best
            
            ### Technical Requirements
            
            - **Duration**: 3-15 seconds is optimal (longer doesn't necessarily mean better)
            - **Format**: WAV format preferred
            - **Sample Rate**: 16-44 kHz supported
            - **Channels**: Mono (single channel) recommended
            
            ### Text Matching
            
            - **Exact Match**: The reference text must match exactly what is spoken
            - **Punctuation**: Include punctuation as it affects prosody
            - **Spelling**: Use correct spelling (phonemes are generated from text)
            
            ### Common Issues
            
            - ❌ **Poor quality**: Use better source audio
            - ❌ **Mismatched text**: Ensure text exactly matches audio
            - ❌ **Too short**: Use at least 3 seconds of audio
            - ❌ **Background noise**: Use clean recordings
            """)
        
        return {
            "tab": tab,
            "new_voice_name": new_voice_name,
            "ref_text_input": ref_text_input,
            "ref_audio_input": ref_audio_input,
            "clone_btn": clone_btn,
            "clone_status": clone_status,
        }
