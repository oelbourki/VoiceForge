"""Configuration constants for NeuTTSAir."""

# Audio constants
SAMPLE_RATE = 24_000
MAX_CONTEXT = 2048
HOP_LENGTH = 480

# Streaming parameters
STREAMING_OVERLAP_FRAMES = 1
STREAMING_FRAMES_PER_CHUNK = 25
STREAMING_LOOKFORWARD = 5
STREAMING_LOOKBACK = 50

def get_streaming_stride_samples():
    return STREAMING_FRAMES_PER_CHUNK * HOP_LENGTH
