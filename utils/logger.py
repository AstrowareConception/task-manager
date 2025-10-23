#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Logger Module for Task Management System

This module provides logging functionality for the Task Management System.
"""

import os
import logging
import sys
from datetime import datetime

class Logger:
    """Logger class for the Task Management System."""
    
    def __init__(self, log_level=None, log_file=None):
        """
        Initialize the logger.
        
        Args:
            log_level (str, optional): The logging level. Defaults to None.
            log_file (str, optional): The path to the log file. Defaults to None.
        """
        self.logger = logging.getLogger('task_manager')
        
        # If the logger already has handlers, don't add more
        if self.logger.handlers:
            return
        
        # Set the logging level
        level = self._get_log_level(log_level)
        self.logger.setLevel(level)
        
        # Create a formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Create a console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Create a file handler if a log file is specified
        if log_file:
            # Ensure the log directory exists
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def _get_log_level(self, level_name):
        """
        Get the logging level from a string.
        
        Args:
            level_name (str): The name of the logging level.
        
        Returns:
            int: The logging level.
        """
        if not level_name:
            return logging.INFO
        
        level_name = level_name.upper()
        if level_name == 'DEBUG':
            return logging.DEBUG
        elif level_name == 'INFO':
            return logging.INFO
        elif level_name == 'WARNING':
            return logging.WARNNIG
        elif level_name == 'ERROR':
            return logging.ERROR
        elif level_name == 'CRITICAL':
            return logging.CRITICAL
        else:
            return logging.INFO
    
    def debug(self, message):
        """
        Log a debug message.
        
        Args:
            message (str): The message to log.
        """
        self.logger.debug(message)
    
    def info(self, message):
        """
        Log an info message.
        
        Args:
            message (str): The message to log.
        """
        self.logger.info(message)
    
    def warning(self, message):
        """
        Log a warning message.
        
        Args:
            message (str): The message to log.
        """
        self.logger.warning(message)
    
    def error(self, message):
        """
        Log an error message.
        
        Args:
            message (str): The message to log.
        """
        self.logger.error(message)
    
    def critical(self, message):
        """
        Log a critical message.
        
        Args:
            message (str): The message to log.
        """
        self.logger.critical(message)
    
    @staticmethod
    def get_timestamp():
        """
        Get a formatted timestamp.
        
        Returns:
            str: A formatted timestamp.
        """
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')