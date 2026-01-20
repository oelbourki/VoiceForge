"""Main Gradio application for VoiceForge."""

import gradio as gr
from typing import Tuple, Optional

from voiceforge.config import get_settings
from voiceforge.services import TTSService, VoiceService
from voiceforge.utils import get_logger
from .components import create_header, create_generation_tab, create_clone_tab

logger = get_logger(__name__)


def create_app(tts_service: TTSService, voice_service: VoiceService) -> gr.Blocks:
    """
    Create and configure the Gradio application.
    
    Args:
        tts_service: Initialized TTS service
        voice_service: Initialized voice service
        
    Returns:
        Configured Gradio Blocks app
    """
    settings = get_settings()
    
    # Get initial voice list
    voice_choices = voice_service.get_voices()
    
    # Create app
    with gr.Blocks(
        title=settings.ui.title,
        theme=gr.themes.Soft() if settings.ui.theme == "soft" else gr.themes.Default()
    ) as app:
        # Header
        create_header()
        
        # Create tabs
        gen_components = create_generation_tab(voice_choices, voice_service, tts_service)
        clone_components = create_clone_tab(voice_service, tts_service)
        
        # Generation tab event handlers
        def handle_generate(text: str, voice_name: str, speed: float):
            """Handle speech generation."""
            if not text or not text.strip():
                yield 0, None, "❌ Error: Input text cannot be empty.", None
                return
            
            if not voice_name:
                yield 0, None, "❌ Error: No voice selected. Please select a voice.", None
                return
            
            try:
                ref_text, ref_codes = voice_service.load_reference(voice_name, tts_service.tts)
                
                # Generate speech
                for progress, audio_path, status, error in tts_service.generate_speech(
                    text, ref_codes, ref_text, speed
                ):
                    yield progress, audio_path, status, error
                    
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                logger.error(error_msg, exc_info=True)
                yield 0, None, error_msg, None
        
        def handle_delete(voice_name: str) -> Tuple[str, gr.update]:
            """Handle voice deletion."""
            try:
                voice_service.delete_voice(voice_name)
                remaining_voices = voice_service.get_voices()
                new_selected = remaining_voices[0] if remaining_voices else None
                return (
                    f"✅ Voice '{voice_name}' deleted successfully!",
                    gr.update(choices=remaining_voices, value=new_selected)
                )
            except Exception as e:
                error_msg = f"❌ Error deleting voice: {e}"
                logger.error(error_msg, exc_info=True)
                return error_msg, gr.update()
        
        def handle_reload() -> gr.update:
            """Handle voice reload."""
            voices = voice_service.reload()
            return gr.update(choices=voices, value=voices[0] if voices else None)
        
        def handle_clone(voice_name: str, ref_text: str, audio_file: Optional[str]) -> Tuple[str, gr.update]:
            """Handle voice cloning."""
            try:
                if not audio_file:
                    return "❌ Error: No reference audio file provided.", gr.update()
                
                message = voice_service.clone_voice(
                    voice_name,
                    ref_text,
                    audio_file,
                    tts_service.tts
                )
                
                # Reload voices and update dropdown
                voices = voice_service.reload()
                return message, gr.update(choices=voices, value=voice_name)
            except Exception as e:
                error_msg = f"❌ Error cloning voice: {e}"
                logger.error(error_msg, exc_info=True)
                return error_msg, gr.update()
        
        # Attach event handlers
        gen_components["generate_btn"].click(
            fn=handle_generate,
            inputs=[
                gen_components["text_input"],
                gen_components["voice_select"],
                gen_components["speed_slider"]
            ],
            outputs=[
                gen_components["progress_bar"],
                gen_components["audio_output"],
                gen_components["status_box"],
                gen_components["delete_status"]
            ]
        )
        
        gen_components["delete_btn"].click(
            fn=handle_delete,
            inputs=[gen_components["voice_select"]],
            outputs=[gen_components["delete_status"], gen_components["voice_select"]]
        )
        
        gen_components["reload_btn"].click(
            fn=handle_reload,
            outputs=[gen_components["voice_select"]]
        )
        
        clone_components["clone_btn"].click(
            fn=handle_clone,
            inputs=[
                clone_components["new_voice_name"],
                clone_components["ref_text_input"],
                clone_components["ref_audio_input"]
            ],
            outputs=[clone_components["clone_status"], gen_components["voice_select"]]
        )
    
    return app
