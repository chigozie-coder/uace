"""
Transcription engines for UACE.
"""

from uace.engines.transcription import (
    TranscriptionEngine,
    EngineSelector,
)

# Try to import existing engines
try:
    from uace.engines.transcription import FasterWhisperEngine
except ImportError:
    FasterWhisperEngine = None

try:
    from uace.engines.transcription import WhisperXEngine
except ImportError:
    WhisperXEngine = None

try:
    from uace.engines.transcription import DistilWhisperEngine
except ImportError:
    DistilWhisperEngine = None

# Try to import HyperFast engines
HYPERFAST_AVAILABLE = False
try:
    from uace.engines.hyperfast import (
        HyperFastEngine,
        VoiceActivityDetector,
        FastSpeakerEmbedder,
    )
    HYPERFAST_AVAILABLE = True
except ImportError:
    HyperFastEngine = None
    VoiceActivityDetector = None
    FastSpeakerEmbedder = None

# Try to import HyperFast V2
HYPERFAST_V2_AVAILABLE = False
try:
    from uace.engines.hyperfast_v2 import (
        HyperFastV2,
        HyperFastPro,
        AudioEnhancer,
        ImprovedSpeakerEmbedder,
        TemporalSmoother,
    )
    HYPERFAST_V2_AVAILABLE = True
except ImportError:
    HyperFastV2 = None
    HyperFastPro = None
    AudioEnhancer = None
    ImprovedSpeakerEmbedder = None
    TemporalSmoother = None

__all__ = [
    'TranscriptionEngine',
    'EngineSelector',
    'HYPERFAST_AVAILABLE',
    'HYPERFAST_V2_AVAILABLE',
]

# Add available engines to exports
if FasterWhisperEngine:
    __all__.append('FasterWhisperEngine')
if WhisperXEngine:
    __all__.append('WhisperXEngine')
if DistilWhisperEngine:
    __all__.append('DistilWhisperEngine')

if HYPERFAST_AVAILABLE:
    __all__.extend(['HyperFastEngine', 'VoiceActivityDetector', 'FastSpeakerEmbedder'])

if HYPERFAST_V2_AVAILABLE:
    __all__.extend([
        'HyperFastV2',
        'HyperFastPro',
        'AudioEnhancer',
        'ImprovedSpeakerEmbedder',
        'TemporalSmoother',
    ])
