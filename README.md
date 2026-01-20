# 🎙️ VoiceForge

**Professional Voice Cloning & Text-to-Speech Application**

VoiceForge is a modern, professional-grade voice cloning and text-to-speech application built on NeuTTS Air. Transform text into natural speech with instant voice cloning capabilities, featuring a clean modular architecture and beautiful user interface.

## Features

- 🎙️ **Instant Voice Cloning**: Clone any voice from 3-15 seconds of reference audio
- 🚀 **GPU Acceleration**: CUDA support for fast inference (CPU fallback available)
- 🌐 **Web Interface**: User-friendly Gradio interface
- 📱 **On-Device**: Runs locally, no cloud API required
- 🔒 **Watermarked**: All outputs include imperceptible watermarks

## Requirements

### System Requirements

- **OS**: Linux (Ubuntu 20.04+, Debian 11+, Arch Linux, Fedora, etc.)
- **Python**: 3.11 or higher
- **RAM**: 8GB minimum (16GB recommended)
- **GPU**: NVIDIA GPU with CUDA support (optional but recommended)
- **Disk Space**: ~5GB for models and dependencies

### System Dependencies

- **eSpeak-ng**: For phonemization (text-to-phoneme conversion)

## Quick Start

### 1. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y espeak-ng espeak-data libespeak1 libespeak-dev python3 python3-pip python3-venv
```

**Arch Linux:**
```bash
sudo pacman -S espeak-ng python python-pip
```

**Fedora:**
```bash
sudo dnf install espeak-ng espeak-ng-devel python3 python3-pip
```

### 2. Run Setup Script

```bash
chmod +x setup_linux.sh
./setup_linux.sh
```

This will:
- Install system dependencies
- Create Python virtual environment
- Install Python packages
- Set up directories

### 3. Run the Application

**Option 1: Using the run script**
```bash
chmod +x run_neutts.sh
./run_neutts.sh
```

**Option 2: Manual activation**
```bash
source .venv/bin/activate
python main.py
```

The web interface will open at `http://localhost:7860`

## Usage

### Cloning a Voice

1. Go to the "Instantly Clone New Voice" tab
2. Enter a name for your voice
3. Upload a reference audio file (`.wav` format, 3-15 seconds)
4. Enter the exact text spoken in the audio
5. Click "Clone Voice"

**Reference Audio Requirements:**
- Format: WAV
- Sample rate: 16-44 kHz
- Channels: Mono
- Duration: 3-15 seconds
- Quality: Clear, minimal background noise

### Generating Speech

1. Go to the "Generate Speech" tab
2. Select a cloned voice from the dropdown
3. Enter the text you want to synthesize
4. Adjust speed (optional, 0.5x to 2.0x)
5. Click "Generate Speech"

The system will:
- Split long texts into chunks
- Generate audio for each chunk
- Combine chunks with proper spacing
- Apply speed adjustment
- Return the final audio file

## Project Structure

VoiceForge features a professional, modular architecture:

```
VoiceForge/
├── main.py                 # Main entry point
├── voiceforge/             # Main package
│   ├── config/             # Configuration management
│   ├── models/             # Model loading
│   ├── services/           # Business logic (TTS, Voice management)
│   ├── ui/                 # User interface components
│   └── utils/              # Utilities (logging, system checks)
├── neuttsair/              # Core TTS module
├── samples/                # Voice samples directory
├── Models/                 # Model cache
├── temp/                   # Temporary files
└── logs/                   # Application logs
```

For detailed structure information, see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).

**Note**: The `neuttsair` module is included in this repository. Make sure it's present in the project directory.

## Troubleshooting

### eSpeak Not Found

**Error**: `Error: espeak-ng not found!`

**Solution**:
```bash
# Ubuntu/Debian
sudo apt install espeak-ng

# Arch Linux
sudo pacman -S espeak-ng

# Verify installation
which espeak-ng
```

### CUDA Not Available

**Warning**: `CUDA not available, using CPU`

**Solutions**:
1. Install NVIDIA drivers: `sudo apt install nvidia-driver-xxx`
2. Install CUDA toolkit (if needed)
3. Install PyTorch with CUDA: `pip install torch --index-url https://download.pytorch.org/whl/cu118`

### Model Download Fails

**Error**: Model download timeout or failure

**Solutions**:
1. Check internet connection
2. Increase timeout in code
3. Download models manually from HuggingFace
4. Place in `Models/neutts-air/` directory

### Out of Memory

**Error**: CUDA out of memory

**Solutions**:
1. Use CPU mode (slower but uses less memory)
2. Reduce text chunk size
3. Use quantized models (GGUF format)
4. Close other GPU applications

### Audio Generation Fails

**Error**: Failed to generate audio

**Solutions**:
1. Verify reference audio format (WAV, mono, 16-44kHz)
2. Check text encoding (UTF-8)
3. Ensure reference text matches audio exactly
4. Check disk space

## Advanced Configuration

### Using Local Models

Place models in `Models/neutts-air/` directory:
```
Models/
└── neutts-air/
    └── models--neuphonic--neutts-air/
        └── snapshots/
            └── [snapshot-hash]/
                ├── config.json
                └── ...
```

### Custom Device Selection

Edit `voiceforge/config/settings.py` to change device:
```python
model = ModelConfig(
    backbone_device="cuda",  # or "cpu" or "auto"
    codec_device="cuda"
)
```

### Changing Port

Edit `voiceforge/config/settings.py`:
```python
ui = UIConfig(
    server_port=7861  # Change port number
)
```

## Performance Tips

1. **Use GPU**: Significantly faster than CPU
2. **Pre-encode voices**: Saves `.pt` files for faster loading
3. **Optimize reference audio**: Use clear, 5-10 second samples
4. **Batch processing**: Process multiple texts in sequence
5. **Monitor memory**: Close other applications when using GPU

## Professional Features

- 🏗️ **Modular Architecture**: Clean separation of concerns, easy to maintain and extend
- ⚙️ **Configuration Management**: Centralized settings, easy to customize
- 📝 **Comprehensive Logging**: File and console logging for debugging and monitoring
- 🎨 **Modern UI**: Professional interface with VoiceForge branding
- 🔧 **Service Layer**: Reusable business logic, easy to test
- 📚 **Type Hints**: Better IDE support and code clarity
- 🛡️ **Error Handling**: Robust error handling with meaningful messages

See [IMPROVEMENTS.md](IMPROVEMENTS.md) for detailed information about the professional improvements.

## License

Same as original NeuTTS Air project. Please refer to the original repository for license information.

## Credits

- **Original Project**: [NeuTTS Air](https://github.com/neuphonic/neutts-air)
- **Model**: Neuphonic
- **VoiceForge**: Professional modular implementation

## Documentation

- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Detailed project structure
- [IMPROVEMENTS.md](IMPROVEMENTS.md) - Professional improvements made

## Support

For issues specific to this Linux port, please check:
1. System dependencies are installed
2. Virtual environment is activated
3. Python version is 3.11+
4. CUDA is properly configured (if using GPU)

For general NeuTTS Air issues, refer to the [original repository](https://github.com/neuphonic/neutts-air).

---

**Enjoy professional voice cloning with VoiceForge! 🎙️✨**
