# UACE Style Presets Guide

## 🎨 Complete Style Collection (30+ Presets!)

### Quick Start

```python
from uace import CaptionEngine, ProcessingConfig

# Use any preset
config = ProcessingConfig.quick(style="big_bold")
engine = CaptionEngine(config)
```

---

## 📱 Viral/Social Media Styles

Perfect for TikTok, Instagram Reels, YouTube Shorts

### viral_pop ⭐
**The Original**
- Word-by-word pop animation
- Bold white text, black outline
- Center bottom position
- **Best for:** Short-form content, general use

### big_bold 🔥
**MAXIMUM IMPACT**
- HUGE 72px font size
- Zooms in one word at a time
- Center screen, fills the frame
- **Best for:** Dramatic reveals, announcements

### zoom_punch 💥
**EXPLOSIVE ENERGY**
- Each word PUNCHES onto screen
- Yellow text, aggressive animation
- Fast pacing (0.06s delay)
- **Best for:** Hype content, reactions, gaming

### wave_motion 🌊
**SMOOTH FLOW**
- Smooth wave flowing through words
- Cyan blue aesthetic
- Gentle, mesmerizing motion
- **Best for:** Chill content, transitions, storytelling

### elastic_bounce 🎈
**PLAYFUL & FUN**
- Elastic bounce with overshoot
- Hot pink color
- Rubber band effect
- **Best for:** Fun content, kids videos, playful vlogs

### earthquake 🔴
**VIOLENT SHAKE**
- Intense shake animation
- Orange-red aggressive colors
- Words appear with earthquake effect
- **Best for:** Intense moments, reactions, dramatic reveals

---

## 🎵 Music/Rhythm Styles

Sync with audio beats and rhythm

### karaoke 🎤
**CLASSIC MUSIC VIDEO**
- Color-fill timing effect
- Word-by-word highlight
- Perfect sync with vocals
- **Best for:** Music videos, lyric videos, sing-alongs

### beat_pulse 💓
**PULSE TO THE BEAT**
- Pulses with rhythm
- Magenta and cyan colors
- 0.08s beat timing
- **Best for:** EDM, hip-hop, energetic music

### sound_wave 📊
**VISUAL AUDIO**
- Wave animation synced to sound
- Lime green with glow
- Audio waveform aesthetic
- **Best for:** Music production, DJ content, electronic music

### rhythm_bounce 🎶
**BOUNCE TO RHYTHM**
- Bounces in rhythm
- Pink and gold colors
- Music video style
- **Best for:** Dance videos, music content, rhythmic content

---

## 🎨 Creative/Artistic Styles

Unique aesthetics for creative content

### neon 💎
**CYBERPUNK GLOW**
- Cyan and pink neon colors
- Intense glow effect
- Tech aesthetic
- **Best for:** Tech content, gaming, futuristic themes

### glitch ⚡
**DIGITAL CHAOS**
- RGB split glitch effect
- Rapid flashing
- Cyberpunk aesthetic
- **Best for:** Tech, gaming, edgy content, transitions

### retro_vhs 📼
**80s NOSTALGIA**
- Pink and purple VHS colors
- Vintage font
- Retro fade animation
- **Best for:** Retro content, throwback videos, nostalgic themes

### hologram 🔮
**FUTURISTIC PROJECTION**
- Cyan hologram effect
- Floating animation
- Transparent glow
- **Best for:** Sci-fi, tech demos, futuristic content

### graffiti 🎨
**STREET ART**
- Bold orange and gold
- Urban marker font
- Street style
- **Best for:** Hip-hop, urban content, art videos

### handwritten ✍️
**PERSONAL TOUCH**
- Handwriting font
- Typewriter animation
- Dark gray on light
- **Best for:** Personal stories, journals, intimate content

---

## 🎬 Cinematic Styles

Professional film-quality captions

