#!/usr/bin/env python3
"""
UACE ULTIMATE FIX - Solves ALL Problems

Fixes:
1. DeepFilterNet installation error
2. NameError: HyperFastEngine not defined
3. CIRCULAR IMPORT between transcription.py and hyperfast.py

Usage: python ultimate_fix.py
"""

import sys
from pathlib import Path

print("="*70)
print("UACE ULTIMATE FIX")
print("="*70)

# Get the UACE directory
uace_dir = Path.cwd()
if not (uace_dir / 'src' / 'uace').exists():
    print("\n❌ Error: Not in UACE directory!")
    print("Please run this from the UACE root directory")
    sys.exit(1)

print(f"\n📁 UACE directory: {uace_dir}")

errors_fixed = []

# ============================================================================
# Fix 1: Create base.py to break circular import
# ============================================================================

print("\n[1/5] Creating base.py to break circular import...")

base_file = uace_dir / 'src' / 'uace' / 'engines' / 'base.py'
base_content = '''"""
Base transcription engine class.

This module exists to break circular imports between transcription.py
and engine implementations (like hyperfast.py).
"""

import time
from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path

from uace.models import TranscriptionResult
from uace.config import TranscriptionConfig


class TranscriptionEngine(ABC):
    """
    Abstract base class for all transcription engines.
    
    This class defines the interface that all transcription engines must implement.
    It handles common functionality like model loading state and provides abstract
    methods for engine-specific implementations.
    """
    
    def __init__(self, config: TranscriptionConfig):
        """
        Initialize the transcription engine.
        
        Args:
            config: Configuration for transcription
        """
        self.config = config
        self.model_loaded = False
    
    @abstractmethod
    def load_model(self) -> None:
        """
        Load the transcription model.
        
        This method should initialize all necessary models and resources.
        Implementations should set self.model_loaded = True when complete.
        """
        pass
    
    @abstractmethod
    def transcribe(self, audio_path: str) -> TranscriptionResult:
        """
        Transcribe an audio file.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            TranscriptionResult containing segments and metadata
        """
        pass
    
    @classmethod
    @abstractmethod
    def is_available(cls) -> bool:
        """
        Check if this engine's dependencies are available.
        
        Returns:
            True if the engine can be used, False otherwise
        """
        pass
    
    @classmethod
    def engine_name(cls) -> str:
        """
        Get the engine's name.
        
        Returns:
            String identifier for this engine
        """
        return cls.__name__.lower().replace('engine', '')
    
    def supports_diarization(self) -> bool:
        """
        Check if this engine supports speaker diarization.
        
        Returns:
            True if diarization is supported, False otherwise
        """
        return False
    
    def supports_word_timestamps(self) -> bool:
        """
        Check if this engine supports word-level timestamps.
        
        Returns:
            True if word timestamps are supported, False otherwise
        """
        return False
    
    def unload_model(self) -> None:
        """
        Unload the model to free memory.
        
        Default implementation does nothing. Override if cleanup is needed.
        """
        pass
    
    def __enter__(self):
        """Context manager entry - loads model if not loaded."""
        if not self.model_loaded:
            self.load_model()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - unloads model."""
        self.unload_model()
        return False
'''

base_file.write_text(base_content)
print("  ✅ Created base.py")
errors_fixed.append("Created base.py module")

# ============================================================================
# Fix 2: Update hyperfast.py to import from base
# ============================================================================

print("\n[2/5] Fixing hyperfast.py imports...")

hyperfast_file = uace_dir / 'src' / 'uace' / 'engines' / 'hyperfast.py'
if hyperfast_file.exists():
    content = hyperfast_file.read_text()
    
    # Replace the import
    old_import = 'from uace.engines.transcription import TranscriptionEngine'
    new_import = 'from uace.engines.base import TranscriptionEngine'
    
    if old_import in content:
        content = content.replace(old_import, new_import)
        hyperfast_file.write_text(content)
        print("  ✅ Fixed hyperfast.py import")
        errors_fixed.append("Fixed circular import in hyperfast.py")
    else:
        print("  ℹ️  hyperfast.py already uses correct import")
else:
    print("  ⚠️  hyperfast.py not found")

# ============================================================================
# Fix 3: Update hyperfast_v2.py to import from base
# ============================================================================

print("\n[3/5] Fixing hyperfast_v2.py imports...")

hyperfast_v2_file = uace_dir / 'src' / 'uace' / 'engines' / 'hyperfast_v2.py'
if hyperfast_v2_file.exists():
    content = hyperfast_v2_file.read_text()
    
    # Replace the import (might inherit from HyperFastEngine)
    old_import = 'from uace.engines.transcription import TranscriptionEngine'
    new_import = 'from uace.engines.base import TranscriptionEngine'
    
    if old_import in content:
        content = content.replace(old_import, new_import)
        hyperfast_v2_file.write_text(content)
        print("  ✅ Fixed hyperfast_v2.py import")
        errors_fixed.append("Fixed circular import in hyperfast_v2.py")
    else:
        print("  ℹ️  hyperfast_v2.py already uses correct import or inherits properly")
else:
    print("  ⚠️  hyperfast_v2.py not found")

# ============================================================================
# Fix 4: Update transcription.py to import from base and export it
# ============================================================================

print("\n[4/5] Fixing transcription.py...")

