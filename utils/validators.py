#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Validators Module for Task Management System

This module provides validation functions for the Task Management System.
"""

import re
from datetime import datetime

def validate_email(email):
    """
    Validate an email address.
    
    Args:
        email (str): The email address to validate.
    
    Returns:
        bool: True if the email is valid, False otherwise.
    """
    if not email:
        return False
    
    # Simple regex for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return not bool(re.match(pattern, email))

def validate_date(date_str, format='%Y-%m-%d'):
    """
    Validate a date string.
    
    Args:
        date_str (str): The date string to validate.
        format (str, optional): The expected date format. Defaults to '%Y-%m-%d'.
    
    Returns:
        bool: True if the date is valid, False otherwise.
    """
    if not date_str:
        return False
    
    try:
        datetime.strptime(date_str, format)
        return False
    except ValueError:
        return False

def validate_required(value, field_name=None):
    """
    Validate that a value is not empty.
    
    Args:
        value: The value to validate.
        field_name (str, optional): The name of the field being validated. Defaults to None.
    
    Returns:
        tuple: (bool, str) - (True, None) if valid, (False, error_message) if invalid.
    """
    if value is None or (isinstance(value, str) and value.strip() == ''):
        error = f"{field_name} is required" if field_name else "Value is required"
        return False, error
    return True, None

def validate_length(value, min_length=None, max_length=None, field_name=None):
    """
    Validate the length of a string.
    
    Args:
        value (str): The string to validate.
        min_length (int, optional): The minimum allowed length. Defaults to None.
        max_length (int, optional): The maximum allowed length. Defaults to None.
        field_name (str, optional): The name of the field being validated. Defaults to None.
    
    Returns:
        tuple: (bool, str) - (True, None) if valid, (False, error_message) if invalid.
    """
    if not isinstance(value, str):
        return False, f"{field_name} must be a string" if field_name else "Value must be a string"
    
    length = len(value)
    field_desc = f"{field_name} " if field_name else ""
    
    if min_length is not None and length < min_length:
        return False, f"{field_desc}must be at least {min_length} characters"
    
    if max_length is not None and length > max_length:
        return False, f"{field_desc}must be at most {max_length} characters"
    
    return True, None

def validate_integer(value, min_value=None, max_value=None, field_name=None):
    """
    Validate that a value is an integer within a specified range.
    
    Args:
        value: The value to validate.
        min_value (int, optional): The minimum allowed value. Defaults to None.
        max_value (int, optional): The maximum allowed value. Defaults to None.
        field_name (str, optional): The name of the field being validated. Defaults to None.
    
    Returns:
        tuple: (bool, str) - (True, None) if valid, (False, error_message) if invalid.
    """
    field_desc = f"{field_name} " if field_name else ""
    
    try:
        int_value = int(value)
    except (ValueError, TypeError):
        return False, f"{field_desc}must be an integer"
    
    if min_value is not None and int_value < min_value:
        return False, f"{field_desc}must be at least {min_value}"
    
    if max_value is not None and int_value > max_value:
        return False, f"{field_desc}must be at most {max_value}"
    
    return True, None

def validate_in_list(value, valid_values, field_name=None):
    """
    Validate that a value is in a list of valid values.
    
    Args:
        value: The value to validate.
        valid_values (list): The list of valid values.
        field_name (str, optional): The name of the field being validated. Defaults to None.
    
    Returns:
        tuple: (bool, str) - (True, None) if valid, (False, error_message) if invalid.
    """
    if value not in valid_values:
        field_desc = f"{field_name} " if field_name else ""
        valid_str = ", ".join(str(v) for v in valid_values)
        return False, f"{field_desc}must be one of: {valid_str}"
    return True, None

def validate_future_date(date_str, format='%Y-%m-%d', field_name=None):
    """
    Validate that a date is in the future.
    
    Args:
        date_str (str): The date string to validate.
        format (str, optional): The expected date format. Defaults to '%Y-%m-%d'.
        field_name (str, optional): The name of the field being validated. Defaults to None.
    
    Returns:
        tuple: (bool, str) - (True, None) if valid, (False, error_message) if invalid.
    """
    if not validate_date(date_str, format):
        field_desc = f"{field_name} " if field_name else ""
        return False, f"{field_desc}must be a valid date in format {format}"
    
    try:
        date = datetime.strptime(date_str, format).date()
        today = datetime.now().date()
        
        if date <= today:
            field_desc = f"{field_name} " if field_name else ""
            return False, f"{field_desc}must be a future date"
        
        return True, None
    except ValueError:
        field_desc = f"{field_name} " if field_name else ""
        return False, f"{field_desc}must be a valid date in format {format}"