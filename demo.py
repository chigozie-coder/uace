#!/usr/bin/env python3
"""
UACE Quick Start Demo

Run this to see UACE in action (requires audio/video files).
"""

import sys
from pathlib import Path


def check_installation():
    """Check if UACE is properly installed."""
    print("=" * 60)
    print("UACE Quick Start Demo")
    print("=" * 60)
    print()
    
    try:
        import uace
        print(f"✓ UACE installed (version {uace.__version__})")
    except ImportError:
        print("✗ UACE not installed")
        print("  Install with: pip install -e .")
        sys.exit(1)
    
    # Check engines
    from uace.engines.transcription import EngineSelector
    engines = EngineSelector.get_available_engines()
    
    if engines:
        print(f"✓ Transcription engines available: {', '.join(engines)}")
    else:
        print("✗ No transcription engines available")
        print("  Install with: pip install faster-whisper")
        sys.exit(1)
    
    print()


def demo_quick_caption():
    """Demo 1: Quick caption generation."""
    print("Demo 1: Quick Caption Generation")
    print("-" * 60)
    
    from uace import CaptionEngine
    
    code = '''
    from uace import CaptionEngine
    
    engine = CaptionEngine()
    caption = engine.process("video.mp4", output="captions.ass")
    
    print(f"Generated {len(caption.segments)} segments")
    '''
    
    print("Code:")
    print(code)
    print("This is the simplest usage - just two lines!")
    print()


def demo_viral_style():
    """Demo 2: Viral content style."""
    print("Demo 2: Viral Content (TikTok/Shorts)")
    print("-" * 60)
    
    code = '''
    from uace import CaptionEngine, ProcessingConfig, CleaningMode
    
    config = ProcessingConfig.quick(
        cleaning=CleaningMode.AGGRESSIVE,
        style="viral_pop"
    )
    
    engine = CaptionEngine(config, verbose=True)
    caption = engine.process("short_video.mp4")
    '''
    
    print("Code:")
    print(code)
    print("Aggressive cleaning removes fillers for clean short-form content.")
    print("Viral pop style adds word-by-word animations.")
    print()


def demo_podcast_diarization():
    """Demo 3: Podcast with speaker detection."""
    print("Demo 3: Podcast with Speaker Detection")
    print("-" * 60)
    
    code = '''
    from uace import CaptionEngine, ProcessingConfig
    from uace.config import EnginePreference
    
    config = ProcessingConfig()
    config.transcription.diarization = True
    config.transcription.model = "large"
    config.transcription.preference = EnginePreference.DIARIZATION
    
    engine = CaptionEngine(config, verbose=True)
    caption = engine.process_audio("podcast.mp3")
    
    # Print speaker timeline
    for segment in caption.segments:
        print(f"[{segment.speaker}]: {segment.text}")
    '''
    
    print("Code:")
    print(code)
    print("Automatically detects and labels different speakers.")
    print("Perfect for interviews and multi-speaker content.")
    print()


def demo_cli_usage():
    """Demo 4: CLI usage."""
    print("Demo 4: Command Line Usage")
    print("-" * 60)
    
    examples = [
        ("Basic", "uace process video.mp4"),
        ("Custom style", "uace process video.mp4 --style viral_pop --cleaning aggressive"),
        ("Diarization", "uace process podcast.mp3 --diarization --model large"),
        ("SRT export", "uace process video.mp4 --format srt -o captions.srt"),
        ("List styles", "uace styles"),
        ("System check", "uace doctor"),
    ]
    
    for name, cmd in examples:
        print(f"{name:15} {cmd}")
    
    print()


def demo_custom_cleaning():
    """Demo 5: Custom cleaning rules."""
    print("Demo 5: Custom Cleaning Rules")
    print("-" * 60)
    
    code = '''
    from uace import CaptionEngine, ProcessingConfig
    
    config = ProcessingConfig()
    config.cleaning.custom_fillers = [
        "basically",
        "literally",
        "at the end of the day"
    ]
    config.cleaning.collapse_repetitions = True
    
    engine = CaptionEngine(config)
    caption = engine.process("video.mp4")
    
    # Show what was cleaned
    for segment in caption.segments[:3]:
        print(f"Original: {segment.raw_text}")
        print(f"Cleaned:  {segment.text}")
    '''
    
    print("Code:")
    print(code)
    print("Add your own filler words and customize cleaning behavior.")
    print()


