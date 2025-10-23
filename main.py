#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Task Management System - Main Entry Point

This module serves as the entry point for the Task Management System application.
It provides a command-line interface for users to interact with the system.
"""

import sys
import os
import argparse
from datetime import datetime

# Import local modules
from config import Config
from database import Database
from models.user import User
from models.task import Task
from models.project import Project
from services.user_service import UserService
from services.task_service import TaskService
from services.project_service import ProjectService
from utils.logger import Logger
from utils.validators import validate_email, validate_date

def setup_argparse():
    """Set up command line argument parsing."""
    parser = argparse.ArgumentParser(description='Task Management System')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # User commands
    user_parser = subparsers.add_parser('user', help='User management')
    user_subparsers = user_parser.add_subparsers(dest='user_command')
    
    # Add user
    add_user = user_subparsers.add_parser('add', help='Add a new user')
    add_user.add_argument('--name', required=True, help='User name')
    add_user.add_argument('--email', required=True, help='User email')
    add_user.add_argument('--role', default='member', choices=['admin', 'manager', 'member'], help='User role')
    
    # List users
    list_users = user_subparsers.add_parser('list', help='List all users')
    
    # Task commands
    task_parser = subparsers.add_parser('task', help='Task management')
    task_subparsers = task_parser.add_subparsers(dest='task_command')
    
    # Add task
    add_task = task_subparsers.add_parser('add', help='Add a new task')
    add_task.add_argument('--title', required=True, help='Task title')
    add_task.add_argument('--description', help='Task description')
    add_task.add_argument('--due-date', help='Due date (YYYY-MM-DD)')
    add_task.add_argument('--priority', type=int, choices=[1, 2, 3], default=2, help='Priority (1=High, 2=Medium, 3=Low)')
    add_task.add_argument('--assigned-to', help='User email to assign the task to')
    add_task.add_argument('--project', help='Project ID')
    
    # List tasks
    list_tasks = task_subparsers.add_parser('list', help='List all tasks')
    list_tasks.add_argument('--user', help='Filter by assigned user email')
    list_tasks.add_argument('--project', help='Filter by project ID')
    list_tasks.add_argument('--status', choices=['pending', 'in_progress', 'completed'], help='Filter by status')
    
    # Update task
    update_task = task_subparsers.add_parser('update', help='Update a task')
    update_task.add_argument('--id', required=True, help='Task ID')
    update_task.add_argument('--title', help='New task title')
    update_task.add_argument('--description', help='New task description')
    update_task.add_argument('--due-date', help='New due date (YYYY-MM-DD)')
    update_task.add_argument('--priority', type=int, choices=[1, 2, 3], help='New priority')
    update_task.add_argument('--status', choices=['pending', 'in_progress', 'completed'], help='New status')
    update_task.add_argument('--assigned-to', help='New user email to assign the task to')
    
    # Project commands
    project_parser = subparsers.add_parser('project', help='Project management')
    project_subparsers = project_parser.add_subparsers(dest='project_command')
    
    # Add project
    add_project = project_subparsers.add_parser('add', help='Add a new project')
    add_project.add_argument('--name', required=True, help='Project name')
    add_project.add_argument('--description', help='Project description')
    add_project.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    add_project.add_argument('--end-date', help='End date (YYYY-MM-DD)')
    add_project.add_argument('--manager', help='Project manager email')
    
    # List projects
    list_projects = project_subparsers.add_parser('list', help='List all projects')
    
    return parser

def main():
    """Main function to run the Task Management System."""
    # Initialize logger
    logger = Logger()
    logger.info("Starting Task Management System")
    
    # Load configuration
    config = Config()
    
    # Initialize database
    db = Database(config.get('database_path'))
    
    # Initialize services
    user_service = UserService(db)
    task_service = TaskService(db)
    project_service = ProjectService(db)
    
    # Parse command line arguments
    parser = setup_argparse()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Handle user commands
        if args.command == 'user':
            if args.user_command == 'add':
                if not validate_email(args.email):
                    logger.error(f"Invalid email format: {args.email}")
                    return
                
                user = User(name=args.name, email=args.email, role=args.role)
                user_service.add_user(user)
                logger.info(f"User added: {args.name} ({args.email})")
                
            elif args.user_command == 'list':
                users = user_service.get_all_users()
                if not users:
                    print("No users found.")
                else:
                    print("\nUsers:")
                    for user in users:
                        print(f"  - {user.name} ({user.email}), Role: {user.role}")
            else:
                parser.print_help()
        
        # Handle task commands
        elif args.command == 'task':
            if args.task_command == 'add':
                # Validate due date if provided
                due_date = None
                if args.due_date:
                    if not validate_date(args.dueDate):
                        logger.error(f"Invalid date format: {args.dueDate}. Use YYYY-MM-DD.")
                        return
                    due_date = datetime.strptime(args.dueDate, "%Y-%m-%d").date()
                
                # Validate assigned user if provided
                assigned_to = None
                if args.assigned_to:
                    if not validate_email(args.assigned_to):
                        logger.error(f"Invalid email format: {args.assigned_to}")
                        return
                    user = user_service.get_user_by_email(args.assigned_to)
                    if not user:
                        logger.error(f"User not found: {args.assigned_to}")
                        return
                    assigned_to = user.id
                
                # Validate project if provided
                project_id = None
                if args.project:
                    project = project_service.get_project_by_id(args.project)
                    if not project:
                        logger.error(f"Project not found: {args.project}")
                        return
                    project_id = project.id
                
                task = Task(
                    title=args.title,
                    description=args.description or "",
                    due_date=due_date,
                    priority=args.priority,
                    assigned_to=assigned_to,
                    project_id=project_id
                )
                task_service.add_task(task)
                logger.info(f"Task added: {args.title}")
                
            elif args.task_command == 'list':
                tasks = task_service.get_tasks(
                    user_email=args.user,
                    project_id=args.project,
                    status=args.status
                )
                if not tasks:
                    print("No tasks found.")
                else:
                    print("\nTasks:")
                    for task in tasks:
                        assigned_to = user_service.get_user_by_id(task.assigned_to).email if task.assigned_to else "Unassigned"
                        project = project_service.get_project_by_id(task.project_id).name if task.project_id else "No project"
                        due_date = task.due_date.strftime("%Y-%m-%d") if task.due_date else "No due date"
                        print(f"  - [{task.id}] {task.title} (Priority: {task.priority}, Status: {task.status})")
                        print(f"    Due: {due_date}, Assigned to: {assigned_to}, Project: {project}")
                        if task.description:
                            print(f"    Description: {task.description}")
            
            elif args.task_command == 'update':
                task = task_service.get_task_by_id(args.id)
                if not task:
                    logger.error(f"Task not found: {args.id}")
                    return
                
                # Update task fields if provided
                if args.title:
                    task.title = args.title
                if args.description:
                    task.description = args.description
                if args.due_date:
                    if not validate_date(args.due_date):
                        logger.error(f"Invalid date format: {args.due_date}. Use YYYY-MM-DD.")
                        return
                    task.due_date = datetime.strptime(args.due_date, "%Y-%m-%d").date()
                if args.priority:
                    task.priority = args.priority
                if args.status:
                    task.status = args.status
                if args.assigned_to:
                    if not validate_email(args.assigned_to):
                        logger.error(f"Invalid email format: {args.assigned_to}")
                        return
                    user = user_service.get_user_by_email(args.assigned_to)
                    if not user:
                        logger.error(f"User not found: {args.assigned_to}")
                        return
                    task.assigned_to = user.id
                
                task_service.update_task(task)
                logger.info(f"Task updated: {task.title}")
            
            else:
                parser.print_help()
        
        # Handle project commands
        elif args.command == 'project':
            if args.project_command == 'add':
                # Validate dates if provided
                start_date = None
                if args.start_date:
                    if not validate_date(args.start_date):
                        logger.error(f"Invalid date format: {args.start_date}. Use YYYY-MM-DD.")
                        return
                    start_date = datetime.strptime(args.start_date, "%Y-%m-%d").date()
                
                end_date = None
                if args.end_date:
                    if not validate_date(args.end_date):
                        logger.error(f"Invalid date format: {args.end_date}. Use YYYY-MM-DD.")
                        return
                    end_date = datetime.strptime(args.end_date, "%Y-%m-%d").date()
                
                # Validate manager if provided
                manager_id = None
                if args.manager:
                    if not validate_email(args.manager):
                        logger.error(f"Invalid email format: {args.manager}")
                        return
                    manager = user_service.get_user_by_email(args.manager)
                    if not manager:
                        logger.error(f"User not found: {args.manager}")
                        return
                    manager_id = manager.id
                
                project = Project(
                    name=args.name,
                    description=args.description or "",
                    start_date=start_date,
                    end_date=end_date,
                    manager_id=manager_id
                )
                project_service.add_project(project)
                logger.info(f"Project added: {args.name}")
                
            elif args.project_command == 'list':
                projects = project_service.get_all_projects()
                if not projects:
                    print("No projects found.")
                else:
                    print("\nProjects:")
                    for project in projects:
                        manager = user_service.get_user_by_id(project.manager_id).name if project.manager_id else "Unassigned"
                        start_date = project.start_date.strftime("%Y-%m-%d") if project.start_date else "Not set"
                        end_date = project.end_date.strftime("%Y-%m-%d") if project.end_date else "Not set"
                        print(f"  - [{project.id}] {project.name}")
                        print(f"    Manager: {manager}, Period: {start_date} to {end_date}")
                        if project.description:
                            print(f"    Description: {project.description}")
            
            else:
                parser.print_help()
        
        else:
            parser.print_help()
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())