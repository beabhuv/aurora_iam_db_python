# __init__.py

# This is the initialization file for the `aurora_iam_db` package.
# It is automatically executed when the package is imported, and can be used to expose
# essential functions or classes to make them easier to import.

# Import necessary classes and functions to expose them at the package level
from .sync import AuroraIAMDatabase  # Import the synchronous class for database connections
from .asynch import AsyncAuroraIAMDatabase  # Import the asynchronous class for database connections

__all__ = ["AuroraIAMDatabase", "AsyncAuroraIAMDatabase"]  # Define what is exposed when the package is imported
