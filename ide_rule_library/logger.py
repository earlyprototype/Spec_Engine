#!/usr/bin/env python3
"""Structured logging framework with correlation IDs"""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Optional


class StructuredLogger:
    """JSON-structured logging with correlation IDs and file/console handlers"""
    
    def __init__(self, name: str, config: dict):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(config.get('level', 'INFO'))
        
        # Clear existing handlers to avoid duplicates
        self.logger.handlers = []
        
        # File handler with JSON formatting
        log_file = Path(config.get('file', 'logs/ide_rule_library.log'))
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(config.get('level', 'INFO'))
        file_handler.setFormatter(self._json_formatter())
        
        # Console handler with readable formatting
        console_handler = logging.StreamHandler()
        console_handler.setLevel(config.get('console_level', 'INFO'))
        console_handler.setFormatter(self._console_formatter())
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def _json_formatter(self):
        """JSON formatter for file logs"""
        class JsonFormatter(logging.Formatter):
            def format(self, record):
                log_data = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'level': record.levelname,
                    'message': record.getMessage(),
                    'module': record.module,
                    'function': record.funcName,
                    'line': record.lineno
                }
                if hasattr(record, 'correlation_id'):
                    log_data['correlation_id'] = record.correlation_id
                if record.exc_info:
                    log_data['exception'] = self.formatException(record.exc_info)
                return json.dumps(log_data)
        return JsonFormatter()
    
    def _console_formatter(self):
        """Readable formatter for console output"""
        return logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%H:%M:%S'
        )
    
    def debug(self, message: str, correlation_id: Optional[str] = None):
        """Log debug message"""
        extra = {'correlation_id': correlation_id} if correlation_id else {}
        self.logger.debug(message, extra=extra)
    
    def info(self, message: str, correlation_id: Optional[str] = None):
        """Log info message"""
        extra = {'correlation_id': correlation_id} if correlation_id else {}
        self.logger.info(message, extra=extra)
    
    def warning(self, message: str, correlation_id: Optional[str] = None):
        """Log warning message"""
        extra = {'correlation_id': correlation_id} if correlation_id else {}
        self.logger.warning(message, extra=extra)
    
    def error(self, message: str, correlation_id: Optional[str] = None, exc_info: bool = False):
        """Log error message"""
        extra = {'correlation_id': correlation_id} if correlation_id else {}
        self.logger.error(message, extra=extra, exc_info=exc_info)
    
    def critical(self, message: str, correlation_id: Optional[str] = None, exc_info: bool = False):
        """Log critical message"""
        extra = {'correlation_id': correlation_id} if correlation_id else {}
        self.logger.critical(message, extra=extra, exc_info=exc_info)
