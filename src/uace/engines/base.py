"""
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
