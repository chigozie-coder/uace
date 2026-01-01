"""
Logging Configuration for UACE

Provides comprehensive logging with tqdm progress bars.

FIXED VERSION - Enhanced error handling and robustness.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


class TqdmLoggingHandler(logging.Handler):
    """
    Logging handler that works with tqdm progress bars.
    Prevents logging from disrupting progress bar display.
    
    FIXED: Enhanced error handling.
    """
    
    def emit(self, record):
        """
        Emit a log record.
        
        FIXED: Better fallback handling.
        """
        try:
            from tqdm import tqdm
            msg = self.format(record)
            tqdm.write(msg)
        except ImportError:
            # Fallback if tqdm not available
            try:
                print(self.format(record), file=sys.stderr)
            except Exception:
                # Last resort fallback
                print(str(record.getMessage()), file=sys.stderr)
        except Exception as e:
            # Handle any other errors gracefully
            try:
                print(self.format(record), file=sys.stderr)
            except Exception:
                pass


class ColoredFormatter(logging.Formatter):
    """
    Colored log formatter for better readability.
    
    FIXED: Enhanced with better error handling and terminal detection.
    """
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    # Emoji prefixes
    EMOJI = {
        'DEBUG': '🔍',
        'INFO': '✅',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'CRITICAL': '🚨',
    }
    
    def __init__(self, *args, use_colors=True, use_emoji=True, **kwargs):
        """
        Initialize formatter.
        
        Args:
            use_colors: Enable ANSI colors
            use_emoji: Enable emoji prefixes
        """
        super().__init__(*args, **kwargs)
        self.use_colors = use_colors
        self.use_emoji = use_emoji
    
    def format(self, record):
        """
        Format log record.
        
        FIXED: Better handling of record modification.
        """
        try:
            levelname = record.levelname
            
            if self.use_colors and levelname in self.COLORS:
                # Create a copy to avoid modifying the original record permanently
                original_levelname = record.levelname
                
                # Build formatted level name
                parts = []
                if self.use_colors:
                    parts.append(self.COLORS[levelname])
                if self.use_emoji:
                    parts.append(self.EMOJI.get(levelname, ''))
                parts.append(levelname)
                if self.use_colors:
                    parts.append(self.RESET)
                
                record.levelname = ' '.join(parts)
                result = super().format(record)
                record.levelname = original_levelname
                return result
        except Exception:
            # Fallback to standard formatting
            pass
        
        return super().format(record)


class UACELogger:
    """
    UACE-specific logger with tqdm integration.
    Wraps a standard logger to add custom methods like stage() and statistics().
    
    FIXED: Enhanced error handling and guaranteed method availability.
    """
    
    def __init__(self, name: str = "uace", verbose: bool = False):
        """
        Initialize UACE logger.
        
        Args:
            name: Logger name
            verbose: Enable verbose output
        """
        self.logger = logging.getLogger(name)
        self.verbose = verbose
        self._progress_bars = []
    
    def debug(self, msg: str, *args, **kwargs):
        """
        Log debug message.
        
        Args:
            msg: Log message
        """
        try:
            self.logger.debug(msg, *args, **kwargs)
        except Exception as e:
            print(f"DEBUG: {msg}", file=sys.stderr)
    
    def info(self, msg: str, *args, **kwargs):
        """
        Log info message.
        
        Args:
            msg: Log message
        """
        try:
            self.logger.info(msg, *args, **kwargs)
        except Exception as e:
            print(f"INFO: {msg}", file=sys.stderr)
    
    def warning(self, msg: str, *args, **kwargs):
        """
        Log warning message.
        
        Args:
            msg: Log message
        """
        try:
            self.logger.warning(msg, *args, **kwargs)
        except Exception as e:
            print(f"WARNING: {msg}", file=sys.stderr)
    
    def error(self, msg: str, *args, **kwargs):
        """
        Log error message.
        
        Args:
            msg: Log message
        """
        try:
            self.logger.error(msg, *args, **kwargs)
        except Exception as e:
            print(f"ERROR: {msg}", file=sys.stderr)
    
    def critical(self, msg: str, *args, **kwargs):
        """
        Log critical message.
        
        Args:
            msg: Log message
        """
        try:
            self.logger.critical(msg, *args, **kwargs)
        except Exception as e:
            print(f"CRITICAL: {msg}", file=sys.stderr)
    
    def exception(self, msg: str, *args, **kwargs):
        """
        Log exception message with traceback.
        
        Args:
            msg: Log message
        """
        try:
            self.logger.exception(msg, *args, **kwargs)
        except Exception as e:
            print(f"EXCEPTION: {msg}", file=sys.stderr)
            import traceback
            traceback.print_exc()
    
    def stage(self, name: str, current: int, total: int):
        """
        Log a processing stage.
        
        FIXED: Enhanced formatting and error handling.
        
        Args:
            name: Stage name
            current: Current stage number
            total: Total number of stages
        """
        try:
            self.logger.info(f"\n{'='*70}")
            self.logger.info(f"📍 Stage {current}/{total}: {name}")
            self.logger.info(f"{'='*70}")
        except Exception:
            # Fallback
            try:
                print(f"\nStage {current}/{total}: {name}", file=sys.stderr)
            except Exception:
                pass
    
    def statistics(self, stats: dict):
        """
        Log statistics.
        
        FIXED: Better formatting and error handling.
        
        Args:
            stats: Dictionary of statistics to display
        """
        try:
            self.logger.info("\n" + "="*70)
            self.logger.info("📊 STATISTICS")
            self.logger.info("="*70)
            for key, value in stats.items():
                self.logger.info(f"  {key:.<50} {value}")
            self.logger.info("="*70)
        except Exception:
            # Fallback
            try:
                print("\n" + "="*70, file=sys.stderr)
                print("STATISTICS", file=sys.stderr)
                print("="*70, file=sys.stderr)
                for key, value in stats.items():
                    print(f"  {key}: {value}", file=sys.stderr)
                print("="*70, file=sys.stderr)
            except Exception:
                pass
    
    def close_all_progress(self):
        """
        Close any open progress bars.
        
        FIXED: Enhanced cleanup with better error handling.
        """
        for pbar in self._progress_bars[:]:  # Create a copy to iterate
            try:
                if hasattr(pbar, 'close'):
                    pbar.close()
            except Exception:
                # Silently ignore errors during cleanup
                pass
        
        self._progress_bars.clear()
    
    def progress_bar(self, total: int, desc: str = "", **kwargs):
        """
        Create a progress bar.
        
        FIXED: Enhanced with better fallback handling.
        
        Args:
            total: Total number of items
            desc: Progress bar description
            **kwargs: Additional tqdm arguments
            
        Returns:
            Progress bar object (tqdm or dummy)
        """
        try:
            from tqdm import tqdm
            pbar = tqdm(total=total, desc=desc, **kwargs)
            self._progress_bars.append(pbar)
            return pbar
        except ImportError:
            pass
        except Exception as e:
            self.warning(f"Could not create progress bar: {e}")
        
        # Return enhanced dummy object if tqdm not available
        class DummyProgressBar:
            """
            Dummy progress bar that does nothing but won't crash.
            
            FIXED: Enhanced with all common tqdm methods.
            """
            def __init__(self, total=None, desc=""):
                self.total = total
                self.desc = desc
                self.n = 0
            
            def update(self, n=1):
                """Update progress."""
                self.n += n
            
            def close(self):
                """Close progress bar."""
                pass
            
            def __enter__(self):
                """Context manager entry."""
                return self
            
            def __exit__(self, *args):
                """Context manager exit."""
                self.close()
            
            def set_description(self, desc):
                """Set description."""
                self.desc = desc
            
            def set_postfix(self, **kwargs):
                """Set postfix values."""
                pass
            
            def refresh(self):
                """Refresh display."""
                pass
            
            def reset(self, total=None):
                """Reset progress."""
                self.n = 0
                if total is not None:
                    self.total = total
        
        dummy = DummyProgressBar(total=total, desc=desc)
        self._progress_bars.append(dummy)
        return dummy


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    use_colors: bool = True,
    verbose: bool = False
) -> UACELogger:
    """
    Setup UACE logging configuration.
    
    FIXED: Enhanced error handling and guaranteed return value.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
        use_colors: Enable colored output
        verbose: Enable verbose mode (sets level to DEBUG)
        
    Returns:
        UACELogger instance (always returns a working logger)
    """
    
    try:
        # Set level
        if verbose:
            level = "DEBUG"
        
        log_level = getattr(logging, level.upper(), logging.INFO)
        
        # Create logger
        logger = logging.getLogger("uace")
        logger.setLevel(log_level)
        logger.handlers.clear()  # Remove existing handlers
        
        # Console handler with tqdm support
        console_handler = TqdmLoggingHandler()
        console_handler.setLevel(log_level)
        
        # Determine if we should use colors
        should_use_colors = use_colors and sys.stdout.isatty()
        
        # Format
        if should_use_colors:
            formatter = ColoredFormatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S',
                use_colors=True,
                use_emoji=True
            )
        else:
            formatter = ColoredFormatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S',
                use_colors=False,
                use_emoji=False
            )
        
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler if specified
        if log_file:
            try:
                log_path = Path(log_file)
                log_path.parent.mkdir(parents=True, exist_ok=True)
                
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(logging.DEBUG)  # Always log everything to file
                
                file_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                file_handler.setFormatter(file_formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                # If file logging fails, continue without it
                print(f"Warning: Could not setup file logging: {e}", file=sys.stderr)
        
    except Exception as e:
        # If anything fails, fall back to basic logging
        print(f"Warning: Error setting up logging: {e}", file=sys.stderr)
        logging.basicConfig(level=logging.INFO)
    
    # Always return a UACELogger instance
    return UACELogger("uace", verbose=verbose)


def get_logger(name: str = "uace") -> logging.Logger:
    """
    Get standard logger (legacy support).
    
    Args:
        name: Logger name
        
    Returns:
        Standard Python logger
    """
    return logging.getLogger(name)


# Create default logger
logger = get_logger()

__all__ = [
    "setup_logging",
    "get_logger",
    "logger",
    "UACELogger",
    "TqdmLoggingHandler",
    "ColoredFormatter",
]
