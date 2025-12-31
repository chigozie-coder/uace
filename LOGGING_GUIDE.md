# Logging & Progress Tracking Guide

## 🔍 Full-Fledged Logging with TQDM

UACE v1.2.2 includes comprehensive logging with beautiful progress bars!

---

## 📊 Progress Bars

### Automatic Progress Tracking

```python
from uace import CaptionEngine, ProcessingConfig

config = ProcessingConfig()
engine = CaptionEngine(config, verbose=True)  # ✅ Enable verbose mode

caption = engine.process("video.mp4", "captions.ass")
```

**Output:**
```
15:30:42 - ✅ INFO - 🎬 Processing: video.mp4
Stage 1/5: Transcription
Overall Progress:  40%|████████░░| 40/100 [00:05<00:08, 8.5%/s] 🎤 Transcribing
15:30:47 - ✅ INFO - ✅ Transcribed 145 segments

Stage 2/5: Cleaning
Overall Progress:  60%|████████████░| 60/100 [00:07<00:04, 8.3%/s] 🧹 Cleaning  
15:30:49 - ✅ INFO - ✅ Cleaned 145 segments

Stage 3/5: Semantic Chunking
Overall Progress:  75%|██████████████░| 75/100 [00:08<00:02, 9.0%/s] ✂️  Chunking
15:30:50 - ✅ INFO - ✅ Created 138 chunks

Stage 4/5: Applying Style
Overall Progress:  85%|████████████████░| 85/100 [00:09<00:01, 8.8%/s] 🎨 Styling

Stage 5/5: Exporting
Overall Progress: 100%|████████████████████| 100/100 [00:10<00:00, 9.5%/s] 💾 Exporting
15:30:52 - ✅ INFO - ✅ Exported to: captions.ass

============================================================
🎉 Processing Complete!
⏱️  Time: 10.32s
📊 Segments: 138
📝 Words: 892
⏱️  Duration: 120.5s
============================================================
```

---

## 📝 Logging Levels

### Enable Different Logging Levels

```python
from uace import CaptionEngine, ProcessingConfig

# INFO level (default, verbose=True)
engine = CaptionEngine(verbose=True)

# DEBUG level (most detailed)
from uace.utils.logging import setup_logging
setup_logging(level="DEBUG", verbose=True)
engine = CaptionEngine()

# WARNING level (minimal output)
setup_logging(level="WARNING")
engine = CaptionEngine()
```

### Log to File

```python
from uace import CaptionEngine

engine = CaptionEngine(
    verbose=True,
    log_file="uace_processing.log"  # ✅ Save logs to file
)

caption = engine.process("video.mp4")
```

**File Output:** `uace_processing.log`
```
2024-12-30 15:30:42 - uace.engine - INFO - process_audio:245 - 🎬 Processing: video.mp4
2024-12-30 15:30:42 - uace.engine - DEBUG - _transcribe:312 - Loading transcription engine
2024-12-30 15:30:43 - uace.transcription - INFO - load_model:89 - Model loaded: base
2024-12-30 15:30:47 - uace.engine - INFO - _transcribe:325 - ✅ Transcribed 145 segments
...
```

---

## 🎨 Colored Output

Logging automatically uses colors in terminals:

- 🔍 **DEBUG** - Cyan
- ✅ **INFO** - Green  
- ⚠️ **WARNING** - Yellow
- ❌ **ERROR** - Red
- 🚨 **CRITICAL** - Magenta

### Disable Colors

```python
from uace.utils.logging import setup_logging

setup_logging(use_colors=False)
```

---

## 📊 One-Word Chunking (Word-by-Word Display)

Perfect for viral TikTok-style captions that display one word at a time!

### Enable One-Word Chunking

```python
from uace import CaptionEngine, ProcessingConfig

config = ProcessingConfig()

# One word at a time!
config.chunking.strategy = "word"  # ✅ Word-by-word chunking

# Use with word-pop animation
config.styling.preset = "big_bold"  # Or zoom_punch, viral_pop, etc.

engine = CaptionEngine(config, verbose=True)
caption = engine.process("video.mp4", "captions.ass")
```

### Result

Each word appears individually:

```
[00:00:00.00 - 00:00:00.50] This
[00:00:00.50 - 00:00:01.00] is
[00:00:01.00 - 00:00:01.50] viral
[00:00:01.50 - 00:00:02.00] style
[00:00:02.00 - 00:00:02.50] captions
```

