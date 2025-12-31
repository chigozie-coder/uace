# Speaker Diarization & Intelligent Labeling Guide

## 🎙️ Highly Intelligent Speaker Labeling

UACE includes a **creative speaker identification system** that goes beyond simple "Speaker 1, Speaker 2" labels!

---

## ✨ Features

### 🤖 Automatic Role Detection
- **Host** - Identifies the main speaker (most speaking time)
- **Guests** - Identifies secondary speakers
- **Co-host** - Detects equal conversation partners
- **Narrator** - Single speaker scenarios

### 🎨 Visual Distinction
- **Color Coding** - Each speaker gets a unique color
- **Emoji Assignment** - Visual icons for quick identification
- **Position Control** - Host at bottom, guests at top
- **Custom Styling** - Speaker-specific caption styles

### 🧠 Smart Analysis
- Speaking time analysis
- Segment counting
- Confidence scoring
- Pattern recognition

---

## 🚀 Quick Start

### Basic Usage

```python
from uace import CaptionEngine, ProcessingConfig

config = ProcessingConfig()

# Enable diarization
config.transcription.diarization = True

# Create engine
engine = CaptionEngine(config, verbose=True)

# Process (speakers will be auto-detected and labeled)
caption = engine.process("podcast.mp3", "captions.ass")

# Speakers are automatically labeled!
# Result: "Host", "Guest 1", "Guest 2", etc.
```

### Advanced Labeling

```python
from uace import CaptionEngine, ProcessingConfig
from uace.diarization import SpeakerLabeler

config = ProcessingConfig()
config.transcription.diarization = True

engine = CaptionEngine(config)

# Process with diarization
caption = engine.process("podcast.mp3")

# Apply intelligent labeling
labeler = SpeakerLabeler(
    style='vibrant',      # Color palette
    context='podcast',    # Context for emojis
    auto_detect_roles=True  # Smart role detection
)

labeled_segments = labeler.label_segments(caption.segments)

# Update caption with labeled segments
caption.segments = labeled_segments

# Export
engine.export(caption, "captions.ass")

# Print summary
print(labeler.get_speaker_summary())
```

**Output:**
```
============================================================
SPEAKER SUMMARY
============================================================
🎙️ Host
   Segments: 145
   Duration: 320.5s
   Confidence: 92.3%
   Color: #2E86DE

🎤 Guest 1
   Segments: 89
   Duration: 180.2s
   Confidence: 89.7%
   Color: #EE5A6F

🗣️ Guest 2
   Segments: 56
   Duration: 95.8s
   Confidence: 91.1%
   Color: #10AC84

============================================================
```

---

## 🎨 Customization Options

### Style Presets

```python
from uace.diarization import SpeakerLabeler

# Professional colors
labeler = SpeakerLabeler(
    style='professional',  # Blue, red, green tones
    context='interview'
)

# Vibrant colors
labeler = SpeakerLabeler(
    style='vibrant',  # Bright, energetic
    context='podcast'
)

# Pastel colors
labeler = SpeakerLabeler(
    style='pastel',  # Soft, gentle
    context='educational'
)

# Neon colors
labeler = SpeakerLabeler(
    style='neon',  # Bold, high contrast
    context='casual'
)

# Warm colors
labeler = SpeakerLabeler(
    style='warm',  # Reds, oranges, yellows
    context='casual'
)

# Cool colors
labeler = SpeakerLabeler(
    style='cool',  # Blues, greens, purples
    context='professional'
)
```

### Context-Based Emojis

```python
# Professional setting
labeler = SpeakerLabeler(context='professional')
# Emojis: 👔 💼 🎯 📊 🎤 🎙️ 👨‍💼 👩‍💼

# Podcast setting
labeler = SpeakerLabeler(context='podcast')
# Emojis: 🎙️ 🎧 🎤 📻 🔊 🎵 🎶 🗣️

# Educational setting
labeler = SpeakerLabeler(context='educational')
# Emojis: 👨‍🏫 👩‍🏫 📚 🎓 ✏️ 📖 🧑‍🎓 👨‍🔬

# Interview setting
labeler = SpeakerLabeler(context='interview')
# Emojis: 💬 🗨️ 💭 🎤 🎙️ 📝 ✍️ 🤝

# Casual setting
labeler = SpeakerLabeler(context='casual')
# Emojis: 😊 🙂 😄 🤗 👋 ✨ 🎈 🌟
```

### Custom Labels

