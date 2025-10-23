#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project Service for Task Management System

This module provides the ProjectService class which implements business logic
for project management in the Task Management System.
"""

import logging
from datetime import datetime
from models.project import Project

class ProjectService:
    """Service class for project management."""
    
    def __init__(self, database):
        """
        Initialize the ProjectService.
        
        Args:
            database (Database): The database instance.
        """
        self.db = database
        self.logger = logging.getLogger(__name__)
    
    def add_project(self, project):
        """
        Add a new project to the system.
        
        Args:
            project (Project): The project to add.
        
        Returns:
            int: The ID of the newly added project.
        """
        # Prepare project data for database
        project_data = {
            'name': project.name,
            'description': project.description,
            'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else None,
            'end_date': project.end_date.strftime('%Y-%m-%d') if project.end_date else None,
            'manager_id': project.manager_id
        }
        
        try:
            project_id = self.db.insert('projects', project_data)
            project.id = project_id
            self.logger.info(f"Added project: {project.name} (ID: {project_id})")
            return project_id
        except Exception as e:
            self.logger.error(f"Error adding project: {str(e)}")
            raise
    
    def get_project_by_id(self, project_id):
        """
        Get a project by ID.
        
        Args:
            project_id (int): The ID of the project to retrieve.
        
        Returns:
            Project: The project with the specified ID, or None if not found.
        """
        try:
            row = self.db.fetch_one("SELECT * FROM projects WHERE id = ?", (project_id,))
            return Project.from_db_row(row)
        except Exception as e:
            self.logger.error(f"Error retrieving project by ID: {str(e)}")
            return None
    
    def get_all_projects(self):
        """
        Get all projects in the system.
        
        Returns:
            list: A list of Project objects.
        """
        try:
            rows = self.db.fetch_all("SELECT * FROM projects ORDER BY name")
            return [Project.from_db_row(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Error retrieving all projects: {str(e)}")
            return []
    
    def update_project(self, project):
        """
        Update an existing project.
        
        Args:
            project (Project): The project to update.
        
        Returns:
            bool: True if the update was successful, False otherwise.
        
        Raises:
            ValueError: If the project does not exist.
        """
        # Check if project exists
        existing_project = self.get_project_by_id(project.id)
        if not existing_project:
            raise ValueError(f"Project with ID {project.id} does not exist")
        
        # Update the project in the database
        project_data = {
            'name': project.name,
            'description': project.description,
            'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else None,
            'end_date': project.end_date.strftime('%Y-%m-%d') if project.end_date else None,
            'manager_id': project.manager_id
        }
        
        try:
            self.db.update('projects', project_data, f"id = {project.id}")
            self.logger.info(f"Updated project: {project.name} (ID: {project.id})")
            return True
        except Exception as e:
            self.logger.error(f"Error updating project: {str(e)}")
            return False
    
    def delete_project(self, project_id):
        """
        Delete a project from the system.
        
        Args:
            project_id (int): The ID of the project to delete.
        
        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            # Check if project exists
            project = self.get_project_by_id(project_id)
            if not project:
                self.logger.warning(f"Attempted to delete non-existent project with ID {project_id}")
                return False
            
            # Delete the project
            self.db.delete('projects', f"id = {project_id}")
            self.logger.info(f"Deleted project: {project.name} (ID: {project_id})")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting project: {str(e)}")
            return False
    
    def get_projects_by_manager(self, manager_id):
        """
        Get all projects managed by a specific user.
        
        Args:
            manager_id (int): The ID of the manager.
        
        Returns:
            list: A list of Project objects managed by the user.
        """
        try:
            rows = self.db.fetch_all("SELECT * FROM projects WHERE manager_id = ? ORDER BY name", (manager_id,))
            return [Project.from_db_row(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Error retrieving projects by manager: {str(e)}")
            return []
    
    def get_active_projects(self):
        """
        Get all currently active projects.
        
        Returns:
            list: A list of active Project objects.
        """
        today = datetime.now().date().strftime('%Y-%m-%d')
        try:
            # Get projects where:
            # 1. No start date is set, or start date is in the past
            # 2. No end date is set, or end date is in the future
            rows = self.db.fetch_all(
                """
                SELECT * FROM projects 
                WHERE (start_date IS NULL OR start_date <= ?) 
                AND (end_date IS NULL OR end_date >= ?)
                ORDER BY name
                """,
                (today, today)
            )
            return [Project.from_db_row(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Error retrieving active projects: {str(e)}")
            return []
    
    def get_completed_projects(self):
        """
        Get all completed projects (end date is in the past).
        
        Returns:
            list: A list of completed Project objects.
        """
        today = datetime.now().date().strftime('%Y-%m-%d')
        try:
            rows = self.db.fetch_all(
                "SELECT * FROM projects WHERE end_date < ? ORDER BY end_date DESC",
                (today,)
            )
            return [Project.from_db_row(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Error retrieving completed projects: {str(e)}")
            return []
    
    def get_upcoming_projects(self):
        """
        Get all upcoming projects (start date is in the future).
        
        Returns:
            list: A list of upcoming Project objects.
        """
        today = datetime.now().date().strftime('%Y-%m-%d')
        try:
            rows = self.db.fetch_all(
                "SELECT * FROM projects WHERE start_date > ? ORDER BY start_date",
                (today,)
            )
            return [Project.from_db_row(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Error retrieving upcoming projects: {str(e)}")
            return []