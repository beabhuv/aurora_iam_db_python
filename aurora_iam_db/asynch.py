import aiomysql
import asyncio
import boto3


class AsyncAuroraIAMDatabase:
    def __init__(self, db_host, db_name, db_user, region, ssl_ca_path,
                 pool_size=10, max_overflow=5, pool_recycle=900, pool_timeout=30,
                 retry_attempts=3, retry_delay=2):
        """
        Initializes the async database connection parameters.
        """
        self.db_host = db_host  # Aurora MySQL instance endpoint
        self.db_name = db_name  # Database name
        self.db_user = db_user  # Database username
        self.region = region  # AWS region for IAM authentication
        self.ssl_ca_path = ssl_ca_path  # Path to SSL certificate for encrypted connections
        self.pool_size = pool_size  # Connection pool size
        self.max_overflow = max_overflow  # Maximum overflow connections
        self.pool_recycle = pool_recycle  # Timeout before connections are recycled
        self.pool_timeout = pool_timeout  # Timeout for acquiring a connection
        self.retry_attempts = retry_attempts  # Retry attempts for connection
        self.retry_delay = retry_delay  # Delay between retry attempts
        self._pool = None  # To be initialized when connecting to the DB

    async def _generate_token(self):
        """
        Asynchronously generates an authentication token using AWS IAM for Aurora MySQL.
        This token is used instead of a password for connecting.
        """
        rds = boto3.client("rds", region_name=self.region)
        return rds.generate_db_auth_token(
            DBHostname=self.db_host,
            Port=3306,
            DBUsername=self.db_user,
            Region=self.region
        )

    async def _connect(self):
        """
        Establishes an asynchronous connection to the Aurora MySQL instance with retries.
        """
        token = await self._generate_token()  # Get the IAM token for authentication
        connect_args = {
            "ssl": {"ca": self.ssl_ca_path}  # SSL configuration for secure connection
        }

        # Try connecting with retries
        for attempt in range(1, self.retry_attempts + 1):
            try:
                # Create an asynchronous MySQL connection pool
                self._pool = await aiomysql.create_pool(
                    host=self.db_host,
                    port=3306,
                    user=self.db_user,
                    password=token,
                    db=self.db_name,
                    ssl=connect_args["ssl"],
                    minsize=self.pool_size,
                    maxsize=self.max_overflow,
                    autocommit=True,
                    loop=asyncio.get_event_loop(),
                )
                return self._pool
            except Exception as e:
                # If connection fails, log the error and retry if attempts are left
                if attempt == self.retry_attempts:
                    raise  # Re-raise exception after all retry attempts
                print(f"Connection attempt {attempt} failed: {e}")
                await asyncio.sleep(self.retry_delay)  # Wait before retrying

    async def execute_query(self, query):
        """
        Executes a SQL query on the Aurora MySQL database asynchronously and returns the results.
        """
        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query)  # Execute the query
                return await cur.fetchall()  # Return all results from the query