### Chunking Strategies Comparison

```python
# ONE WORD (viral TikTok style)
config.chunking.strategy = "word"
# Result: One | word | at | a | time

# SEMANTIC (default, natural phrases)
config.chunking.strategy = "semantic"  
# Result: One word | at a time

# SENTENCE (full sentences)
config.chunking.strategy = "sentence"
# Result: One word at a time.

# WORD_COUNT (fixed number of words)
config.chunking.strategy = "word_count"
config.chunking.words_per_chunk = 3
# Result: One word at | a time

# FIXED_TIME (fixed duration chunks)
config.chunking.strategy = "fixed_time"
config.chunking.chunk_duration = 2.0  # 2 seconds
# Result: One word | at a time

# PUNCTUATION (break on punctuation)
config.chunking.strategy = "punctuation"
# Result: One word at a time.
```

---

## 🔥 Viral TikTok Complete Setup

One-word chunking + big bold style + progress tracking:

```python
from uace import CaptionEngine, ProcessingConfig

config = ProcessingConfig()

# Transcription
config.transcription.gpu = False
config.transcription.model = "base"

# ONE WORD CHUNKING (viral style!)
config.chunking.strategy = "word"  # ✅ One word at a time

# Big bold styling
config.styling.preset = "big_bold"  # Huge text
config.styling.font_size = 90  # Extra large
config.styling.animation_duration = 0.15  # Fast pop

# Aggressive cleaning
config.cleaning.mode = "aggressive"

# Create engine with progress bars
engine = CaptionEngine(config, verbose=True, log_file="process.log")

# Process with full progress tracking
caption = engine.process(
    "viral_video.mp4",
    "viral_captions.ass"
)

print(f"✅ Created {len(caption.segments)} one-word segments!")
```

**Output:**
```
15:45:10 - ✅ INFO - 🎬 Processing: viral_video.mp4
Stage 1/5: Transcription
Overall Progress:  40%|████████░░| 40/100 [00:03<00:05] 🎤 Transcribing
15:45:13 - ✅ INFO - ✅ Transcribed 89 words

Stage 2/5: Cleaning  
Overall Progress:  60%|████████████░| 60/100 [00:04<00:03] 🧹 Cleaning
15:45:14 - ✅ INFO - ✅ Cleaned 89 words

Stage 3/5: Word Chunking
Overall Progress:  75%|██████████████░| 75/100 [00:05<00:02] ✂️  Chunking
15:45:15 - ✅ INFO - ✅ Created 89 one-word chunks

Stage 4/5: Applying Style
Overall Progress:  85%|████████████████░| 85/100 [00:06<00:01] 🎨 Styling

Stage 5/5: Exporting
Overall Progress: 100%|████████████████████| 100/100 [00:07<00:00] 💾 Exporting
15:45:17 - ✅ INFO - ✅ Exported to: viral_captions.ass

============================================================
🎉 Processing Complete!
⏱️  Time: 7.15s
📊 Segments: 89 (one-word chunks)
📝 Words: 89
⏱️  Duration: 15.2s
============================================================

✅ Created 89 one-word segments!
```

---

## 📊 Advanced Logging Configuration

### Full Configuration

```python
from uace.utils.logging import setup_logging

logger = setup_logging(
    level="DEBUG",           # DEBUG, INFO, WARNING, ERROR, CRITICAL
    log_file="uace.log",    # Optional file output
    use_colors=True,        # Colored terminal output
    verbose=True            # Enable all debug messages
)

# Now all UACE operations will log
from uace import CaptionEngine
engine = CaptionEngine()
```

### Custom Logging in Your Code

```python
from uace.utils.logging import get_logger

logger = get_logger("my_script")

logger.debug("🔍 Debug message")
logger.info("✅ Info message")
logger.warning("⚠️  Warning message")
logger.error("❌ Error message")
logger.critical("🚨 Critical message")
```

---

## 🎯 Progress Tracking Features

### What Gets Tracked

1. **Stage Progress** - 5 stages with percentages
2. **Time Elapsed** - Real-time timing
3. **Segment Count** - Number of segments processed
4. **Word Count** - Total words processed
5. **Duration** - Video/audio duration
6. **Processing Speed** - Items/second

### Nested Progress Bars

For transcription, you'll see nested bars:

