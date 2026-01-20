# Testing VoiceForge

This guide helps you test your VoiceForge application.

## Quick Test

Run the test script to check if everything is set up correctly:

```bash
python3 test_app.py
```

This will check:
- ✓ Directory structure
- ✓ Python imports
- ✓ System requirements (eSpeak)
- ✓ Configuration loading
- ✓ Voice service initialization

## Setup Before Testing

If you haven't set up the environment yet:

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
- Create virtual environment
- Install Python dependencies
- Create necessary directories

### 3. Run Test Script

```bash
python3 test_app.py
```

## Running the Application

### Option 1: Using Run Script

```bash
chmod +x run_neutts.sh
./run_neutts.sh
```

### Option 2: Manual

```bash
source .venv/bin/activate
python main.py
```

The web interface will open at `http://localhost:7860`

## Testing Features

### 1. Test Voice Cloning

1. Go to "🧬 Clone Voice" tab
2. Enter a voice name (e.g., "test_voice")
3. Upload a reference audio file (WAV, 3-15 seconds)
4. Enter the exact text spoken in the audio
5. Click "🧬 Clone Voice"
6. Should see success message

### 2. Test Speech Generation

1. Go to "🎤 Generate Speech" tab
2. Select a cloned voice from dropdown
3. Enter some text (e.g., "Hello, this is a test.")
4. Click "🎙️ Generate Speech"
5. Should see progress and audio output

### 3. Test Voice Management

1. Click "🔄 Reload" to refresh voice list
2. Select a voice and click "🗑️ Delete" to remove it
3. Verify voice is removed from list

## Troubleshooting

### Import Errors

If you see import errors:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### eSpeak Not Found

```bash
# Check if installed
which espeak-ng

# Install if missing
sudo apt install espeak-ng  # Ubuntu/Debian
sudo pacman -S espeak-ng     # Arch
sudo dnf install espeak-ng   # Fedora
```

### Model Download Issues

On first run, models will be downloaded from HuggingFace:
- Ensure internet connection
- Check disk space (~2-4 GB needed)
- Be patient, download can take time

### CUDA Issues

If CUDA is not available:
- App will automatically use CPU (slower but works)
- To use GPU, ensure PyTorch with CUDA is installed:
  ```bash
  pip install torch --index-url https://download.pytorch.org/whl/cu118
  ```

## Expected Behavior

### Successful Startup

You should see:
```
============================================================
🚀 Starting VoiceForge
============================================================
Checking eSpeak installation...
✓ eSpeak found
Initializing TTS model...
Loading phonemizer...
Loading backbone from: neuphonic/neutts-air on cuda...
Loading codec from: neuphonic/neucodec on cuda...
✅ Model initialized successfully!
Initializing services...
Creating UI...
============================================================
🌐 Web interface will open at: http://localhost:7860
============================================================
```

### Web Interface

- Should open automatically in browser
- Two tabs: "🎤 Generate Speech" and "🧬 Clone Voice"
- Voice dropdown should show available voices
- All buttons should be functional

## Performance Testing

### CPU vs GPU

- **CPU**: Slower but works on any machine
- **GPU**: Much faster, recommended if available

Test generation time:
- Short text (< 50 words): Should complete in < 30 seconds
- Long text (> 200 words): May take 1-3 minutes

### Memory Usage

- Minimum: 8GB RAM
- Recommended: 16GB RAM
- GPU: 4GB+ VRAM recommended

## Log Files

Check logs for detailed information:
```bash
ls -la logs/
tail -f logs/voiceforge_*.log
```

## Next Steps

After successful testing:
1. Clone some voices
2. Generate speech samples
3. Test different text lengths
4. Experiment with speed settings
5. Verify audio quality

Happy testing! 🎉