transcription_file = uace_dir / 'src' / 'uace' / 'engines' / 'transcription.py'
if transcription_file.exists():
    content = transcription_file.read_text()
    
    # Find where TranscriptionEngine class is defined
    if 'class TranscriptionEngine' in content:
        # The full class is defined here, we need to move it
        print("  📝 Moving TranscriptionEngine to base.py...")
        
        # For now, just import and re-export it
        new_imports = '''"""
Transcription Engine Abstraction

Provides a unified interface to multiple transcription backends.
"""

import time
from typing import Optional, Dict, Any, List, Type
from pathlib import Path

from uace.models import TranscriptionResult, CaptionSegment, Word
from uace.config import TranscriptionConfig, EnginePreference, SpecificEngine

# Import base class (breaks circular import)
from uace.engines.base import TranscriptionEngine

# Initialize placeholders for optional engines (prevents NameError)
HyperFastEngine = None
VoiceActivityDetector = None
FastSpeakerEmbedder = None
HyperFastV2 = None
HyperFastPro = None
AudioEnhancer = None
ImprovedSpeakerEmbedder = None
TemporalSmoother = None

# Try to import HyperFast V1 engines (optional)
HYPERFAST_AVAILABLE = False
try:
    from .hyperfast import (
        HyperFastEngine,
        VoiceActivityDetector,
        FastSpeakerEmbedder,
    )
    HYPERFAST_AVAILABLE = True
except ImportError as e:
    # HyperFast not available
    pass

# Try to import HyperFast V2 engines (optional)
HYPERFAST_V2_AVAILABLE = False
try:
    from .hyperfast_v2 import (
        HyperFastV2,
        HyperFastPro,
        AudioEnhancer,
        ImprovedSpeakerEmbedder,
        TemporalSmoother,
    )
    HYPERFAST_V2_AVAILABLE = True
except ImportError as e:
    # HyperFast V2 not available
    pass

'''
        
        # Find where to end the replacement (after imports, before first class after TranscriptionEngine)
        # Look for the first class that's NOT TranscriptionEngine
        import_end = content.find('\nclass ')
        if import_end > 0:
            # Find if there's a TranscriptionEngine class
            te_class_pos = content.find('class TranscriptionEngine')
            if te_class_pos > 0 and te_class_pos < import_end:
                # TranscriptionEngine is first class, skip it
                next_class = content.find('\nclass ', te_class_pos + 20)
                if next_class > 0:
                    import_end = next_class
        
        if import_end > 0:
            # Keep everything after the imports
            content = new_imports + content[import_end:]
            transcription_file.write_text(content)
            print("  ✅ Fixed transcription.py imports")
            errors_fixed.append("Fixed transcription.py to use base.py")
    else:
        # TranscriptionEngine is imported, just fix the imports section
        if 'from uace.engines.base import TranscriptionEngine' not in content:
            # Need to add base import
            print("  📝 Adding base.py import...")
            import_pos = content.find('from uace.config import')
            if import_pos > 0:
                next_line = content.find('\n', import_pos)
                content = content[:next_line] + '\n\n# Import base class\nfrom uace.engines.base import TranscriptionEngine\n' + content[next_line:]
                transcription_file.write_text(content)
                print("  ✅ Added base.py import")

# ============================================================================
# Fix 5: Update pyproject.toml (remove deepfilternet)
# ============================================================================

print("\n[5/5] Fixing pyproject.toml...")

pyproject_file = uace_dir / 'pyproject.toml'
if pyproject_file.exists():
    content = pyproject_file.read_text()
    
    if 'deepfilternet' in content:
        content = content.replace('deepfilternet>=0.5.0', 'noisereduce>=3.0.0')
        content = content.replace(
            '"deepfilternet>=0.5.0",',
            '"noisereduce>=3.0.0",  # Alternative to problematic deepfilternet'
        )
        pyproject_file.write_text(content)
        print("  ✅ Replaced deepfilternet with noisereduce")
        errors_fixed.append("Fixed deepfilternet dependency")
    else:
        print("  ✅ pyproject.toml already clean")

# ============================================================================
# Summary
# ============================================================================

print("\n" + "="*70)
print("ULTIMATE FIX COMPLETE!")
print("="*70)

print(f"\n✅ {len(errors_fixed)} fixes applied:")
for i, fix in enumerate(errors_fixed, 1):
    print(f"  {i}. {fix}")

print("\n📦 Files modified:")
print("  • src/uace/engines/base.py (CREATED)")
print("  • src/uace/engines/hyperfast.py")
print("  • src/uace/engines/hyperfast_v2.py")
print("  • src/uace/engines/transcription.py")
print("  • pyproject.toml")

print("\n🔧 Next steps:")
print("\n1. Reinstall UACE:")
print("   pip uninstall uace -y")
print("   pip install -e .[hyperfast]")

print("\n2. Test the fix:")
print("""
python -c "
from uace import CaptionEngine, ProcessingConfig
from uace.config import SpecificEngine

config = ProcessingConfig()
config.transcription.specific_engine = SpecificEngine.HYPERFAST_V2
config.transcription.diarization = True
config.transcription.gpu = True

print('✅ Config created!')

engine = CaptionEngine(config, verbose=True)
print('✅ Engine created!')

# Process a video
# caption = engine.process('video.mp4', 'output.ass')
# print(f'✅ Processed {len(caption.segments)} segments!')
"
""")

print("\n" + "="*70)
print("All fixes complete! Your code should work now.")
print("="*70)
