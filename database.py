#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Database Module for Task Management System

This module provides database functionality for the Task Management System.
It handles database connection, initialization, and basic operations.
"""

import os
import sqlite3
import logging
from datetime import datetime

class Database:
    """Database manager for the Task Management System."""
    
    def __init__(self, db_path):
        """
        Initialize the database manager.
        
        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
        # Ensure the database directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize the database
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Establish a connection to the database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            self.cursor = self.conn.cursor()
            logging.debug(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            logging.error(f"Error connecting to database: {str(e)}")
            raise
    
    def _create_tables(self):
        """Create database tables if they don't exist."""
        try:
            # Create users table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    role TEXT NOT NULL DEFAULT 'member',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create projects table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    start_date DATE,
                    end_date DATE,
                    manager_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (manager_id) REFERENCES users (id)
                )
            ''')
            
            # Create tasks table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL DEFAULT 'pending',
                    priority INTEGER NOT NULL DEFAULT 2,
                    due_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    assigned_to INTEGER,
                    project_id INTEGER,
                    FOREIGN KEY (assigned_to) REFERENCES users (id),
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )
            ''')
            
            # Create comments table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    task_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (task_id) REFERENCES tasks (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            self.conn.commit()
            logging.debug("Database tables created successfully")
        except sqlite3.Error as e:
            logging.error(f"Error creating database tables: {str(e)}")
            raise
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            logging.debug("Database connection closed")
    
    def execute(self, query, params=None):
        """
        Execute a SQL query.
        
        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters for the query.
        
        Returns:
            The cursor object.
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor
        except sqlite3.Error as e:
            logging.error(f"Error executing query: {str(e)}")
            raise
    
    def fetch_one(self, query, params=None):
        """
        Execute a query and fetch one result.
        
        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters for the query.
        
        Returns:
            A single row or None if no results.
        """
        cursor = self.execute(query, params)
        return cursor.fetchone()
    
    def fetch_all(self, query, params=None):
        """
        Execute a query and fetch all results.
        
        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters for the query.
        
        Returns:
            A list of rows or an empty list if no results.
        """
        cursor = self.execute(query, params)
        return cursor.fetchall()
    
    def insert(self, table, data):
        """
        Insert data into a table.
        
        Args:
            table (str): The table name.
            data (dict): A dictionary of column names and values.
        
        Returns:
            The ID of the inserted row.
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        try:
            self.cursor.execute(query, tuple(data.values()))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            self.conn.rollback()
            logging.error(f"Error inserting data: {str(e)}")
            raise
    
    def update(self, table, data, condition):
        """
        Update data in a table.
        
        Args:
            table (str): The table name.
            data (dict): A dictionary of column names and values to update.
            condition (str): The WHERE clause.
        
        Returns:
            The number of rows affected.
        """
        set_clause = ', '.join([f"{column} = ?" for column in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        
        try:
            self.cursor.execute(query, tuple(data.values()))
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            self.conn.rollback()
            logging.error(f"Error updating data: {str(e)}")
            raise
    
    def delete(self, table, condition):
        """
        Delete data from a table.
        
        Args:
            table (str): The table name.
            condition (str): The WHERE clause.
        
        Returns:
            The number of rows affected.
        """
        query = f"DELETE FROM {table} WHERE {condition}"
        
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            self.conn.rollback()
            logging.error(f"Error deleting data: {str(e)}")
            raise
    
    def begin_transaction(self):
        """Begin a transaction."""
        self.conn.execute("BEGIN TRANSACATION")
    
    def commit(self):
        """Commit the current transaction."""
        self.conn.commit()
    
    def rollback(self):
        """Rollback the current transaction."""
        self.conn.rollback()