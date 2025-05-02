import boto3
from sqlalchemy import create_engine
import time
import logging

class AuroraIAMDatabase:
    def __init__(self, db_host, db_name, db_user, region, ssl_ca_path,
                 pool_size=10, max_overflow=5, pool_recycle=900, pool_timeout=30,
                 retry_attempts=3, retry_delay=2):
        """
        Initializes the database connection parameters.
        """
        self.db_host = db_host  # Aurora MySQL instance endpoint
        self.db_name = db_name  # Database name
        self.db_user = db_user  # Database username
        self.region = region    # AWS region for IAM authentication
        self.ssl_ca_path = ssl_ca_path  # Path to SSL certificate for encrypted connections
        self.pool_size = pool_size  # Connection pool size
        self.max_overflow = max_overflow  # Maximum overflow connections
        self.pool_recycle = pool_recycle  # Timeout before connections are recycled
        self.pool_timeout = pool_timeout  # Timeout for acquiring a connection
        self.retry_attempts = retry_attempts  # Retry attempts for connection
        self.retry_delay = retry_delay  # Delay between retry attempts
        self._engine = self._connect()  # Initialize the connection engine

    def _generate_token(self):
        """
        Generates an authentication token using AWS IAM for Aurora MySQL.
        This token is used instead of a password for connecting.
        """
        rds = boto3.client("rds", region_name=self.region)
        return rds.generate_db_auth_token(
            DBHostname=self.db_host,
            Port=3306,
            DBUsername=self.db_user,
            Region=self.region
        )

    def _connect(self):
        """
        Establishes the connection to the Aurora MySQL instance with retries.
        """
        token = self._generate_token()  # Get the IAM token for authentication
        connect_args = {
            "ssl": {"ca": self.ssl_ca_path}  # SSL configuration for secure connection
        }

        # Try connecting with retries
        for attempt in range(1, self.retry_attempts + 1):
            try:
                # Create the SQLAlchemy engine with the authentication token
                engine = create_engine(
                    f"mysql+pymysql://{self.db_user}:{token}@{self.db_host}:3306/{self.db_name}",
                    pool_size=self.pool_size,
                    max_overflow=self.max_overflow,
                    pool_recycle=self.pool_recycle,
                    pool_timeout=self.pool_timeout,
                    connect_args=connect_args,
                )
                # Test the connection by executing a simple query
                with engine.connect() as conn:
                    conn.execute("SELECT 1")  # Simple test query
                return engine
            except Exception as e:
                # If connection fails, log the error and retry if attempts are left
                if attempt == self.retry_attempts:
                    raise  # Re-raise exception after all retry attempts
                logging.warning(f"Connection attempt {attempt} failed: {e}")
                time.sleep(self.retry_delay)  # Wait before retrying

    def execute_query(self, query):
        """
        Executes a SQL query on the Aurora MySQL database and returns the results.
        """
        with self._engine.connect() as conn:
            result = conn.execute(query)  # Execute the query
            return result.fetchall()  #
