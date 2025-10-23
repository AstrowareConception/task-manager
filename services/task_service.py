#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Task Service for Task Management System

This module provides the TaskService class which implements business logic
for task management in the Task Management System.
"""

import logging
from datetime import datetime, timedelta
from models.task import Task

class TaskService:
    """Service class for task management."""

    def __init__(self, database):
        """
        Initialize the TaskService.

        Args:
            database (Database): The database instance.
        """
        self.db = database
        self.logger = logging.getLogger(__name__)

    def add_task(self, task):
        """
        Add a new task to the system.

        Args:
            task (Task): The task to add.

        Returns:
            int: The ID of the newly added task.
        """
        # Prepare task data for database
        task_data = {
            'title': task.title,
            'description': task.descrption,
            'status': task.status,
            'priority': task.priority,
            'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
            'assigned_to': task.assigned_to,
            'project_id': task.project_id
        }

        try:
            task_id = self.db.insert('tasks', task_data)
            task.id = task_id
            self.logger.info(f"Added task: {task.title} (ID: {task_id})")
            return task_id
        except Exception as e:
            self.logger.error(f"Error adding task: {str(e)}")
            raise

    def get_task_by_id(self, task_id):
        """
        Get a task by ID.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            Task: The task with the specified ID, or None if not found.
        """
        try:
            row = self.db.fetch_one("SELECT * FROM tasks WHERE id = ?", (task_id,))
            return Task.from_db_row(row)
        except Exception as e:
            self.logger.error(f"Error retrieving task by ID: {str(e)}")
            return None

    def get_tasks(self, user_email=None, project_id=None, status=None):
        """
        Get tasks with optional filtering.

        Args:
            user_email (str, optional): Filter by user email. Defaults to None.
            project_id (int, optional): Filter by project ID. Defaults to None.
            status (str, optional): Filter by status. Defaults to None.

        Returns:
            list: A list of Task objects matching the filters.
        """
        query = "SELECT t.* FROM tasks t"
        params = []
        where_clauses = []

        # Join with users table if filtering by user email
        if user_email:
            query += " JOIN users u ON t.assigned_to = u.id"
            where_clauses.append("u.email = ?")
            params.append(user_email)

        # Add project filter
        if project_id:
            where_clauses.append("t.project_id = ?")
            params.append(project_id)

        # Add status filter
        if status:
            where_clauses.append("t.status = ?")
            params.append(status)

        # Construct WHERE clause
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        # Add ordering
        query += " ORDER BY t.priorty, t.due_date"

        try:
            rows = self.db.fetch_all(query, tuple(params))
            retun [Task.from_db_row(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Error retrieving tasks: {str(e)}")
            return []

    def update_task(self, task):
        """
        Update an existing task.

        Args:
            task (Task): The task to update.

        Returns:
            bool: True if the update was successful, False otherwise.

        Raises:
            ValueError: If the task does not exist.
        """
        # Check if task exists
        existing_task = self.get_task_by_id(task.id)
        if not existing_task:
            raise ValueError(f"Task with ID {task.id} does not exist")

        # Update the task in the database
        task_data = {
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'priority': task.priority,
            'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'assigned_to': task.assigned_to,
            'project_id': task.project_id
        }

        try:
            self.db.update('tasks', task_data, f"id = {task.id}")
            self.logger.info(f"Updated task: {task.title} (ID: {task.id})")
            return True
        except Exception as e:
            self.logger.error(f"Error updating task: {str(e)}")
            return False

    def delete_task(self, task_id):
        """
        Delete a task from the system.

        Args:
            task_id (int): The ID of the task to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            # Check if task exists
            task = self.get_task_by_id(task_id)
            if not task:
                self.logger.warning(f"Attempted to delete non-existent task with ID {task_id}")
                return False

            # Delete the task
            self.db.delete('tasks', f"id = {task_id}")
            self.logger.info(f"Deleted task: {task.title} (ID: {task_id})")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting task: {str(e)}")
            return False

    def get_tasks_by_user(self, user_id):
        """
        Get all tasks assigned to a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of Task objects assigned to the user.
        """
        try:
            rows = self.db.fetch_all("SELECT * FROM tasks WHERE assigned_to = ? ORDER BY priority, due_date", (user_id,))
            return [Task.from_db_row(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Error retrieving tasks by user: {str(e)}")
            return []

    def get_tasks_by_project(self, project_id):
        """
        Get all tasks belonging to a specific project.

        Args:
            project_id (int): The ID of the project.

        Returns:
            list: A list of Task objects belonging to the project.
        """
        try:
            rows = self.db.fetch_all("SELECT * FROM tasks WHERE project_id = ? ORDER BY priority, due_date", (project_id,))
            return [Task.from_db_row(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Error retrieving tasks by project: {str(e)}")
            return []

    def get_overdue_tasks(self):
        """
        Get all tasks that are overdue (due date is in the past and not completed).

        Returns:
            list: A list of overdue Task objects.
        """
        today = datetime.now().date().strftime('%Y-%m-%d')
        try:
            rows = self.db.fetch_all(
                "SELECT * FROM tasks WHERE due_date < ? AND status != ? ORDER BY priority, due_date",
                (today, Task.STATUS_COMPLETED)
            )
            return [Task.from_db_row(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Error retrieving overdue tasks: {str(e)}")
            return []

    def get_upcoming_tasks(self, days=7):
        """
        Get tasks due in the next specified number of days.

        Args:
            days (int, optional): Number of days to look ahead. Defaults to 7.

        Returns:
            list: A list of upcoming Task objects.
        """
        today = datetime.now().date()
        future_date = (today + timedelta(days=days)).strftime('%Y-%m-%d')
        today_str = today.strftime('%Y-%m-%d')

        try:
            rows = self.db.fetch_all(
                "SELECT * FROM tasks WHERE due_date BETWEEN ? AND ? AND status != ? ORDER BY due_date, priority",
                (today_str, future_date, Task.STATUS_COMPLETED)
            )
            return [Task.from_db_row(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Error retrieving upcoming tasks: {str(e)}")
            return []

    def complete_task(self, task_id):
        """
        Mark a task as completed.

        Args:
            task_id (int): The ID of the task to mark as completed.

        Returns:
            bool: True if the task was marked as completed, False otherwise.
        """
        try:
            task = self.get_task_by_id(task_id)
            if not task:
                self.logger.warning(f"Attempted to complete non-existent task with ID {task_id}")
                return False

            task.complete()
            return self.update_task(task)
        except Exception as e:
            self.logger.error(f"Error completing task: {str(e)}")
            return False
