#!/bin/bash
# VoiceForge - Linux Setup Script
# This script installs all dependencies and sets up the environment

set -e  # Exit on error

echo "=========================================="
echo "VoiceForge - Linux Setup"
echo "=========================================="
echo ""

# Detect Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "⚠ Warning: Cannot detect Linux distribution"
    OS="unknown"
fi

echo "📦 Detected OS: $OS"
echo ""

# Install system dependencies
echo "🔧 Installing system dependencies..."
case $OS in
    ubuntu|debian)
        sudo apt update
        sudo apt install -y \
            espeak-ng \
            espeak-data \
            libespeak1 \
            libespeak-dev \
            python3 \
            python3-pip \
            python3-venv \
            git
        ;;
    arch|manjaro)
        sudo pacman -S --noconfirm \
            espeak-ng \
            python \
            python-pip \
            git
        ;;
    fedora|rhel|centos)
        sudo dnf install -y \
            espeak-ng \
            espeak-ng-devel \
            python3 \
            python3-pip \
            git
        ;;
    *)
        echo "⚠ Warning: Unsupported distribution. Please install manually:"
        echo "  - espeak-ng"
        echo "  - python3"
        echo "  - python3-pip"
        echo "  - python3-venv"
        ;;
esac

echo ""
echo "✅ System dependencies installed"
echo ""

# Check for CUDA (optional but recommended)
if command -v nvidia-smi &> /dev/null; then
    echo "🎮 NVIDIA GPU detected!"
    nvidia-smi --query-gpu=name --format=csv,noheader
    echo ""
    echo "💡 CUDA support will be enabled if PyTorch with CUDA is installed"
else
    echo "⚠ No NVIDIA GPU detected - will use CPU (slower)"
    echo ""
fi

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
if [ -d ".venv" ]; then
    echo "⚠ Virtual environment already exists, skipping..."
else
    python3 -m venv .venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
echo "   This may take several minutes..."
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "📁 Creating directories..."
mkdir -p samples
mkdir -p Models
mkdir -p temp
mkdir -p logs

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source .venv/bin/activate"
echo "  2. Run: python main.py"
echo ""
echo "Or use the run script:"
echo "  ./run_neutts.sh"
echo ""
