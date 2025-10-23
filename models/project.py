#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Model for Task Management System

This module defines the Project class which represents a project in the system.
"""

from datetime import datetime

class Project:
    """
    Project class representing a project in the Task Management System.
    
    Attributes:
        id (int): The unique identifier for the project.
        name (str): The name of the project.
        description (str): The description of the project.
        start_date (datetime.date): The start date of the project.
        end_date (datetime.date): The end date of the project.
        manager_id (int): The ID of the user who manages the project.
        created_at (datetime): The timestamp when the project was created.
    """
    
    def __init__(self, name, description="", start_date=None, end_date=None, 
                 manager_id=None, id=None, created_at=None):
        """
        Initialize a Project object.
        
        Args:
            name (str): The name of the project.
            description (str, optional): The description of the project. Defaults to "".
            start_date (datetime.date, optional): The start date of the project. Defaults to None.
            end_date (datetime.date, optional): The end date of the project. Defaults to None.
            manager_id (int, optional): The ID of the user who manages the project. Defaults to None.
            id (int, optional): The unique identifier for the project. Defaults to None.
            created_at (datetime, optional): The timestamp when the project was created. Defaults to None.
        """
        self.id = id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.manager_id = manager_id
        self.created_at = created_at or datetime.now()
    
    @classmethod
    def from_db_row(cls, row):
        """
        Create a Project object from a database row.
        
        Args:
            row (sqlite3.Row): A row from the database.
        
        Returns:
            Project: A Project object.
        """
        if not row:
            return None
        
        # Parse dates from string if they exist
        start_date = None
        if row['start_date']:
            try:
                start_date = datetime.strptime(row['start_date'], '%Y-%m-%d').date()
            except ValueError:
                pass
        
        end_date = None
        if row['end_date']:
            try:
                end_date = datetime.strptime(row['end_date'], '%Y-%m-%d').date()
            except ValueError:
                pass
        
        created_at = None
        if row['created_at']:
            try:
                created_at = datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass
        
        return cls(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            start_date=start_date,
            end_date=end_date,
            manager_id=row['manager_id'],
            created_at=created_at
        )
    
    def to_dict(self):
        """
        Convert the Project object to a dictionary.
        
        Returns:
            dict: A dictionary representation of the Project.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'manager_id': self.manager_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
    
    def __str__(self):
        """
        Return a string representation of the Project.
        
        Returns:
            str: A string representation of the Project.
        """
        return f"Project(id={self.id}, name='{self.name}')"
    
    def __repr__(self):
        """
        Return a string representation of the Project for debugging.
        
        Returns:
            str: A string representation of the Project.
        """
        return self.__str__()
    
    def is_active(self):
        """
        Check if the project is currently active.
        
        Returns:
            bool: True if the project is active, False otherwise.
        """
        today = datetime.now().date()
        
        # If no dates are set, consider it active
        if not self.start_date and not self.end_date:
            return True
        
        # If only start date is set, check if it's in the past
        if self.start_date and not self.end_date:
            return self.start_date <= today
        
        # If only end date is set, check if it's in the future
        if not self.start_date and self.end_date:
            return today <= self.end_date
        
        # If both dates are set, check if today is between them
        return self.start_date <= today <= self.end_date
    
    def is_completed(self):
        """
        Check if the project is completed (end date is in the past).
        
        Returns:
            bool: True if the project is completed, False otherwise.
        """
        if not self.end_date:
            return False
        
        return self.end_date < datetime.now().date()
    
    def is_upcoming(self):
        """
        Check if the project is upcoming (start date is in the future).
        
        Returns:
            bool: True if the project is upcoming, False otherwise.
        """
        if not self.start_date:
            return False
        
        return self.start_date > datetime.now().date()
    
    def get_duration_days(self):
        """
        Calculate the duration of the project in days.
        
        Returns:
            int: The duration in days, or None if start_date or end_date is not set.
        """
        if not self.start_date or not self.end_date:
            return None
        
        return (self.end_date - self.start_date).days