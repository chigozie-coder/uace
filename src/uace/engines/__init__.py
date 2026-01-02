"""
Transcription Engines

Multi-engine support for speech-to-text transcription.
"""

from uace.engines.transcription import (
    TranscriptionEngine,
    FasterWhisperEngine,
    WhisperXEngine,
    DistilWhisperEngine,
    EngineSelector,
)

# NEW: Import HyperFast engines
try:
    from .hyperfast import (
        HyperFastEngine,
        VoiceActivityDetector,
        FastSpeakerEmbedder,
    )
    from .hyperfast_v2 import (
        HyperFastV2,
        HyperFastPro,
        AudioEnhancer,
        ImprovedSpeakerEmbedder,
        TemporalSmoother,
    )
    HYPERFAST_AVAILABLE = True
except ImportError:
    HYPERFAST_AVAILABLE = False

__all__ = [
    "TranscriptionEngine",
    "FasterWhisperEngine",
    "WhisperXEngine",
    "DistilWhisperEngine",
    "EngineSelector",
]

if HYPERFAST_AVAILABLE:
    __all__.extend([
        "HyperFastEngine",
        "HyperFastV2",
        "HyperFastPro",
        "VoiceActivityDetector",
        "FastSpeakerEmbedder",
        "ImprovedSpeakerEmbedder",
        "AudioEnhancer",
        "TemporalSmoother",
        "HYPERFAST_AVAILABLE"
    ])