#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Task Model for Task Management System

This module defines the Task class which represents a task in the system.
"""

from datetime import datetime

class Task:
    """
    Task class representing a task in the Task Management System.
    
    Attributes:
        id (int): The unique identifier for the task.
        title (str): The title of the task.
        description (str): The description of the task.
        status (str): The status of the task (pending, in_progress, completed).
        priority (int): The priority of the task (1=High, 2=Medium, 3=Low).
        due_date (datetime.date): The due date of the task.
        created_at (datetime): The timestamp when the task was created.
        updated_at (datetime): The timestamp when the task was last updated.
        assigned_to (int): The ID of the user assigned to the task.
        project_id (int): The ID of the project the task belongs to.
    """
    
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    
    PRIORITY_HIGH = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_LOW = 3
    
    def __init__(self, title, description="", status=STATUS_PENDING, priority=PRIORITY_MEDIUM,
                 due_date=None, id=None, created_at=None, updated_at=None, assigned_to=None, project_id=None):
        """
        Initialize a Task object.
        
        Args:
            title (str): The title of the task.
            description (str, optional): The description of the task. Defaults to "".
            status (str, optional): The status of the task. Defaults to STATUS_PENDING.
            priority (int, optional): The priority of the task. Defaults to PRIORITY_MEDIUM.
            due_date (datetime.date, optional): The due date of the task. Defaults to None.
            id (int, optional): The unique identifier for the task. Defaults to None.
            created_at (datetime, optional): The timestamp when the task was created. Defaults to None.
            updated_at (datetime, optional): The timestamp when the task was last updated. Defaults to None.
            assigned_to (int, optional): The ID of the user assigned to the task. Defaults to None.
            project_id (int, optional): The ID of the project the task belongs to. Defaults to None.
        """
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.due_date = due_date
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.assigned_to = assigned_to
        self.project_id = project_id
    
    @classmethod
    def from_db_row(cls, row):
        """
        Create a Task object from a database row.
        
        Args:
            row (sqlite3.Row): A row from the database.
        
        Returns:
            Task: A Task object.
        """
        if not row:
            return None
        
        # Parse dates from string if they exist
        due_date = None
        if row['due_date']:
            try:
                due_date = datetime.strptime(row['due_date'], '%Y-%m-%d').date()
            except ValueError:
                pass
        
        created_at = None
        if row['created_at']:
            try:
                created_at = datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass
        
        updated_at = None
        if row['updated_at']:
            try:
                updated_at = datetime.strptime(row['updated_at'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass
        
        return cls(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            status=row['status'],
            priority=row['priority'],
            due_date=due_date,
            created_at=created_at,
            updated_at=updated_at,
            assigned_to=row['assigned_to'],
            project_id=row['project_id']
        )
    
    def to_dict(self):
        """
        Convert the Task object to a dictionary.
        
        Returns:
            dict: A dictionary representation of the Task.
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'assigned_to': self.assigned_to,
            'project_id': self.project_id
        }
    
    def __str__(self):
        """
        Return a string representation of the Task.
        
        Returns:
            str: A string representation of the Task.
        """
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}', priority={self.priority})"
    
    def __repr__(self):
        """
        Return a string representation of the Task for debugging.
        
        Returns:
            str: A string representation of the Task.
        """
        return self.__str__()
    
    def is_completed(self):
        """
        Check if the task is completed.
        
        Returns:
            bool: True if the task is completed, False otherwise.
        """
        return self.status == self.STATUS_COMPLETED
    
    def is_pending(self):
        """
        Check if the task is pending.
        
        Returns:
            bool: True if the task is pending, False otherwise.
        """
        return self.status == self.STATUS_PENDING
    
    def is_in_progress(self):
        """
        Check if the task is in progress.
        
        Returns:
            bool: True if the task is in progress, False otherwise.
        """
        return self.status == self.STATUS_IN_PROGRESS
    
    def is_high_priority(self):
        """
        Check if the task is high priority.
        
        Returns:
            bool: True if the task is high priority, False otherwise.
        """
        return self.priority == self.PRIORITY_HIGH
    
    def is_overdue(self):
        """
        Check if the task is overdue.
        
        Returns:
            bool: True if the task is overdue, False otherwise.
        """
        if not self.due_date:
            return False

        return self.due_date > datetime.now().date() and not self.is_completed()
    
    def complete(self):
        """
        Mark the task as completed.
        """
        self.status = self.STATUS_COMPLETED
        self.updated_at = datetime.now()
    
    def start(self):
        """
        Mark the task as in progress.
        """
        self.status = self.STATUS_IN_PROGRESS
        self.updated_at = datetime.now()
    
    def reset(self):
        """
        Reset the task to pending status.
        """
        self.status = self.STATUS_PENDING
        self.updated_at = datetime.now()