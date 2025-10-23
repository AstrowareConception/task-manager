# Task Management System

A command-line task management system that allows users to manage tasks, projects, and team members.

## Features

- User management (add, list, update, delete)
- Task management (add, list, update, delete, filter)
- Project management (add, list, update, delete)
- Task assignment to users and projects
- Task prioritization and status tracking
- Project timeline management
- Logging and error handling

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/AstrowareConception/task-manager.git
   cd task-manager
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Tutorial: Step-by-Step Commands

This tutorial provides a logical sequence of commands to learn and test the Task Management System. Follow these steps in order to build a complete workflow.

### 1. Setting Up Users

First, let's create some users who will work with our system.

#### 1.1. Create an admin user
```bash
python main.py user add --name "Admin User" --email "admin@example.com" --role "admin"
```
Expected output: A success message indicating the user was added.

#### 1.2. Create a project manager
```bash
python main.py user add --name "Project Manager" --email "manager@example.com" --role "manager"
```
Expected output: A success message indicating the user was added.

#### 1.3. Create team members
```bash
python main.py user add --name "John Doe" --email "john@example.com" --role "member"
python main.py user add --name "Jane Smith" --email "jane@example.com" --role "member"
```
Expected output: Success messages for each user added.

#### 1.4. List all users to verify
```bash
python main.py user list
```
Expected output:
```
Users:
  - Admin User (admin@example.com), Role: admin
  - Project Manager (manager@example.com), Role: manager
  - John Doe (john@example.com), Role: member
  - Jane Smith (jane@example.com), Role: member
```

### 2. Creating Projects

Now that we have users, let's create some projects.

#### 2.1. Create a website redesign project
```bash
python main.py project add --name "Website Redesign" --description "Redesign company website with modern UI" --start-date "2023-10-01" --end-date "2023-12-31" --manager "manager@example.com"
```
Expected output: A success message indicating the project was added.

#### 2.2. Create a mobile app project
```bash
python main.py project add --name "Mobile App Development" --description "Create a mobile app for customers" --start-date "2023-11-01" --end-date "2024-03-31" --manager "manager@example.com"
```
Expected output: A success message indicating the project was added.

#### 2.3. List all projects to verify
```bash
python main.py project list
```
Expected output:
```
Projects:
  - [1] Website Redesign
    Manager: Project Manager, Period: 2023-10-01 to 2023-12-31
    Description: Redesign company website with modern UI
  - [2] Mobile App Development
    Manager: Project Manager, Period: 2023-11-01 to 2024-03-31
    Description: Create a mobile app for customers
```

### 3. Creating and Assigning Tasks

Now let's create tasks for our projects and assign them to team members.

#### 3.1. Create tasks for the website redesign project

##### 3.1.1. Create a high-priority task
```bash
python main.py task add --title "Design Homepage Mockup" --description "Create mockups for the new homepage" --due-date "2023-10-15" --priority 1 --assigned-to "john@example.com" --project 1
```
Expected output: A success message indicating the task was added.

##### 3.1.2. Create a medium-priority task
```bash
python main.py task add --title "Implement Navigation Menu" --description "Create responsive navigation menu" --due-date "2023-10-30" --priority 2 --assigned-to "jane@example.com" --project 1
```
Expected output: A success message indicating the task was added.

#### 3.2. Create tasks for the mobile app project

##### 3.2.1. Create a task for John
```bash
python main.py task add --title "Design App Wireframes" --description "Create wireframes for all app screens" --due-date "2023-11-15" --priority 1 --assigned-to "john@example.com" --project 2
```
Expected output: A success message indicating the task was added.

##### 3.2.2. Create a task for Jane
```bash
python main.py task add --title "Implement User Authentication" --description "Create login and registration screens" --due-date "2023-11-30" --priority 2 --assigned-to "jane@example.com" --project 2
```
Expected output: A success message indicating the task was added.