```python
from uace.diarization import SpeakerLabeler

labeler = SpeakerLabeler()

# Define custom labels
custom_labels = {
    'SPEAKER_00': 'Alex (Host)',
    'SPEAKER_01': 'Dr. Smith (Expert)',
    'SPEAKER_02': 'Sarah (Guest)'
}

# Apply custom labels
labeled_segments = labeler.label_segments(
    caption.segments,
    custom_labels=custom_labels
)
```

---

## 🎯 Automatic Role Detection

### How It Works

The system analyzes:
1. **Speaking Time** - Who talks the most?
2. **Turn Taking** - Who initiates conversations?
3. **Segment Distribution** - How is speaking balanced?

### Role Assignment Logic

**1 Speaker:**
```
Narrator
```

**2 Speakers:**
```
Primary (60%+ time)  → Host
Secondary           → Guest

Equal time          → Speaker A, Speaker B
```

**3+ Speakers:**
```
Most time           → Host
Second most         → Co-host
Others              → Guest 1, Guest 2, etc.
```

---

## 🎨 Visual Styling

### Speaker-Specific Styles

```python
from uace.diarization import SpeakerStyler

# Create speaker-specific styles
base_style = {
    'font_size': 52,
    'animation': 'fade',
    'outline_width': 3
}

speaker_styles = SpeakerStyler.create_speaker_styles(
    labeler.speaker_profiles,
    base_style
)

# Apply to segments
for segment in caption.segments:
    speaker_id = segment.metadata.get('speaker_id')
    if speaker_id in speaker_styles:
        # Apply speaker-specific styling
        style = speaker_styles[speaker_id]
        segment.style = style
```

### Position by Role

```python
# Automatic positioning:
# - Host/Narrator → Bottom center
# - Guests → Top center
# - This creates visual distinction!

# Customize:
config.styling.position_by_speaker = True
config.styling.host_position = 'bottom'
config.styling.guest_position = 'top'
```

---

## 🔥 Complete Examples

### Example 1: Podcast with Auto-Detection

```python
from uace import CaptionEngine, ProcessingConfig
from uace.diarization import SpeakerLabeler

# Configure
config = ProcessingConfig()
config.transcription.diarization = True
config.transcription.model = "medium"
config.styling.preset = "minimal"

# Process
engine = CaptionEngine(config, verbose=True)
caption = engine.process("podcast.mp3")

# Apply intelligent labeling
labeler = SpeakerLabeler(
    style='professional',
    context='podcast',
    auto_detect_roles=True
)

caption.segments = labeler.label_segments(caption.segments)

# Export with speaker labels
engine.export(caption, "podcast_captions.ass")

# Print speaker summary
print(labeler.get_speaker_summary())
```

### Example 2: Interview with Custom Labels

```python
from uace import CaptionEngine, ProcessingConfig
from uace.diarization import SpeakerLabeler

config = ProcessingConfig()
config.transcription.diarization = True

engine = CaptionEngine(config)
caption = engine.process("interview.mp4")

# Custom labels
labeler = SpeakerLabeler(
    style='vibrant',
    context='interview'
)

custom_labels = {
    'SPEAKER_00': 'Interviewer',
    'SPEAKER_01': 'CEO (John Smith)'
}

caption.segments = labeler.label_segments(
    caption.segments,
    custom_labels=custom_labels
)

engine.export(caption, "interview_captions.ass")
```

### Example 3: Multi-Speaker Panel

```python
from uace import CaptionEngine, ProcessingConfig
from uace.diarization import SpeakerLabeler

config = ProcessingConfig()
config.transcription.diarization = True

engine = CaptionEngine(config, verbose=True)
caption = engine.process("panel_discussion.mp4")

# Auto-detect with neon colors
labeler = SpeakerLabeler(
    style='neon',
    context='professional',
    auto_detect_roles=True
)

caption.segments = labeler.label_segments(caption.segments)

# See results
print(labeler.get_speaker_summary())

# Export
engine.export(caption, "panel_captions.ass")
```

### Example 4: Educational Lecture

```python
from uace import CaptionEngine, ProcessingConfig
from uace.diarization import SpeakerLabeler

config = ProcessingConfig()
config.transcription.diarization = True

engine = CaptionEngine(config)
caption = engine.process("lecture.mp4")

labeler = SpeakerLabeler(
    style='pastel',
    context='educational',
    auto_detect_roles=False  # Use simple labels
)

# Will label as "Speaker 1", "Speaker 2", etc.
caption.segments = labeler.label_segments(caption.segments)

engine.export(caption, "lecture_captions.ass")
```

---

## 🎨 Color Palettes

