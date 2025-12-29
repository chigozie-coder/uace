# UACE Documentation

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Core Concepts](#core-concepts)
4. [API Reference](#api-reference)
5. [Configuration](#configuration)
6. [Style Presets](#style-presets)
7. [Advanced Usage](#advanced-usage)
8. [Performance Tuning](#performance-tuning)
9. [Troubleshooting](#troubleshooting)

## Installation

### Basic Installation

```bash
pip install uace
```

### With Transcription Engines

```bash
# faster-whisper (recommended)
pip install "uace[whisper]"

# WhisperX (for diarization)
pip install "uace[whisperx]"

# Distil-Whisper (fast CPU)
pip install "uace[distil]"

# All engines
pip install "uace[all]"
```

### For Development

```bash
git clone https://github.com/uace/uace
cd uace
pip install -e ".[dev]"
```

## Quick Start

### CLI

```bash
# Process video with defaults
uace process video.mp4

# Custom style and cleaning
uace process video.mp4 --style viral_pop --cleaning aggressive

# View available styles
uace styles

# Check system
uace doctor
```

### Python API

```python
from uace import CaptionEngine

# Simple usage
engine = CaptionEngine()
caption = engine.process("video.mp4", output="captions.ass")

# Print results
print(f"Generated {len(caption.segments)} segments")
for segment in caption.segments[:3]:
    print(f"{segment.start:.2f}s: {segment.text}")
```

## Core Concepts

### The Pipeline

UACE processes captions through five stages:

```
TRANSCRIBE → CLEAN → CHUNK → STYLE → EXPORT
```

Each stage is:
- **Configurable** - Full control over behavior
- **Non-destructive** - Original data preserved
- **Transparent** - Complete metadata available
- **Fast** - Linear time complexity

### Transcription

Converts audio to text using ML models.

**Engines:**
- `faster-whisper` - Default, fastest
- `whisperx` - Advanced alignment + diarization
- `distil-whisper` - Ultra-fast CPU
- `openai-whisper` - Maximum accuracy

**Features:**
- Word-level timestamps
- Speaker diarization
- Multi-language support
- Confidence scores

### Cleaning

Transforms raw transcription into readable text.

**Operations:**
- Filler removal ("um", "uh", "like")
- Sound effect removal ([laughter], [music])
- Repetition collapsing ("I I I" → "I")
- Conversational normalization

**Modes:**
- `none` - Raw transcript
- `light` - Minimal cleaning
- `balanced` - Default, good for most content
- `aggressive` - Maximum cleaning for short-form

### Chunking

Breaks text into readable caption segments.

**Strategies:**
- `semantic` - Respects meaning boundaries (default)
- `sentence` - Splits on sentences
- `fixed_time` - Fixed duration chunks
- `word_count` - Fixed word count
- `punctuation` - Splits on punctuation

**Constraints:**
- Max characters per line (default: 42)
- Max lines per segment (default: 2)
- Reading speed (default: 20 chars/second)

### Styling

Applies visual styling and animations.

**Presets:**
- `viral_pop` - TikTok/Shorts style
- `minimal` - Clean, professional
- `karaoke` - Music video style
- `subtitle_classic` - Traditional
- `bounce` - Energetic animation
- `neon` - Cyberpunk glow

**Features:**
- Word-by-word animation
- Color customization
- Font control
- Position settings

### Export

Exports to various formats.

**Formats:**
- `ASS` - Advanced SubStation Alpha (with animations)
- `SRT` - SubRip (basic)
- `VTT` - WebVTT (web)
- `JSON` - Full data export

## API Reference

### CaptionEngine

Main entry point for processing.

```python
from uace import CaptionEngine, ProcessingConfig

engine = CaptionEngine(
    config: Optional[ProcessingConfig] = None,
    verbose: bool = False
)
```

**Methods:**

```python
# Process video or audio
caption = engine.process(
    input_file: str,
    output: Optional[str] = None,
    **overrides
) -> Caption

# Process audio specifically
caption = engine.process_audio(
    audio_file: str,
    output: Optional[str] = None
) -> Caption

# Process video specifically  
caption = engine.process_video(
    video_file: str,
    output: Optional[str] = None
) -> Caption

# Export caption
engine.export(
    caption: Caption,
    output_path: str
) -> None
```

### ProcessingConfig

Complete configuration object.

```python
from uace import ProcessingConfig, CleaningMode

# Quick presets
config = ProcessingConfig.quick(
    cleaning=CleaningMode.BALANCED,
    style="viral_pop"
)

config = ProcessingConfig.fast()      # Speed priority
config = ProcessingConfig.accurate()  # Quality priority

# Full customization
config = ProcessingConfig()
config.transcription.model = "large"
config.transcription.diarization = True
config.cleaning.mode = CleaningMode.AGGRESSIVE
config.chunking.max_chars_per_line = 38
config.styling.preset = "neon"
```

**Sub-configurations:**

```python
# Transcription
config.transcription.preference  # EnginePreference
config.transcription.model       # Model size
config.transcription.language    # Language code
config.transcription.diarization # Enable speaker detection
config.transcription.gpu         # Use GPU

# Cleaning
config.cleaning.mode             # CleaningMode
config.cleaning.custom_fillers   # List of custom fillers
config.cleaning.language         # Language code
config.cleaning.dialect          # Dialect code

# Chunking
config.chunking.strategy         # ChunkingStrategy
config.chunking.max_chars_per_line
config.chunking.max_lines
config.chunking.max_duration

# Styling
config.styling.preset            # StylePresetName
config.styling.font_family
config.styling.font_size
config.styling.animation_style

# Export
config.export.format             # ExportFormat
config.export.output_path
```

### Caption

Container for caption data.

```python
class Caption:
    segments: List[CaptionSegment]
    language: str
    total_duration: float
    engine_used: str
    cleaning_mode: str
    style_preset: str
    word_count: int
    avg_confidence: float
```

**Methods:**

```python
# Get segment at specific time
segment = caption.segment_at(time: float)

# Compute statistics
caption.compute_stats()

# Duration
duration = caption.duration
```

### CaptionSegment

Single caption segment.

```python
class CaptionSegment:
    text: str                    # Processed text
    start: float                 # Start time (seconds)
    end: float                   # End time (seconds)
    confidence: float            # Confidence score (0-1)
    speaker: Optional[str]       # Speaker ID
    raw_text: Optional[str]      # Original text
    cleaning_applied: List[str]  # Cleaning operations
    words: List[Word]           # Word-level timing
```

**Properties:**

```python
duration = segment.duration
timespan = segment.timespan
has_word_timing = segment.has_words()
```

## Configuration

### Transcription Configuration

```python
config = ProcessingConfig()

# Model selection
config.transcription.model = "large"  # tiny, base, small, medium, large

# Engine preference
from uace.config import EnginePreference
config.transcription.preference = EnginePreference.ACCURACY

# Language
config.transcription.language = "en"  # ISO 639-1 code

# Features
config.transcription.diarization = True
config.transcription.word_timestamps = True

# Performance
config.transcription.gpu = True
config.transcription.compute_type = "float16"
config.transcription.batch_size = 16
```

### Cleaning Configuration

```python
config = ProcessingConfig()

# Mode
config.cleaning.mode = CleaningMode.BALANCED

# Custom fillers
config.cleaning.custom_fillers = [
    "basically",
    "literally",
    "at the end of the day"
]

# Options
config.cleaning.remove_fillers = True
config.cleaning.remove_sound_effects = True
config.cleaning.collapse_repetitions = True
config.cleaning.normalize_contractions = False

# Language
config.cleaning.language = "en"
config.cleaning.dialect = "us"
```

### Chunking Configuration

```python
config = ProcessingConfig()

# Strategy
config.chunking.strategy = ChunkingStrategy.SEMANTIC

# Constraints
config.chunking.max_chars_per_line = 42
config.chunking.max_lines = 2
config.chunking.max_duration = 7.0
config.chunking.min_duration = 0.5

# Reading speed
config.chunking.chars_per_second = 20.0

# Behavior
config.chunking.gap_threshold = 2.0
config.chunking.preserve_phrases = True
```

### Styling Configuration

```python
config = ProcessingConfig()

# Preset
config.styling.preset = "viral_pop"

# Font
config.styling.font_family = "Inter"
config.styling.font_size = 56
config.styling.font_weight = "bold"

# Colors (hex format)
config.styling.primary_color = "#FFFFFF"
config.styling.outline_color = "#000000"
config.styling.emphasis_color = "#FFD700"

# Effects
config.styling.outline_width = 3
config.styling.shadow = True
config.styling.glow = False

# Animation
config.styling.animation_style = "word_pop"
config.styling.animation_duration = 0.15
```

## Style Presets

### Available Presets

#### viral_pop
High-energy TikTok/Shorts style
- Word-by-word pop animation
- Bold white text
- Strong outline
- Center bottom position

```python
config.styling.preset = "viral_pop"
```

#### minimal
Clean, professional style
- Subtle fade animation
- Normal weight font
- Minimal outline
- Clean appearance

```python
config.styling.preset = "minimal"
```

#### karaoke
Music video style
- Color-fill timing
- Word-level synchronization
- Bold text
- Emphasis color changes

```python
config.styling.preset = "karaoke"
```

#### subtitle_classic
Traditional movie subtitles
- No animation
- Standard positioning
- Readable font
- Black background

```python
config.styling.preset = "subtitle_classic"
```

#### bounce
Energetic bounce animation
- Words bounce in
- Colorful outline
- Center screen
- High energy

```python
config.styling.preset = "bounce"
```

#### neon
Cyberpunk glow effect
- Cyan/pink colors
- Glow effect
- Scale animation
- Tech aesthetic

```python
config.styling.preset = "neon"
```

## Advanced Usage

### Speaker Diarization

```python
config = ProcessingConfig()
config.transcription.diarization = True
config.transcription.preference = EnginePreference.DIARIZATION

engine = CaptionEngine(config)
caption = engine.process("podcast.mp3")

# Access speaker information
for segment in caption.segments:
    print(f"[{segment.speaker}]: {segment.text}")
```

### Custom Cleaning Rules

```python
config = ProcessingConfig()

# Add custom fillers
config.cleaning.custom_fillers = [
    "you see",
    "if you will",
    "as it were"
]

# Fine-tune behavior
config.cleaning.preserve_emphasis = True
config.cleaning.fix_grammar = False

engine = CaptionEngine(config)
```

### Word-Level Access

```python
config = ProcessingConfig()
config.transcription.word_timestamps = True

engine = CaptionEngine(config)
caption = engine.process("video.mp4")

# Access word timing
for segment in caption.segments:
    if segment.has_words():
        for word in segment.words:
            print(f"{word.text}: {word.start:.2f}s")
```

### Multi-Language

```python
# Spanish
config = ProcessingConfig()
config.transcription.language = "es"
config.cleaning.language = "es"
config.cleaning.dialect = "mx"

engine = CaptionEngine(config)
caption = engine.process("video_spanish.mp4")
```

### Batch Processing

```python
config = ProcessingConfig.quick()
engine = CaptionEngine(config)

videos = ["video1.mp4", "video2.mp4", "video3.mp4"]

for video in videos:
    output = video.replace(".mp4", "_captions.ass")
    caption = engine.process(video, output=output)
    print(f"✓ {video}: {len(caption.segments)} segments")
```

## Performance Tuning

### Speed Optimization

```python
# Use fast preset
config = ProcessingConfig.fast()

# Or customize
config = ProcessingConfig()
config.transcription.model = "tiny"
config.transcription.word_timestamps = False
config.cleaning.mode = CleaningMode.LIGHT
```

### Quality Optimization

```python
# Use accurate preset
config = ProcessingConfig.accurate()

# Or customize
config = ProcessingConfig()
config.transcription.model = "large"
config.transcription.beam_size = 10
config.cleaning.mode = CleaningMode.BALANCED
```

### GPU Usage

```python
config = ProcessingConfig()
config.transcription.gpu = True
config.transcription.compute_type = "float16"  # or "int8" for even faster
```

### Batch Size

```python
config = ProcessingConfig()
config.transcription.batch_size = 32  # Higher = faster but more memory
```

## Troubleshooting

### No Engine Available

**Problem:** `No transcription engine available`

**Solution:**
```bash
pip install faster-whisper
# or
pip install "uace[whisper]"
```

### Out of Memory

**Problem:** CUDA out of memory

**Solutions:**
```python
# Use smaller model
config.transcription.model = "base"

# Use int8
config.transcription.compute_type = "int8"

# Reduce batch size
config.transcription.batch_size = 8

# Use CPU
config.transcription.gpu = False
```

### Slow Processing

**Solutions:**
```python
# Use GPU
config.transcription.gpu = True

# Use smaller model
config.transcription.model = "tiny"

# Disable word timestamps
config.transcription.word_timestamps = False
```

### Poor Accuracy

**Solutions:**
```python
# Use larger model
config.transcription.model = "large"

# Specify language
config.transcription.language = "en"

# Increase beam size
config.transcription.beam_size = 10
```

### Installation Issues

**Check system:**
```bash
uace doctor
uace doctor --check-gpu
```

**Check engines:**
```bash
uace engines
```

## Examples

See `examples.py` for comprehensive examples of all features.

## Support

- Documentation: https://docs.uace.dev
- Issues: https://github.com/uace/uace/issues
- Discussions: https://github.com/uace/uace/discussions
