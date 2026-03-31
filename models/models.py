"""
models.py - Raw SQL schema and database connection for Tales of Time.

Replaces SQLAlchemy ORM entirely. Responsibilities:
  - Define the database connection factory
  - Define and create all 13 tables via raw DDL SQL
  - Provide a single get_db() function consumed by repositories

No ORM classes, no session management, no db.Model inheritance.
"""

