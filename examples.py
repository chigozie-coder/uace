"""
UACE Examples

Demonstrates various use cases and capabilities.
"""

from uace import CaptionEngine, ProcessingConfig, CleaningMode
from uace.config import EnginePreference


def example_1_quick_start():
    """
    Example 1: Quick Start
    
    Simplest possible usage with defaults.
    """
    print("\n=== Example 1: Quick Start ===\n")
    
    engine = CaptionEngine()
    caption = engine.process("video.mp4", output="captions.ass")
    
    print(f"Generated {len(caption.segments)} segments")
    print(f"Total duration: {caption.duration:.2f}s")


def example_2_viral_content():
    """
    Example 2: Viral Content (TikTok/Shorts)
    
    Aggressive cleaning with viral pop style.
    """
    print("\n=== Example 2: Viral Content ===\n")
    
    config = ProcessingConfig.quick(
        cleaning=CleaningMode.AGGRESSIVE,
        style="viral_pop"
    )
    
    # Additional customization
    config.chunking.max_chars_per_line = 38  # Shorter for mobile
    config.styling.font_size = 60  # Larger for impact
    
    engine = CaptionEngine(config, verbose=True)
    caption = engine.process("short_video.mp4")
    
    # Export
    engine.export(caption, "viral_captions.ass")


def example_3_podcast_diarization():
    """
    Example 3: Podcast with Speaker Diarization
    
    Multi-speaker detection and attribution.
    """
    print("\n=== Example 3: Podcast Diarization ===\n")
    
    config = ProcessingConfig()
    config.transcription.diarization = True
    config.transcription.model = "large"
    config.transcription.preference = EnginePreference.DIARIZATION
    config.cleaning.mode = CleaningMode.LIGHT  # Preserve conversational tone
    
    engine = CaptionEngine(config, verbose=True)
    caption = engine.process_audio("podcast.mp3")
    
    # Print speaker timeline
    print("\nSpeaker Timeline:")
    current_speaker = None
    for segment in caption.segments:
        if segment.speaker != current_speaker:
            current_speaker = segment.speaker
            print(f"\n[{current_speaker or 'Unknown'}]:")
        print(f"  {segment.text}")


def example_4_professional_subtitles():
    """
    Example 4: Professional Subtitles
    
    Traditional subtitle style for movies/documentaries.
    """
    print("\n=== Example 4: Professional Subtitles ===\n")
    
    config = ProcessingConfig()
    config.transcription.model = "medium"  # Good balance
    config.cleaning.mode = CleaningMode.LIGHT  # Minimal cleaning
    config.styling.preset = "subtitle_classic"
    config.export.format = "srt"  # Standard subtitle format
    
    engine = CaptionEngine(config)
    caption = engine.process("movie.mp4", output="movie.srt")
    
    print(f"Created professional subtitles: {len(caption.segments)} segments")


def example_5_custom_cleaning():
    """
    Example 5: Custom Cleaning Rules
    
    Add custom filler words and configure cleaning.
    """
    print("\n=== Example 5: Custom Cleaning ===\n")
    
    config = ProcessingConfig()
    
    # Custom filler words (e.g., for a specific speaker or domain)
    config.cleaning.custom_fillers = [
        "basically",
        "literally",
        "at the end of the day",
        "to be honest"
    ]
    
    # Fine-tune cleaning
    config.cleaning.collapse_repetitions = True
    config.cleaning.normalize_contractions = True
    config.cleaning.preserve_emphasis = True
    
    engine = CaptionEngine(config)
    caption = engine.process("video.mp4")
    
    # Show cleaning stats
    for segment in caption.segments[:3]:
        if segment.raw_text:
            print(f"Original: {segment.raw_text}")
            print(f"Cleaned:  {segment.text}")
            print(f"Applied:  {', '.join(segment.cleaning_applied)}\n")


def example_6_word_level_timing():
    """
    Example 6: Word-Level Timing
    
    Access word-by-word timing data.
    """
    print("\n=== Example 6: Word-Level Timing ===\n")
    
    config = ProcessingConfig()
    config.transcription.word_timestamps = True
    config.styling.preset = "karaoke"
    
    engine = CaptionEngine(config)
    caption = engine.process("video.mp4")
    
    # Access word timing
    print("Word-level timing for first segment:")
    first_segment = caption.segments[0]
    
    if first_segment.has_words():
        for word in first_segment.words:
            print(f"  {word.text:15} {word.start:.2f}s - {word.end:.2f}s "
                  f"(conf: {word.confidence:.2%})")


