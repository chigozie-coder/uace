"""
Main caption processing engine.
"""

import time
import logging
from pathlib import Path
from typing import Optional, Union

from uace.models import Caption, TranscriptionResult
from uace.config import ProcessingConfig
from uace.engines.transcription import EngineSelector

# Graceful rich imports
try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    # Minimal stubs
    class Console:
        def print(self, *args, **kwargs):
            print(*args)
    
    class Progress:
        def __init__(self, *args, **kwargs):
            pass
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def add_task(self, *args, **kwargs):
            return 0
        def update(self, *args, **kwargs):
            pass
    
    SpinnerColumn = TextColumn = TimeElapsedColumn = object


from uace.config import ProcessingConfig, CleaningMode, ExportFormat
from uace.models import Caption, ProcessingPipeline, TranscriptionResult
from uace.engines.transcription import EngineSelector
from uace.cleaning.engine import SubtitleCleaner
from uace.chunking.semantic import SemanticChunker
from uace.styling.presets import get_preset, VIRAL_POP
from uace.export.formats import ASSExporter, SRTExporter, VTTExporter
from uace.utils.logging import setup_logging, UACELogger


class CaptionEngine:
    """
    Universal Auto-Caption Engine
    
    The complete pipeline: Transcribe → Clean → Chunk → Style → Export
    """
    
    @staticmethod
    def _safe_list_attr(obj, attr_name: str, default=None):
        """
        Safely get a list attribute, ensuring it's never None.
        
        Args:
            obj: Object to get attribute from
            attr_name: Name of the attribute
            default: Default value if attribute is None or missing
            
        Returns:
            List value or default (never None)
        """
        if default is None:
            default = []
        value = getattr(obj, attr_name, default)
        return value if value is not None else default
    
    @staticmethod
    def _safe_num_attr(obj, attr_name: str, default=0.0):
        """
        Safely get a numeric attribute, ensuring it's never None.
        
        Args:
            obj: Object to get attribute from
            attr_name: Name of the attribute
            default: Default value if attribute is None or missing
            
        Returns:
            Numeric value or default (never None)
        """
        value = getattr(obj, attr_name, None)
        return value if value is not None else default
    
    def __init__(
        self,
        config: Optional[ProcessingConfig] = None,
        verbose: bool = False,
        log_file: Optional[str] = None
    ):
        """
        Initialize Caption Engine.
        """
        self.config = config or ProcessingConfig()
        self.verbose = verbose or self.config.verbose
        self.console = Console() if self.verbose else None
        self.pipeline = ProcessingPipeline()
        
        # Setup logging
        self.logger = setup_logging(
            verbose=self.verbose,
            log_file=log_file
        )
        
        # FIX: Ensure logger works even if setup_logging returned a standard logger
        self._ensure_robust_logger()
        
        # Components (lazy-loaded)
        self._transcription_engine = None
        self._cleaner = None
        self._chunker = None
    
    def _ensure_robust_logger(self):
        """
        Guarantees self.logger has 'stage' and other custom methods.
        If we got a standard Logger, we wrap it in an adapter.
        """
        # If it already has the method, we are good (it's likely a UACELogger)
        if hasattr(self.logger, 'stage'):
            return

        # If we are here, we have a standard Logger (or broken object). Wrap it.
        class LoggerAdapter:
            def __init__(self, original_logger):
                self.logger = original_logger
            
            def __getattr__(self, name):
                # Pass through standard methods (info, error, etc.) to the real logger
                return getattr(self.logger, name)

            def stage(self, name: str, current: int, total: int):
                self.logger.info(f"Stage {current}/{total}: {name}")

            def statistics(self, stats: dict):
                self.logger.info("\n" + "="*70)
                self.logger.info("📊 STATISTICS")
                self.logger.info("="*70)
                for key, value in stats.items():
                    self.logger.info(f"  {key}: {value}")
                self.logger.info("="*70)

            def close_all_progress(self):
                pass

            def progress_bar(self, total: int, desc: str = "", **kwargs):
                # Simple fallback
                try:
                    from tqdm import tqdm
                    return tqdm(total=total, desc=desc, **kwargs)
                except ImportError:
                    class Dummy:
                        def update(self, n=1): pass
                        def close(self): pass
                        def __enter__(self): return self
                        def __exit__(self, *args): pass
                    return Dummy()

        # Replace the raw logger with our adapter
        self.logger = LoggerAdapter(self.logger)
    
    def process(
        self,
        input_file: Union[str, Path],
        output: Optional[Union[str, Path]] = None,
        **overrides
    ) -> Caption:
        """
        Process a video or audio file end-to-end.
        """
        input_path = Path(input_file)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Apply overrides
        self._apply_overrides(**overrides)
        
        # Determine if video or audio
        audio_extensions = {'.mp3', '.wav', '.flac', '.m4a', '.ogg'}
        video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.webm'}
        
        suffix = input_path.suffix.lower()
        
        if suffix in audio_extensions:
            return self.process_audio(str(input_path), output)
        elif suffix in video_extensions:
            return self.process_video(str(input_path), output)
        else:
            # Fallback: Try processing as audio anyway if extension unknown
            self.logger.warning(f"Unknown extension {suffix}, attempting to process as audio/video")
            return self.process_video(str(input_path), output)
    
    def process_video(
        self,
        video_file: str,
        output: Optional[str] = None
    ) -> Caption:
        """
        Process a video file.
        Extracts audio, then processes as audio.
        """
        if self.verbose and self.console:
            self.console.print("[bold blue]Processing video...[/bold blue]")
        
        # Extract audio (would use ffmpeg in production)
        audio_file = self._extract_audio(video_file)
        
        # Process audio
        caption = self.process_audio(audio_file, output)
        
        return caption
    
    def process_audio(
        self,
        audio_file: str,
        output: Optional[str] = None
    ) -> Caption:
        """
        Process an audio file through the complete pipeline.
        """
        start_time = time.time()
        
        self.logger.info("\n" + "="*70)
        self.logger.info("🎬 UACE Caption Generation Pipeline")
        self.logger.info("="*70)
        self.logger.info(f"Input: {audio_file}")
        self.logger.info(f"Output: {output or 'In-memory'}")
        self.logger.info("")
        
        # Stage 1: Transcription
        self.logger.stage("Transcription", 1, 5)
        transcription = self._transcribe(audio_file)
        # Safe attribute access with helper - never returns None
        transcription_segments = self._safe_list_attr(transcription, 'segments')
        self.logger.info(f"✅ Transcribed {len(transcription_segments)} segments")
        audio_dur = self._safe_num_attr(transcription, 'audio_duration', 0.0)
        self.logger.info(f"⏱️  Duration: {audio_dur:.1f}s")
        
        # Stage 2: Cleaning
        self.logger.stage("Cleaning", 2, 5)
        caption = self._clean(transcription)
        
        # Stage 3: Chunking
        self.logger.stage("Chunking", 3, 5)
        caption = self._chunk(caption)
        seg_count = len(self._safe_list_attr(caption, 'segments'))
        self.logger.info(f"✅ Created {seg_count} chunks")
        
        # Stage 4: Styling (metadata)
        self.logger.stage("Styling", 4, 5)
        caption = self._style(caption)
        
        # Stage 5: Export
        if output:
            self.logger.stage("Export", 5, 5)
            self.export(caption, output)
            self.logger.info(f"✅ Exported to {output}")
        
        # Final summary
        total_time = time.time() - start_time
        self.logger.close_all_progress()
        
        # Safely extract statistics with helpers - never returns None
        segments_count = len(self._safe_list_attr(caption, 'segments'))
        duration = self._safe_num_attr(caption, 'duration', 0.0)
        word_count = self._safe_num_attr(caption, 'word_count', 0)
        avg_confidence = self._safe_num_attr(caption, 'avg_confidence', 0.0)
        
        self.logger.statistics({
            "Total Segments": segments_count,
            "Total Duration": f"{duration:.1f}s",
            "Word Count": word_count,
            "Avg Confidence": f"{avg_confidence:.1%}",
            "Processing Time": f"{total_time:.1f}s",
            "Speed": f"{duration/total_time if total_time > 0 else 0:.1f}x realtime"
        })
        
        self.logger.info("🎉 Caption generation complete!\n")
        
        return caption
    
    def _transcribe(self, audio_file: str) -> TranscriptionResult:
        """Transcription stage."""
        start_time = time.time()
        
        # Get or create engine
        if not self._transcription_engine:
            self._transcription_engine = EngineSelector.select_engine(
                self.config.transcription
            )
        
        # Transcribe
        result = self._transcription_engine.transcribe(audio_file)
        
        # Track in pipeline
        self.pipeline.add_stage(
            "transcription",
            duration=time.time() - start_time,
            metadata={
                "engine": getattr(result, 'engine', 'unknown'),
                "model": getattr(result, 'model', 'unknown'),
                "language": getattr(result, 'language', 'en'),
                "segments": len(self._safe_list_attr(result, 'segments'))
            }
        )
            
        
        
        return result
    
    def _clean(self, transcription: TranscriptionResult) -> Caption:
        """Cleaning stage."""
        start_time = time.time()
        
        # Get or create cleaner
        if not self._cleaner:
            self._cleaner = SubtitleCleaner(self.config.cleaning)
        
        # Convert to caption
        caption = transcription.to_caption()
        
        # Clean segments with progress bar - use safe helper
        segments_to_clean = self._safe_list_attr(caption, 'segments')
        pbar = self.logger.progress_bar(
            total=len(segments_to_clean),
            desc="Cleaning segments",
            unit="seg"
        )
        
        cleaned_segments = []
        for segment in segments_to_clean:
            cleaned = self._cleaner.clean_segment(segment)
            cleaned_segments.append(cleaned)
            pbar.update(1)
        
        pbar.close()
        
        caption.segments = cleaned_segments
        # Safe assignment with fallback
        if hasattr(self.config.cleaning, 'mode') and hasattr(self.config.cleaning.mode, 'value'):
            caption.cleaning_mode = self.config.cleaning.mode.value
        else:
            caption.cleaning_mode = 'unknown'
        
        # Compute stats
        caption.compute_stats()
        
        # Log cleaning stats
        stats = self._cleaner.get_stats()
        fillers = getattr(stats, 'fillers_removed', 0) if stats else 0
        reps = getattr(stats, 'repetitions_collapsed', 0) if stats else 0
        self.logger.info(f"   Fillers removed: {fillers}")
        #self.logger.info(f"   Events removed: {stats.events_removed}")
        self.logger.info(f"   Repetitions collapsed: {reps}")
        
        # Track in pipeline
        self.pipeline.add_stage(
            "cleaning",
            duration=time.time() - start_time,
            metadata={
                "mode": getattr(self.config.cleaning.mode, 'value', 'unknown') if hasattr(self.config.cleaning, 'mode') else 'unknown',
                "reduction": f"{getattr(stats, 'reduction_percent', 0.0):.1f}%" if stats else "0.0%",
                "fillers_removed": getattr(stats, 'fillers_removed', 0) if stats else 0,
                "operations": getattr(stats, 'operations_applied', []) if stats else []
            }
        )
        
        return caption
    
    def _chunk(self, caption: Caption) -> Caption:
        """Chunking stage."""
        start_time = time.time()
        
        # Get or create chunker
        if not self._chunker:
            self._chunker = SemanticChunker(self.config.chunking)
        
        # Chunk segments safely - use safe helper
        segments = self._safe_list_attr(caption, 'segments')
        caption.segments = self._chunker.chunk_segments(segments)
        
        # Track in pipeline
        self.pipeline.add_stage(
            "chunking",
            duration=time.time() - start_time,
            metadata={
                "strategy": getattr(self.config.chunking.strategy, 'value', 'unknown') if hasattr(self.config.chunking, 'strategy') else 'unknown',
                "final_segments": len(self._safe_list_attr(caption, 'segments'))
            }
        )
        
        return caption
    
    def _style(self, caption: Caption) -> Caption:
        """Styling stage (metadata only, actual rendering happens at export)."""
        start_time = time.time()
        
        # Get preset - handle both enum and string
        preset_name = self.config.styling.preset
        if hasattr(preset_name, 'value'):
            preset_name = preset_name.value
        
        preset = get_preset(preset_name)
        if not preset:
            preset = VIRAL_POP
        
        # Store style info in caption
        preset_name_str = getattr(preset, 'name', 'viral_pop')
        caption.style_preset = preset_name_str
        
        # Auto-emphasis detection (if enabled)
        if getattr(self.config.styling, 'auto_emphasis', False):
            segments = self._safe_list_attr(caption, 'segments')
            for segment in segments:
                if hasattr(segment, 'text'):
                    segment.emphasis_words = self._detect_emphasis_words(segment.text)
        
        # Track in pipeline
        self.pipeline.add_stage(
            "styling",
            duration=time.time() - start_time,
            metadata={
                "preset": preset_name_str,
                "animation": getattr(self.config.styling, 'animation_style', 'default')
            }
        )
        
        return caption
    
    def export(self, caption: Caption, output_path: str) -> None:
        """
        Export caption to file.
        
        Supports: ASS, SRT, VTT, JSON
        """
        output = Path(output_path)
        format_str = output.suffix.lower().lstrip('.')
        
        # Determine format
        try:
            export_format = ExportFormat(format_str)
        except ValueError:
            export_format = ExportFormat.ASS
            output = output.with_suffix('.ass')
        
        # Get preset for styling - safe attribute access
        preset_value = self.config.styling.preset
        if hasattr(preset_value, 'value'):
            preset_value = preset_value.value
        preset = get_preset(preset_value) or VIRAL_POP
        
        # Export based on format
        if export_format == ExportFormat.ASS:
            exporter = ASSExporter(preset, self.config.export)
            exporter.export(caption, str(output))
        
        elif export_format == ExportFormat.SRT:
            exporter = SRTExporter()
            exporter.export(caption, str(output))
        
        elif export_format == ExportFormat.VTT:
            exporter = VTTExporter()
            exporter.export(caption, str(output))
        
        elif export_format == ExportFormat.JSON:
            self._export_json(caption, str(output))
        
        else:
            raise ValueError(f"Unsupported export format: {export_format}")
        
        if self.verbose and self.console:
            self.console.print(f"[green]✓ Exported to: {output}[/green]")
    
    def _export_json(self, caption: Caption, output_path: str) -> None:
        """Export caption as JSON."""
        import json
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(caption.model_dump(), f, indent=2, ensure_ascii=False)
    
    def _extract_audio(self, video_file: str) -> str:
        """Extract audio from video (stub - would use ffmpeg)."""
        # In production: use ffmpeg-python
        # For now, assume video_file is actually audio or has audio stream
        return video_file
    
    def _detect_emphasis_words(self, text: str) -> list[str]:
        """
        Detect words that should be emphasized.
        """
        words = text.split()
        emphasis = []
        
        for word in words:
            clean_word = word.strip('.,!?;:')
            
            # All caps (but not single letter)
            if clean_word.isupper() and len(clean_word) > 1:
                emphasis.append(word)
            
            # Words with exclamation
            if '!' in word:
                emphasis.append(word)
        
        return emphasis
    
    def _apply_overrides(self, **overrides) -> None:
        """Apply configuration overrides."""
        for key, value in overrides.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
    
    def _print_summary(self, caption: Caption) -> None:
        """Print processing summary."""
        from rich.table import Table
        
        if not self.console:
            return

        table = Table(title="Processing Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        # Safe attribute extraction with helpers
        segments_count = len(self._safe_list_attr(caption, 'segments'))
        duration = self._safe_num_attr(caption, 'duration', 0.0)
        word_count = self._safe_num_attr(caption, 'word_count', 0)
        avg_confidence = self._safe_num_attr(caption, 'avg_confidence', 0.0)
        engine = getattr(caption, 'engine_used', None) or 'unknown'
        
        table.add_row("Segments", str(segments_count))
        table.add_row("Duration", f"{duration:.2f}s")
        table.add_row("Word Count", str(word_count))
        table.add_row("Avg Confidence", f"{avg_confidence * 100:.1f}%")
        table.add_row("Processing Time", f"{self.pipeline.total_time:.2f}s")
        table.add_row("Engine", engine)
        
        self.console.print(table)


# Convenience functions

def quick_caption(
    input_file: str,
    output: Optional[str] = None,
    style: str = "viral_pop",
    cleaning: str = "balanced"
) -> Caption:
    """
    Quick caption generation with sensible defaults.
    """
    config = ProcessingConfig.quick()
    config.styling.preset = style
    config.cleaning.mode = CleaningMode(cleaning)
    
    engine = CaptionEngine(config)
    return engine.process(input_file, output)
