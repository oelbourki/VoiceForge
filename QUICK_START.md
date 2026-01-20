# Quick Start Guide - Testing VoiceForge

## Step 1: Setup Environment

If you haven't set up the environment yet, run:

```bash
chmod +x setup_linux.sh
./setup_linux.sh
```

This will:
- Install system dependencies (eSpeak)
- Create Python virtual environment
- Install all Python packages
- Create necessary directories

**Note**: This may take 5-10 minutes depending on your internet speed (downloads models).

## Step 2: Run Test Script

Check if everything is set up correctly:

```bash
python3 test_app.py
```

This will verify:
- ✓ Directory structure
- ✓ All dependencies installed
- ✓ System requirements
- ✓ Configuration
- ✓ Voice service

## Step 3: Start the Application

### Option A: Using Run Script (Recommended)

```bash
chmod +x run_neutts.sh
./run_neutts.sh
```

### Option B: Manual

```bash
source .venv/bin/activate
python main.py
```

## Step 4: Access Web Interface

The application will:
1. Check eSpeak installation
2. Load TTS models (first time downloads from HuggingFace)
3. Initialize services
4. Open web interface at `http://localhost:7860`

**First run**: Model download may take 5-15 minutes depending on connection.

## Quick Test Checklist

Once the web interface opens:

### ✅ Test 1: Check Voice List
- Go to "🎤 Generate Speech" tab
- Check if voice dropdown shows existing voices
- Should see voices from `samples/` directory

### ✅ Test 2: Clone a Voice
1. Go to "🧬 Clone Voice" tab
2. Enter name: `test_voice`
3. Upload a WAV file (3-15 seconds, clear audio)
4. Enter exact text from audio
5. Click "🧬 Clone Voice"
6. Should see success message

### ✅ Test 3: Generate Speech
1. Go to "🎤 Generate Speech" tab
2. Select a voice
3. Enter text: "Hello, this is a test of VoiceForge."
4. Click "🎙️ Generate Speech"
5. Should see progress bar and audio output

### ✅ Test 4: Voice Management
- Click "🔄 Reload" - should refresh voice list
- Select voice and click "🗑️ Delete" - should remove voice

## Troubleshooting

### Missing Dependencies

If test script shows missing modules:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### eSpeak Not Found

```bash
# Ubuntu/Debian
sudo apt install espeak-ng espeak-data libespeak1 libespeak-dev

# Arch Linux
sudo pacman -S espeak-ng

# Fedora
sudo dnf install espeak-ng espeak-ng-devel
```

### Model Download Fails

- Check internet connection
- Ensure ~5GB free disk space
- First download can take 10-20 minutes
- Models are cached in `Models/` directory

### Port Already in Use

If port 7860 is busy, edit `voiceforge/config/settings.py`:

```python
ui = UIConfig(
    server_port=7861  # Change to different port
)
```

## Expected Output

### Successful Startup

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
Voice Service initialized with X voice(s)
Creating UI...
============================================================
🌐 Web interface will open at: http://localhost:7860
============================================================
```

### Web Interface Features

- **Header**: VoiceForge branding with gradient
- **Generate Speech Tab**: 
  - Text input
  - Voice selector
  - Speed slider
  - Progress tracking
  - Audio output
- **Clone Voice Tab**:
  - Voice name input
  - Reference text
  - Audio upload
  - Status messages

## Performance Notes

- **First Run**: Slow (downloads models)
- **CPU Mode**: ~3-5 seconds per sentence
- **GPU Mode**: ~1-2 seconds per sentence
- **Long Text**: Automatically split into chunks

## Next Steps

After successful testing:
1. ✅ Clone multiple voices
2. ✅ Test different text lengths
3. ✅ Experiment with speed settings
4. ✅ Generate longer audio samples
5. ✅ Verify audio quality

Enjoy VoiceForge! 🎙️✨