def example_7_multilanguage():
    """
    Example 7: Multi-language Processing
    
    Process captions in different languages.
    """
    print("\n=== Example 7: Multi-language ===\n")
    
    # Spanish
    config_es = ProcessingConfig()
    config_es.transcription.language = "es"
    config_es.cleaning.language = "es"
    config_es.cleaning.dialect = "mx"  # Mexican Spanish
    
    engine_es = CaptionEngine(config_es)
    caption_es = engine_es.process("video_spanish.mp4")
    
    print(f"Processed Spanish: {len(caption_es.segments)} segments")
    
    # French
    config_fr = ProcessingConfig()
    config_fr.transcription.language = "fr"
    config_fr.cleaning.language = "fr"
    
    engine_fr = CaptionEngine(config_fr)
    caption_fr = engine_fr.process("video_french.mp4")
    
    print(f"Processed French: {len(caption_fr.segments)} segments")


def example_8_batch_processing():
    """
    Example 8: Batch Processing
    
    Process multiple files with the same configuration.
    """
    print("\n=== Example 8: Batch Processing ===\n")
    
    config = ProcessingConfig.quick(
        cleaning=CleaningMode.BALANCED,
        style="viral_pop"
    )
    
    engine = CaptionEngine(config)
    
    video_files = [
        "video1.mp4",
        "video2.mp4",
        "video3.mp4"
    ]
    
    for video in video_files:
        try:
            output = video.replace(".mp4", "_captions.ass")
            caption = engine.process(video, output=output)
            print(f"✓ {video}: {len(caption.segments)} segments")
        except Exception as e:
            print(f"✗ {video}: {e}")


def example_9_export_formats():
    """
    Example 9: Multiple Export Formats
    
    Export captions in different formats.
    """
    print("\n=== Example 9: Export Formats ===\n")
    
    engine = CaptionEngine()
    caption = engine.process("video.mp4")
    
    # Export to multiple formats
    formats = {
        "captions.ass": "ASS (with animations)",
        "captions.srt": "SRT (basic subtitles)",
        "captions.vtt": "WebVTT (web)",
        "captions.json": "JSON (full data)"
    }
    
    for filename, description in formats.items():
        engine.export(caption, filename)
        print(f"✓ Exported {description}: {filename}")


def example_10_pipeline_inspection():
    """
    Example 10: Pipeline Inspection
    
    Inspect the processing pipeline and metadata.
    """
    print("\n=== Example 10: Pipeline Inspection ===\n")
    
    engine = CaptionEngine(verbose=True)
    caption = engine.process("video.mp4")
    
    # Inspect pipeline
    pipeline = engine.pipeline
    
    print("\nPipeline Stages:")
    for stage in pipeline.stages:
        print(f"  {stage['name']:15} {stage['duration']:.2f}s")
        if stage.get('metadata'):
            for key, value in stage['metadata'].items():
                print(f"    {key}: {value}")
    
    print(f"\nTotal processing time: {pipeline.total_time:.2f}s")
    
    # Caption metadata
    print("\nCaption Metadata:")
    print(f"  Engine:      {caption.engine_used}")
    print(f"  Language:    {caption.language}")
    print(f"  Duration:    {caption.duration:.2f}s")
    print(f"  Segments:    {len(caption.segments)}")
    print(f"  Words:       {caption.word_count}")
    print(f"  Confidence:  {caption.avg_confidence:.2%}")


if __name__ == "__main__":
    print("UACE Examples")
    print("=" * 50)
    
    # Run examples (commented out to avoid file requirements)
    # Uncomment and provide actual video files to run
    
    # example_1_quick_start()
    # example_2_viral_content()
    # example_3_podcast_diarization()
    # example_4_professional_subtitles()
    # example_5_custom_cleaning()
    # example_6_word_level_timing()
    # example_7_multilanguage()
    # example_8_batch_processing()
    # example_9_export_formats()
    # example_10_pipeline_inspection()
    
    print("\nTo run examples, uncomment the function calls")
    print("and provide actual video/audio files.")