### Vibrant
```python
Colors: #FF6B6B, #4ECDC4, #45B7D1, #FFA07A, #98D8C8, #F7DC6F
Use for: Energetic content, podcasts, casual videos
```

### Professional
```python
Colors: #2E86DE, #EE5A6F, #10AC84, #F79F1F, #5F27CD, #00D2D3
Use for: Business, interviews, corporate content
```

### Pastel
```python
Colors: #FFB3BA, #BAFFC9, #BAE1FF, #FFFFBA, #FFDFBA, #E0BBE4
Use for: Gentle content, educational, soothing
```

### Neon
```python
Colors: #FF00FF, #00FFFF, #FFFF00, #FF0080, #00FF80, #8000FF
Use for: High-energy, gaming, youth content
```

### Warm
```python
Colors: #FF6B6B, #FFA07A, #FFD93D, #F8B500, #FF8C42, #FF4E50
Use for: Friendly, inviting, cozy content
```

### Cool
```python
Colors: #4ECDC4, #45B7D1, #5F9EA0, #6C5CE7, #74B9FF, #00B894
Use for: Calm, professional, tech content
```

---

## 📊 Speaker Metadata

Each labeled segment includes rich metadata:

```python
segment.metadata = {
    'speaker_id': 'SPEAKER_00',           # Original ID
    'speaker_label': 'Host',              # Creative label
    'speaker_color': '#2E86DE',           # Assigned color
    'speaker_emoji': '🎙️',               # Visual icon
    'speaker_role': 'host'                # Detected role
}
```

---

## 🔧 Advanced Features

### Generate Custom Colors

```python
from uace.diarization import generate_speaker_colors

# Generate 5 distinct colors
colors = generate_speaker_colors(
    num_speakers=5,
    palette='vibrant'
)

print(colors)
# ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
```

### Get Contrast Colors

```python
from uace.diarization import SpeakerStyler

# Get black or white for contrast
outline = SpeakerStyler._get_contrast_color('#FF6B6B')
# Returns: '#FFFFFF' (white for contrast with red)

outline = SpeakerStyler._get_contrast_color('#FFFF00')
# Returns: '#000000' (black for contrast with yellow)
```

---

## 🎯 Best Practices

### 1. Choose Appropriate Model
```python
# For better diarization, use medium or large model
config.transcription.model = "medium"  # Better accuracy
```

### 2. Match Style to Content
```python
# Podcast → Professional/Podcast context
# Interview → Professional/Interview context
# Casual → Casual/Vibrant style
# Educational → Pastel/Educational context
```

### 3. Use Custom Labels for Known Speakers
```python
# If you know the speakers, label them!
custom_labels = {
    'SPEAKER_00': 'Host Name',
    'SPEAKER_01': 'Guest Name'
}
```

### 4. Preview Speaker Summary
```python
# Always check the summary first
print(labeler.get_speaker_summary())
```

---

## 📝 Integration with Styling

### Apply Speaker Colors to Captions

```python
from uace import CaptionEngine, ProcessingConfig
from uace.diarization import SpeakerLabeler

config = ProcessingConfig()
config.transcription.diarization = True
config.styling.preset = "minimal"

engine = CaptionEngine(config)
caption = engine.process("podcast.mp3")

# Label speakers
labeler = SpeakerLabeler(style='vibrant')
caption.segments = labeler.label_segments(caption.segments)

# Update styling to use speaker colors
for segment in caption.segments:
    if 'speaker_color' in segment.metadata:
        # Each speaker gets their own color!
        segment.style_override = {
            'primary_color': segment.metadata['speaker_color']
        }

engine.export(caption, "colorful_podcast.ass")
```

---

## ✅ Summary

### What You Get

1. **Automatic Role Detection**
   - Host, Guest, Co-host, Narrator
   - Based on speaking patterns

2. **Creative Labels**
   - Not just "Speaker 1"
   - Context-aware naming

3. **Visual Distinction**
   - Unique colors per speaker
   - Emoji icons
   - Position control

4. **Rich Metadata**
   - Speaking time
   - Segment count
   - Confidence scores

5. **6 Color Palettes**
   - Vibrant, Professional, Pastel
   - Neon, Warm, Cool

6. **5 Context Sets**
   - Professional, Podcast, Educational
   - Interview, Casual

### Usage Pattern

```python
# 1. Enable diarization
config.transcription.diarization = True

# 2. Process audio
caption = engine.process("audio.mp3")

# 3. Apply intelligent labeling
labeler = SpeakerLabeler(style='vibrant', context='podcast')
caption.segments = labeler.label_segments(caption.segments)

# 4. Export
engine.export(caption, "captions.ass")
```