def demo_word_timing():
    """Demo 6: Word-level timing access."""
    print("Demo 6: Word-Level Timing")
    print("-" * 60)
    
    code = '''
    from uace import CaptionEngine, ProcessingConfig
    
    config = ProcessingConfig()
    config.transcription.word_timestamps = True
    
    engine = CaptionEngine(config)
    caption = engine.process("video.mp4")
    
    # Access word-by-word timing
    for segment in caption.segments:
        if segment.has_words():
            for word in segment.words:
                print(f"{word.text}: {word.start:.2f}s - {word.end:.2f}s")
    '''
    
    print("Code:")
    print(code)
    print("Get precise timing for every word - perfect for karaoke effects.")
    print()


def demo_styles():
    """Demo 7: Available styles."""
    print("Demo 7: Available Style Presets")
    print("-" * 60)
    
    from uace.styling.presets import PRESET_REGISTRY
    
    for name, preset in PRESET_REGISTRY.items():
        print(f"  {name:20} {preset.description}")
    
    print()
    print("Use with: config.styling.preset = 'viral_pop'")
    print()


def demo_batch_processing():
    """Demo 8: Batch processing."""
    print("Demo 8: Batch Processing")
    print("-" * 60)
    
    code = '''
    from uace import CaptionEngine, ProcessingConfig
    
    config = ProcessingConfig.fast()  # Speed optimized
    engine = CaptionEngine(config)
    
    videos = ["video1.mp4", "video2.mp4", "video3.mp4"]
    
    for video in videos:
        output = video.replace(".mp4", "_captions.ass")
        try:
            caption = engine.process(video, output=output)
            print(f"✓ {video}: {len(caption.segments)} segments")
        except Exception as e:
            print(f"✗ {video}: {e}")
    '''
    
    print("Code:")
    print(code)
    print("Process multiple files efficiently with the same configuration.")
    print()


def demo_performance_tuning():
    """Demo 9: Performance tuning."""
    print("Demo 9: Performance Tuning")
    print("-" * 60)
    
    print("Speed Priority:")
    code_fast = '''
    config = ProcessingConfig.fast()
    # Uses: tiny model, light cleaning, no word timestamps
    '''
    print(code_fast)
    
    print("Quality Priority:")
    code_quality = '''
    config = ProcessingConfig.accurate()
    # Uses: large model, balanced cleaning, max beam size
    '''
    print(code_quality)
    
    print("\nCustom tuning:")
    code_custom = '''
    config = ProcessingConfig()
    config.transcription.model = "base"      # Good balance
    config.transcription.gpu = True           # Use GPU
    config.transcription.compute_type = "int8"  # Faster
    config.transcription.batch_size = 32     # Larger batches
    '''
    print(code_custom)
    print()


def print_next_steps():
    """Print next steps."""
    print("=" * 60)
    print("Next Steps")
    print("=" * 60)
    print()
    print("1. Read the documentation:")
    print("   - README.md for overview")
    print("   - DOCS.md for detailed API reference")
    print("   - examples.py for 10+ complete examples")
    print()
    print("2. Try the CLI:")
    print("   uace process video.mp4")
    print("   uace styles")
    print("   uace doctor")
    print()
    print("3. Explore the code:")
    print("   - src/uace/engine.py - Main pipeline")
    print("   - src/uace/cleaning/engine.py - Cleaning logic")
    print("   - src/uace/styling/presets.py - Style presets")
    print()
    print("4. Run tests:")
    print("   pytest tests/")
    print()
    print("=" * 60)
    print("UACE - Transform speech into clarity")
    print("=" * 60)
    print()


def main():
    """Run all demos."""
    check_installation()
    
    demos = [
        demo_quick_caption,
        demo_viral_style,
        demo_podcast_diarization,
        demo_cli_usage,
        demo_custom_cleaning,
        demo_word_timing,
        demo_styles,
        demo_batch_processing,
        demo_performance_tuning,
    ]
    
    for demo in demos:
        demo()
    
    print_next_steps()


if __name__ == "__main__":
    main()
