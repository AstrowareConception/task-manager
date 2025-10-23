#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration Module for Task Management System

This module provides configuration management for the Task Management System.
It loads configuration from a file or environment variables and provides
access to these settings throughout the application.
"""

import os
import json
import logging
from pathlib import Path

class Config:
    """Configuration manager for the Task Management System."""
    
    def __init__(self, config_file=None):
        """
        Initialize the configuration manager.
        
        Args:
            config_file (str, optional): Path to the configuration file.
                If not provided, it will look for a file named 'config.json'
                in the current directory or use default values.
        """
        self.config = {
            # Default configuration values
            'database_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'taskmanager.db'),
            'log_level': 'INFO',
            'log_file': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'taskmanager.log'),
            'max_tasks_per_user': 100,
            'max_projects': 50,
            'date_format': '%Y-%m-%d',
        }
        
        # Load configuration from file if provided
        if config_file:
            self._load_from_file(config_file)
        else:
            default_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
            if os.path.exists(default_config):
                self._load_from_file(default_config)
        
        # Override with environment variables if present
        self._load_from_env()
        
        # Ensure directories exist
        self._ensure_directories()
    
    def _load_from_file(self, config_file):
        """
        Load configuration from a JSON file.
        
        Args:
            config_file (str): Path to the configuration file.
        """
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                self.config.update(file_config)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.warning(f"Error loading configuration from {config_file}: {str(e)}")
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        env_prefix = 'TASKMANAGER_'
        for key in self.config.keys():
            env_key = f"{env_prefix}{key.upper()}"
            if env_key in os.environ:
                # Convert environment variable to appropriate type
                if isinstance(self.config[key], int):
                    self.config[key] = int(os.environ[env_key])
                elif isinstance(self.config[key], bool):
                    self.config[key] = os.environ[env_key].lower() in ('true', 'yes', '1')
                else:
                    self.config[key] = os.environ[env_key]
    
    def _ensure_directories(self):
        """Ensure that necessary directories exist."""
        # Ensure data directory exists
        data_dir = os.path.dirname(self.config['database_path'])
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Ensure log directory exists
        log_dir = os.path.dirname(self.config['log_file'])
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    def get(self, key, default=None):
        """
        Get a configuration value.
        
        Args:
            key (str): The configuration key.
            default: The default value to return if the key is not found.
        
        Returns:
            The configuration value or the default value if the key is not found.
        """
        return self.config.get(key, default)
    
    def set(self, key, value):
        """
        Set a configuration value.
        
        Args:
            key (str): The configuration key.
            value: The value to set.
        """
        self.config[key] = value
    
    def save(self, config_file=None):
        """
        Save the current configuration to a file.
        
        Args:
            config_file (str, optional): Path to the configuration file.
                If not provided, it will use the default 'config.json' file.
        """
        if not config_file:
            config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
        
        try:
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving configuration to {config_file}: {str(e)}")