#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
User Model for Task Management System

This module defines the User class which represents a user in the system.
"""

from datetime import datetime

class User:
    """
    User class representing a user in the Task Management System.
    
    Attributes:
        id (int): The unique identifier for the user.
        name (str): The name of the user.
        email (str): The email address of the user.
        role (str): The role of the user (admin, manager, or member).
        created_at (datetime): The timestamp when the user was created.
    """
    
    def __init__(self, name, email, role='member', id=None, created_at=None):
        """
        Initialize a User object.
        
        Args:
            name (str): The name of the user.
            email (str): The email address of the user.
            role (str, optional): The role of the user. Defaults to 'member'.
            id (int, optional): The unique identifier for the user. Defaults to None.
            created_at (datetime, optional): The timestamp when the user was created. Defaults to None.
        """
        self.id = id
        self.name = name
        self.email = email
        self.role = role
        self.created_at = created_at or datetime.now()
    
    @classmethod
    def from_db_row(cls, row):
        """
        Create a User object from a database row.
        
        Args:
            row (sqlite3.Row): A row from the database.
        
        Returns:
            User: A User object.
        """
        if not row:
            return None
        
        return cls(
            id=row['id'],
            name=row['name'],
            email=row['email'],
            role=row['role'],
            created_at=datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S') if row['created_at'] else None
        )
    
    def to_dict(self):
        """
        Convert the User object to a dictionary.
        
        Returns:
            dict: A dictionary representation of the User.
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
    
    def __str__(self):
        """
        Return a string representation of the User.
        
        Returns:
            str: A string representation of the User.
        """
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role}')"
    
    def __repr__(self):
        """
        Return a string representation of the User for debugging.
        
        Returns:
            str: A string representation of the User.
        """
        return self.__str__()
    
    def is_admin(self):
        """
        Check if the user is an admin.
        
        Returns:
            bool: True if the user is an admin, False otherwise.
        """
        return self.role == 'admin'
    
    def is_manager(self):
        """
        Check if the user is a manager.
        
        Returns:
            bool: True if the user is a manager, False otherwise.
        """
        return self.role == 'manager'
    
    def can_manage_users(self):
        """
        Check if the user can manage other users.
        
        Returns:
            bool: True if the user can manage other users, False otherwise.
        """
        return self.is_admin()
    
    def can_manage_projects(self):
        """
        Check if the user can manage projects.
        
        Returns:
            bool: True if the user can manage projects, False otherwise.
        """
        return self.is_admin() or self.is_manager()