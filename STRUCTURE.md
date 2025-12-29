# UACE Package Structure

```
uace-package/
│
├── pyproject.toml          # Modern Python packaging config
├── README.md               # Comprehensive documentation
├── DOCS.md                # Detailed API reference
├── LICENSE                 # MIT License
├── MANIFEST.in            # Package data manifest
├── .gitignore             # Git ignore rules
├── examples.py            # 10+ usage examples
│
├── src/uace/              # Main package source
│   ├── __init__.py        # Public API exports
│   ├── models.py          # Core data models (Pydantic)
│   ├── config.py          # Configuration system
│   ├── engine.py          # Main CaptionEngine
│   ├── cli.py             # Command-line interface (Click)
│   │
│   ├── engines/           # Transcription engines
│   │   ├── __init__.py
│   │   └── transcription.py  # Multi-engine abstraction
│   │       ├── FasterWhisperEngine
│   │       ├── WhisperXEngine
│   │       ├── DistilWhisperEngine
│   │       └── EngineSelector (intelligent selection)
│   │
│   ├── cleaning/          # Subtitle cleaning
│   │   ├── __init__.py
│   │   └── engine.py      # SubtitleCleaner
│   │       ├── Filler removal (language-aware)
│   │       ├── Sound effect removal
│   │       ├── Repetition collapsing
│   │       ├── Conversational normalization
│   │       └── Language-specific cleaners
│   │
│   ├── chunking/          # Semantic chunking
│   │   ├── __init__.py
│   │   └── semantic.py    # SemanticChunker
│   │       ├── Semantic strategy
│   │       ├── Sentence strategy
│   │       ├── Fixed-time strategy
│   │       └── ReadabilityOptimizer
│   │
│   ├── styling/           # Style presets
│   │   ├── __init__.py
│   │   └── presets.py     # StylePreset system
│   │       ├── VIRAL_POP
│   │       ├── MINIMAL
│   │       ├── KARAOKE
│   │       ├── SUBTITLE_CLASSIC
│   │       ├── BOUNCE
│   │       └── NEON
│   │
│   ├── export/            # Format exporters
│   │   ├── __init__.py
│   │   └── formats.py     # Multiple format support
│   │       ├── ASSExporter (with animations)
│   │       ├── SRTExporter
│   │       └── VTTExporter
│   │
│   └── utils/             # Utilities
│       └── __init__.py
│
└── tests/                 # Test suite
    ├── __init__.py
    └── test_uace.py       # Comprehensive tests
        ├── TestModels
        ├── TestCleaning
        ├── TestChunking
        ├── TestConfiguration
        ├── TestEngine
        ├── TestStyling
        ├── TestExport
        └── TestCLI
```

## Key Components

### 1. Core Models (models.py)
- `Caption` - Complete caption container
- `CaptionSegment` - Single segment with timing
- `Word` - Word-level timing data
- `TranscriptionResult` - Engine output
- `ProcessingPipeline` - Metadata tracking

### 2. Configuration (config.py)
- `ProcessingConfig` - Main configuration
- `TranscriptionConfig` - Engine settings
- `CleaningConfig` - Cleaning behavior
- `ChunkingConfig` - Chunking constraints
- `StylingConfig` - Visual styling
- `ExportConfig` - Output options
- Enums for all choices

### 3. Main Engine (engine.py)
- `CaptionEngine` - User-facing API
- Complete pipeline orchestration
- Progress tracking
- Error handling
- Convenience functions

### 4. Transcription (engines/transcription.py)
- Abstract `TranscriptionEngine` base
- Multi-engine implementations
- `EngineSelector` - Intelligent selection
- GPU/CPU optimization
- Diarization support

### 5. Cleaning (cleaning/engine.py)
- `SubtitleCleaner` - Main cleaner
- Language-specific rules
- Multiple cleaning modes
- Statistics tracking
- Non-destructive processing

### 6. Chunking (chunking/semantic.py)
- `SemanticChunker` - Smart chunking
- Multiple strategies
- Reading speed optimization
- Line splitting
- `ReadabilityOptimizer`

### 7. Styling (styling/presets.py)
- `StylePreset` - Declarative styling
- 6+ built-in presets
- ASS style generation
- Animation support
- Color management

### 8. Export (export/formats.py)
- `ASSExporter` - Full animation support
- `SRTExporter` - Basic compatibility
- `VTTExporter` - Web support
- Word-level animations
- Karaoke timing

### 9. CLI (cli.py)
- Beautiful Click interface
- `process` - Main command
- `styles` - List presets
- `engines` - Show available
- `doctor` - System check
- `demo` - Show examples

## Installation

```bash
# Basic
pip install .

# With extras
pip install ".[whisper]"
pip install ".[all]"

# Development
pip install -e ".[dev]"
```

## Usage

### CLI
```bash
uace process video.mp4
uace process video.mp4 --style viral_pop --cleaning aggressive
```

### Python API
```python
from uace import CaptionEngine

engine = CaptionEngine()
caption = engine.process("video.mp4", output="captions.ass")
```

## Features

✅ Multi-engine transcription (faster-whisper, WhisperX, Distil-Whisper)
✅ Intelligent text cleaning (language-aware)
✅ Semantic chunking (reading-optimized)
✅ Motion typography (CapCut-style animations)
✅ Speaker diarization
✅ Word-level timing
✅ Multiple export formats (ASS, SRT, VTT, JSON)
✅ Offline-first (no cloud dependencies)
✅ Fast processing (linear time)
✅ Complete type safety (Pydantic)
✅ Comprehensive tests
✅ Beautiful CLI
✅ Full documentation

## Architecture Highlights

### Engine-Agnostic Design
- Abstract base class for transcription engines
- Automatic engine selection based on requirements
- Graceful fallback

### Non-Destructive Processing
- Original text always preserved
- Full operation history tracked
- Reversible transformations

### Declarative Configuration
- Pydantic models for type safety
- Quick presets for common use cases
- Complete customization possible

### Pipeline Transparency
- Every stage tracked with metadata
- Processing time recorded
- Statistics computed

### Performance First
- Linear time algorithms
- GPU acceleration support
- Efficient batching
- Lazy loading

## Design Philosophy

1. **Offline First** - No cloud dependencies
2. **Software Agnostic** - Works with any video editor
3. **Linear Time** - Fast processing guaranteed
4. **Declarative** - Simple configuration, powerful results
5. **Graceful Degradation** - Falls back intelligently
6. **Transparent** - Full visibility into processing

## What Makes UACE Unique

- **Not just transcription** - Complete speech refinement
- **Cleaning as core feature** - Language-aware filler removal
- **Semantic chunking** - Respects meaning boundaries
- **Motion typography** - CapCut-style animations without vendor lock-in
- **Multi-engine** - Choose the right tool for the job
- **Offline capable** - No API keys or internet required

---

**UACE transforms raw speech into clean, animated captions that speak clearly and move beautifully.**
