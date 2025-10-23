#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
User Service for Task Management System

This module provides the UserService class which implements business logic
for user management in the Task Management System.
"""

import logging
from models.user import User

class UserService:
    """Service class for user management."""
    
    def __init__(self, database):
        """
        Initialize the UserService.
        
        Args:
            database (Database): The database instance.
        """
        self.db = database
        self.logger = logging.getLogger(__name__)
    
    def add_user(self, user):
        """
        Add a new user to the system.
        
        Args:
            user (User): The user to add.
        
        Returns:
            int: The ID of the newly added user.
        
        Raises:
            ValueError: If a user with the same email already exists.
        """
        # Check if user with the same email already exists
        existing_user = self.get_user_by_email(user.email)
        if existing_user:
            raise ValueError(f"User with email '{user.email}' already exists")
        
        # Insert the user into the database
        user_data = {
            'name': user.name,
            'email': user.email,
            'role': user.role
        }
        
        try:
            user_id = self.db.insert('users', user_data)
            user.id = user_id
            self.logger.info(f"Added user: {user.name} ({user.email})")
            return user_id
        except Exception as e:
            self.logger.error(f"Error adding user: {str(e)}")
            raise
    
    def get_user_by_id(self, user_id):
        """
        Get a user by ID.
        
        Args:
            user_id (int): The ID of the user to retrieve.
        
        Returns:
            User: The user with the specified ID, or None if not found.
        """
        try:
            row = self.db.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
            return User.from_db_row(row)
        except Exception as e:
            self.logger.error(f"Error retrieving user by ID: {str(e)}")
            return None
    
    def get_user_by_email(self, email):
        """
        Get a user by email.
        
        Args:
            email (str): The email of the user to retrieve.
        
        Returns:
            User: The user with the specified email, or None if not found.
        """
        try:
            row = self.db.fetch_one("SELECT * FROM users WHERE email = ?", (email,))
            return User.from_db_row(row)
        except Exception as e:
            self.logger.error(f"Error retrieving user by email: {str(e)}")
            return None
    
    def get_all_users(self):
        """
        Get all users in the system.
        
        Returns:
            list: A list of User objects.
        """
        try:
            rows = self.db.fetch_all("SELECT * FROM users ORDER BY name")
            return [User.from_db_row(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Error retrieving all users: {str(e)}")
            return []
    
    def update_user(self, user):
        """
        Update an existing user.
        
        Args:
            user (User): The user to update.
        
        Returns:
            bool: True if the update was successful, False otherwise.
        
        Raises:
            ValueError: If the user does not exist or if trying to update to an email that is already in use.
        """
        # Check if user exists
        existing_user = self.get_user_by_id(user.id)
        if not existing_user:
            raise ValueError(f"User with ID {user.id} does not exist")
        
        # Check if email is being changed and if it's already in use
        if existing_user.email != user.email:
            email_check = self.get_user_by_email(user.email)
            if email_check:
                raise ValueError(f"Email '{user.email}' is already in use by another user")
        
        # Update the user in the database
        user_data = {
            'name': user.name,
            'email': user.email,
            'role': user.role
        }
        
        try:
            self.db.update('users', user_data, f"id = {user.id}")
            self.logger.info(f"Updated user: {user.name} ({user.email})")
            return True
        except Exception as e:
            self.logger.error(f"Error updating user: {str(e)}")
            return False
    
    def delete_user(self, user_id):
        """
        Delete a user from the system.
        
        Args:
            user_id (int): The ID of the user to delete.
        
        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            # Check if user exists
            user = self.get_user_by_id(user_id)
            if not user:
                self.logger.warning(f"Attempted to delete non-existent user with ID {user_id}")
                return False
            
            # Delete the user
            self.db.delete('users', f"id = {user_id}")
            self.logger.info(f"Deleted user: {user.nam} ({user.email})")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting user: {str(e)}")
            return False
    
    def get_users_by_role(self, role):
        """
        Get all users with a specific role.
        
        Args:
            role (str): The role to filter by.
        
        Returns:
            list: A list of User objects with the specified role.
        """
        try:
            rows = self.db.fetch_all("SELECT * FROM users WHERE role = ? ORDER BY name", (role,))
            return [User.from_db_row(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Error retrieving users by role: {str(e)}")
            return []