"""
repositories.py - Raw SQL data-access layer for Tales of Time.

Each repository class is responsible for one entity's persistence.
All SQL is parameterised (? placeholders) - never string-formatted -
which prevents SQL injection.

JOIN queries are written explicitly here so the service and view layers
never need to know about foreign keys or table relationships.
"""