"""Logging configuration for Manager desktop application.

Handles file-based logging with rotation and console output for debugging.
"""
import logging
import logging.handlers
import os
import sys


def _get_app_dir():
    """Return persistent directory for app data (works with PyInstaller)."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(__file__))


def setup_logging(log_level=logging.INFO):
    """Configure file-based logging with rotation.
    
    Args:
        log_level: logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    app_dir = _get_app_dir()
    logs_dir = os.path.join(app_dir, "logs")
    
    # Create logs directory if it doesn't exist
    os.makedirs(logs_dir, exist_ok=True)
    
    log_file = os.path.join(logs_dir, "manager.log")
    
    # Create logger
    logger = logging.getLogger("Manager")
    logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # File handler with rotation (10 MB max, keep 5 backups)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    
    # Console handler for development/debugging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)  # Only WARNING and above to console
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info("=" * 70)
    logger.info("Manager Application Started")
    logger.info("=" * 70)
    
    return logger


# Global logger instance
_logger = None


def get_logger():
    """Get the global logger instance."""
    global _logger
    if _logger is None:
        _logger = setup_logging()
    return _logger


def log_exception(exc: Exception, context: str = ""):
    """Log an exception with context.
    
    Args:
        exc: The exception to log
        context: Additional context about what was happening
    """
    logger = get_logger()
    if context:
        logger.exception(f"Exception in {context}: {str(exc)}")
    else:
        logger.exception(f"Unexpected exception: {str(exc)}")