#### 3.3. List all tasks to verify
```bash
python main.py task list
```
Expected output:
```
Tasks:
  - [1] Design Homepage Mockup (Priority: 1, Status: pending)
    Due: 2023-10-15, Assigned to: john@example.com, Project: Website Redesign
    Description: Create mockups for the new homepage
  - [2] Implement Navigation Menu (Priority: 2, Status: pending)
    Due: 2023-10-30, Assigned to: jane@example.com, Project: Website Redesign
    Description: Create responsive navigation menu
  - [3] Design App Wireframes (Priority: 1, Status: pending)
    Due: 2023-11-15, Assigned to: john@example.com, Project: Mobile App Development
    Description: Create wireframes for all app screens
  - [4] Implement User Authentication (Priority: 2, Status: pending)
    Due: 2023-11-30, Assigned to: jane@example.com, Project: Mobile App Development
    Description: Create login and registration screens
```

### 4. Filtering and Updating Tasks

Now let's explore how to filter tasks and update their status.

#### 4.1. Filter tasks by user
```bash
python main.py task list --user "john@example.com"
```
Expected output:
```
Tasks:
  - [1] Design Homepage Mockup (Priority: 1, Status: pending)
    Due: 2023-10-15, Assigned to: john@example.com, Project: Website Redesign
    Description: Create mockups for the new homepage
  - [3] Design App Wireframes (Priority: 1, Status: pending)
    Due: 2023-11-15, Assigned to: john@example.com, Project: Mobile App Development
    Description: Create wireframes for all app screens
```

#### 4.2. Filter tasks by project
```bash
python main.py task list --project 1
```
Expected output:
```
Tasks:
  - [1] Design Homepage Mockup (Priority: 1, Status: pending)
    Due: 2023-10-15, Assigned to: john@example.com, Project: Website Redesign
    Description: Create mockups for the new homepage
  - [2] Implement Navigation Menu (Priority: 2, Status: pending)
    Due: 2023-10-30, Assigned to: jane@example.com, Project: Website Redesign
    Description: Create responsive navigation menu
```

#### 4.3. Update task status to in-progress
```bash
python main.py task update --id 1 --status "in_progress"
```
Expected output: A success message indicating the task was updated.

#### 4.4. Reassign a task to another user
```bash
python main.py task update --id 2 --assigned-to "john@example.com"
```
Expected output: A success message indicating the task was updated.

#### 4.5. Mark a task as completed
```bash
python main.py task update --id 1 --status "completed"
```
Expected output: A success message indicating the task was updated.

#### 4.6. Filter tasks by status
```bash
python main.py task list --status "completed"
```
Expected output:
```
Tasks:
  - [1] Design Homepage Mockup (Priority: 1, Status: completed)
    Due: 2023-10-15, Assigned to: john@example.com, Project: Website Redesign
    Description: Create mockups for the new homepage
```

### 5. Advanced Workflow

Let's complete a full workflow by updating project details and managing multiple tasks.

#### 5.1. Update project end date
```bash
python main.py project update --id 1 --end-date "2024-01-31"
```
Note: This command is not implemented in the current version but would be a logical extension.

#### 5.2. Create a new task with dependencies
```bash
python main.py task add --title "Launch Website" --description "Deploy the redesigned website to production" --due-date "2024-01-15" --priority 1 --assigned-to "manager@example.com" --project 1
```
Expected output: A success message indicating the task was added.

#### 5.3. List all pending tasks
```bash
python main.py task list --status "pending"
```
Expected output: A list of all tasks with "pending" status.

#### 5.4. List all high-priority tasks
```bash
python main.py task list --priority 1
```
Note: This filtering option is not implemented in the current version but would be a logical extension.

## Project Structure

- `main.py`: Entry point for the application
- `config.py`: Configuration management
- `database.py`: Database operations
- `models/`: Data models
  - `user.py`: User model
  - `task.py`: Task model
  - `project.py`: Project model
- `services/`: Business logic
  - `user_service.py`: User management
  - `task_service.py`: Task management
  - `project_service.py`: Project management
- `utils/`: Utility functions
  - `logger.py`: Logging functionality
  - `validators.py`: Input validation

## Configuration

The application can be configured using a `config.json` file or environment variables. The following settings are available:

- `database_path`: Path to the SQLite database file
- `log_level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `log_file`: Path to the log file
- `max_tasks_per_user`: Maximum number of tasks per user
- `max_projects`: Maximum number of projects

Environment variables should be prefixed with `TASKMANAGER_`, e.g., `TASKMANAGER_LOG_LEVEL`.

## Error Handling

The application includes comprehensive error handling and logging. Errors are logged to both the console and a log file (if configured). The log format includes timestamps, log levels, and detailed error messages.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
