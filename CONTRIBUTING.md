# Contributing to VoiceForge

Thank you for your interest in contributing to VoiceForge! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/VoiceForge.git`
3. Create a virtual environment: `python3 -m venv .venv`
4. Activate it: `source .venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Create a new branch: `git checkout -b feature/your-feature-name`

## Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose

### Project Structure

- `voiceforge/config/` - Configuration management
- `voiceforge/models/` - Model loading
- `voiceforge/services/` - Business logic
- `voiceforge/ui/` - User interface
- `voiceforge/utils/` - Utility functions

### Commit Messages

Use clear, descriptive commit messages:
- `feat: Add new feature`
- `fix: Fix bug in voice service`
- `docs: Update README`
- `refactor: Restructure TTS service`

### Testing

Before submitting a pull request:
- Test your changes thoroughly
- Ensure the application runs without errors
- Check that existing functionality still works

## Pull Request Process

1. Update the README.md if needed
2. Ensure your code follows the project structure
3. Test your changes
4. Submit a pull request with a clear description

## Reporting Issues

Use the GitHub issue tracker to report bugs or request features. Include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)

## Questions?

Feel free to open an issue for questions or discussions.

Thank you for contributing! 🎉