```
Stage 1/5: Transcription
Transcribing:  60%|████████░░| 60/100 [00:12<00:08, 12.5s/segment]
├─ Model Loading: ████████████████████ 100%
└─ Audio Processing: ████████████░░░░░░ 60%
```

---

## 🔄 Batch Processing with Progress

```python
from uace import CaptionEngine, ProcessingConfig
from tqdm import tqdm
import glob

config = ProcessingConfig()
config.chunking.strategy = "word"  # One word per chunk
config.styling.preset = "big_bold"

engine = CaptionEngine(config, verbose=True)

# Find all videos
videos = glob.glob("videos/*.mp4")

# Process with progress bar
for video in tqdm(videos, desc="Processing Videos"):
    output = video.replace(".mp4", "_captions.ass")
    caption = engine.process(video, output)
    print(f"✅ {video}: {len(caption.segments)} segments")
```

**Output:**
```
Processing Videos:  40%|████████░░| 2/5 [00:45<01:08, 22.5s/video]

15:50:10 - ✅ INFO - 🎬 Processing: videos/video1.mp4
Overall Progress: 100%|████████████████████| 100/100 [00:08<00:00]
✅ videos/video1.mp4: 156 segments

15:50:18 - ✅ INFO - 🎬 Processing: videos/video2.mp4
Overall Progress: 100%|████████████████████| 100/100 [00:12<00:00]
✅ videos/video2.mp4: 203 segments
```

---

## 🎨 Pretty Summary Reports

After processing, get a beautiful summary:

```python
caption = engine.process("video.mp4", "captions.ass")

# Automatic summary (when verbose=True)
# Or manually:
print(f"""
╔════════════════════════════════════════╗
║       UACE Processing Complete         ║
╠════════════════════════════════════════╣
║ File: {caption.metadata.get('source_file')}
║ Duration: {caption.duration:.1f}s
║ Segments: {len(caption.segments)}
║ Words: {caption.word_count}
║ Strategy: {config.chunking.strategy}
║ Style: {config.styling.preset}
╚════════════════════════════════════════╝
""")
```

---

## 🐛 Troubleshooting

### Progress bars not showing

```python
# Make sure verbose=True
engine = CaptionEngine(verbose=True)

# Or manually
from uace.utils.logging import setup_logging
setup_logging(level="INFO", verbose=True)
```

### Log file not created

```python
# Make sure directory exists
import os
os.makedirs("logs", exist_ok=True)

engine = CaptionEngine(log_file="logs/uace.log")
```

### Colors not showing

```python
# Force colors
from uace.utils.logging import setup_logging
setup_logging(use_colors=True)
```

---

## 📚 Complete Example

```python
from uace import CaptionEngine, ProcessingConfig
from uace.utils.logging import setup_logging

# Setup comprehensive logging
logger = setup_logging(
    level="INFO",
    log_file="processing.log",
    use_colors=True,
    verbose=True
)

# Configure for one-word viral style
config = ProcessingConfig()
config.transcription.gpu = False
config.transcription.model = "base"
config.chunking.strategy = "word"  # ✅ ONE WORD AT A TIME
config.styling.preset = "zoom_punch"
config.styling.font_size = 85
config.cleaning.mode = "aggressive"

# Create engine with verbose output
engine = CaptionEngine(
    config=config,
    verbose=True,
    log_file="processing.log"
)

# Process with full progress tracking
caption = engine.process(
    input_file="viral_video.mp4",
    output="viral_captions.ass"
)

# Results
print(f"""
✨ Processing Complete! ✨

📊 Statistics:
   - Segments: {len(caption.segments)} words
   - Duration: {caption.duration:.1f}s  
   - Words: {caption.word_count}
   - Avg Confidence: {caption.avg_confidence:.1%}

📂 Output:
   - Captions: viral_captions.ass
   - Log: processing.log

🎯 Settings:
   - Chunking: ONE WORD (viral style)
   - Style: {config.styling.preset}
   - Cleaning: {config.cleaning.mode}
""")
```

---

## ✅ Summary

### Logging Features
- ✅ Colored output with emojis
- ✅ TQDM progress bars
- ✅ File logging
- ✅ Multiple log levels
- ✅ Stage tracking
- ✅ Time tracking
- ✅ Statistics reporting

### One-Word Chunking
- ✅ `config.chunking.strategy = "word"`
- ✅ Perfect for viral TikTok/Instagram
- ✅ Syncs with word-level timestamps
- ✅ Works with all animation styles
- ✅ Follows voiceover exactly