### minimal 📝
**CLEAN & PROFESSIONAL**
- Simple fade animation
- Normal weight font
- Minimal outline
- **Best for:** Corporate, vlogs, professional content

### subtitle_classic 🎞️
**TRADITIONAL SUBTITLES**
- No animation
- Standard positioning
- Black background bar
- **Best for:** Movies, documentaries, interviews

### cinematic_fade 🎭
**ELEGANT FILM**
- Slow elegant fade
- Italic serif font
- Bottom centered
- **Best for:** Film subtitles, dramatic content, art films

### noir_typewriter 🕵️
**DETECTIVE STORY**
- Typewriter monospace font
- Top-left position
- Character-by-character typing
- **Best for:** Mystery, detective stories, old film aesthetic

---

## 💫 Animation Styles

Dynamic motion effects

### bounce ⚽
**ENERGETIC BOUNCE**
- Vertical bounce motion
- Colorful outline
- Playful energy
- **Best for:** Kids content, fun videos, energetic content

### slide_up ⬆️
**ELEGANT RISE**
- Slides up from bottom
- Smooth entry
- Professional feel
- **Best for:** Professional content, presentations

### slide_down ⬇️
**ELEGANT DESCENT**
- Slides down from top
- Top-aligned
- Graceful entry
- **Best for:** News-style, formal content

### flip_in 🔄
**3D FLIP**
- 3D flip animation
- Purple and red
- Dynamic entrance
- **Best for:** Reveals, transitions, dynamic content

### rotate_in 🌀
**SPINNING ENTRANCE**
- Rotate and zoom in
- Blue and green
- Spiral effect
- **Best for:** Transitions, intros, dynamic content

### blur_focus 📷
**CAMERA FOCUS**
- Blur to sharp focus
- Cinematic depth of field
- DSLR camera effect
- **Best for:** Cinematic content, dramatic reveals

### typewriter ⌨️
**TYPING EFFECT**
- Character-by-character
- Classic typewriter sound sync
- Courier font
- **Best for:** Writing content, stories, vintage aesthetic

---

## 🌐 3D/Perspective Styles

Depth and dimension

### perspective_3d 📐
**DRAMATIC TILT**
- 3D perspective tilt
- Gold with depth
- Rotation effect
- **Best for:** Modern content, tech, architectural

### depth_blur 🎥
**DEPTH OF FIELD**
- Bokeh-style blur
- Focus effect
- Cinematic depth
- **Best for:** Cinematic content, artistic videos

### floating ☁️
**DREAMY MOTION**
- Gentle floating animation
- Sky blue colors
- Ethereal movement
- **Best for:** Calm content, meditation, dreamy aesthetics

---

## ✨ Special Effects

Dramatic visual effects

### fire 🔥
**BURNING EFFECT**
- Orange-red flames
- Intense glow
- Pulsing animation
- **Best for:** Intense content, cooking, energy

### lightning ⚡
**ELECTRIC FLASH**
- White with cyan
- Glitch-style flash
- Electric energy
- **Best for:** Power moments, reveals, energy content

### particles ✨
**MAGICAL EXPLOSION**
- Gold particle effect
- Scale animation
- Magical appearance
- **Best for:** Magic reveals, special moments, celebrations

### spotlight 🎭
**STAGE REVEAL**
- Dramatic spotlight
- Fade reveal
- Performance lighting
- **Best for:** Performance content, reveals, dramatic moments

---

## 🎯 GPU Control

**YES! GPU can be disabled:**

```python
from uace import CaptionEngine, ProcessingConfig

config = ProcessingConfig()
config.transcription.gpu = False  # ✅ Run on CPU
config.transcription.compute_type = "int8"  # Faster CPU inference

engine = CaptionEngine(config)
caption = engine.process("video.mp4")
```

**CPU Optimization:**
```python
# Fast CPU mode
config = ProcessingConfig.fast()
config.transcription.gpu = False
config.transcription.model = "tiny"  # Fastest
```

---

## 🎨 Extreme Customization

**Override ANY style parameter:**

```python
config = ProcessingConfig()

# Start with a preset
config.styling.preset = "big_bold"

# Then customize everything
config.styling.font_size = 80  # Even bigger!
config.styling.primary_color = "#FF00FF"  # Magenta
config.styling.outline_width = 8  # Thicker outline
config.styling.glow = True  # Add glow
config.styling.glow_intensity = 15  # Max glow
config.styling.animation_duration = 0.3  # Slower
config.styling.scale_overshoot = 1.5  # More overshoot
config.styling.rotation_start = -45  # Rotate in from -45°
config.styling.rotation_end = 0  # To 0°

# 3D effects
config.styling.perspective = True
config.styling.rotation_y = 20  # 3D tilt

# Gradients
config.styling.gradient_enabled = True
config.styling.gradient_start = "#FF00FF"
config.styling.gradient_end = "#00FFFF"
config.styling.gradient_angle = 45

engine = CaptionEngine(config)
```

**Custom positioning:**
```python
config.styling.alignment = "left"  # left, center, right
config.styling.vertical_position = "top"  # top, middle, bottom
config.styling.margin_left = 50
config.styling.margin_top = 50
config.styling.max_width_percent = 80
```

**Typography control:**
```python
config.styling.font_family = "Impact"
config.styling.font_weight = "black"  # Extra bold
config.styling.font_italic = True
config.styling.letter_spacing = 5  # Space out letters
config.styling.line_spacing = 1.5  # More line space
config.styling.text_transform = "uppercase"  # ALL CAPS
```

**Effects control:**
```python
config.styling.shadow = True
config.styling.shadow_depth = 10
config.styling.shadow_offset_x = 5
config.styling.shadow_offset_y = 5
config.styling.shadow_color = "#FF0000"

config.styling.blur = 2  # Slight blur
config.styling.opacity = 0.9  # Slight transparency
```

---

## 🚀 Usage Examples

```bash
# CLI - Try any style
uace process video.mp4 --style big_bold
uace process video.mp4 --style zoom_punch
uace process video.mp4 --style fire
uace process video.mp4 --style hologram

# Without GPU
uace process video.mp4 --no-gpu --style earthquake
```

```python
# Python - Mix and match
from uace import CaptionEngine, ProcessingConfig

# Earthquake style without GPU
config = ProcessingConfig.quick(style="earthquake")
config.transcription.gpu = False
engine = CaptionEngine(config)

# Big bold with custom colors
config = ProcessingConfig.quick(style="big_bold")
config.styling.primary_color = "#00FF00"  # Green
config.styling.emphasis_color = "#FF0000"  # Red emphasis
engine = CaptionEngine(config)
```

---

## 📊 Style Selection Guide

| Content Type | Recommended Styles |
|--------------|-------------------|
| TikTok/Shorts | big_bold, zoom_punch, elastic_bounce |
| YouTube | viral_pop, wave_motion, minimal |
| Music Videos | karaoke, beat_pulse, sound_wave |
| Gaming | glitch, lightning, earthquake |
| Vlogs | minimal, handwritten, wave_motion |
| Corporate | minimal, cinematic_fade, subtitle_classic |
| Art/Creative | neon, hologram, retro_vhs |
| Kids Content | elastic_bounce, graffiti, particles |
| Documentary | subtitle_classic, cinematic_fade, minimal |
| Horror | noir_typewriter, glitch, fire |

---

## 💡 Pro Tips

1. **Layer effects** - Combine glow + perspective + rotation
2. **Sync animations** - Match animation_duration to your content's pace
3. **Use emphasis** - auto_emphasis=True highlights important words
4. **Test on mobile** - Most viewers watch on phones
5. **Match your brand** - Customize colors to your brand palette
6. **CPU mode works** - Don't need GPU for great results

**Total: 30+ Presets + Infinite Customization!** 🎉
