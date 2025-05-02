import pytest
from unittest.mock import patch, MagicMock
from aurora_iam_db.sync import AuroraIAMDatabase


@pytest.fixture
def db_config():
    """
    Fixture to provide the database configuration parameters.
    This allows us to reuse the configuration in multiple test functions.
    """
    return {
        "db_host": "test-host",  # Mocked DB Host
        "db_name": "test-db",  # Mocked DB Name
        "db_user": "test-user",  # Mocked DB User
        "region": "us-east-1",  # AWS Region
        "ssl_ca_path": "/path/to/ssl.pem"  # Path to SSL certificate for secure connections
    }


@patch("aurora_iam_db.sync.boto3")
def test_generate_token(mock_boto3, db_config):
    """
    Test the generation of the IAM token using boto3.
    We mock the boto3 client to avoid actual AWS calls during the test.
    """
    # Mock the return value of the generate_db_auth_token method
    mock_boto3.client.return_value.generate_db_auth_token.return_value = "mock-token"

    # Create an instance of the AuroraIAMDatabase class
    db = AuroraIAMDatabase(**db_config)

    # Call the _generate_token method to test if it returns the mocked token
    token = db._generate_token()

    # Verify that the returned token matches the mocked token
    assert token == "mock-token"


@patch("aurora_iam_db.sync.create_engine")
@patch("aurora_iam_db.sync.boto3")
def test_connect_success(mock_boto3, mock_create_engine, db_config):
    """
    Test the connection to the Aurora MySQL database.
    This test checks if the connection engine is created successfully.
    We mock the engine creation to avoid actual DB interaction.
    """
    # Mock the return value of the generate_db_auth_token method
    mock_boto3.client.return_value.generate_db_auth_token.return_value = "mock-token"

    # Mock the SQLAlchemy engine object
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine

    # Create an instance of the AuroraIAMDatabase class
    db = AuroraIAMDatabase(**db_config)

    # Call the _connect method to establish a connection
    engine = db._connect()

    # Verify that the engine returned is the mocked engine
    assert engine == mock_engine


@patch("aurora_iam_db.sync.create_engine", side_effect=Exception("Connection failed"))
@patch("aurora_iam_db.sync.boto3")
def test_connect_retry(mock_boto3, mock_create_engine, db_config):
    """
    Test the connection with retries. This test simulates a connection failure,
    and the system should retry based on the configured retry logic.
    """
    # Mock the return value of the generate_db_auth_token method
    mock_boto3.client.return_value.generate_db_auth_token.return_value = "mock-token"

    # Update the db_config to have a limited number of retries and short delay
    db_config.update({"retry_attempts": 2, "retry_delay": 0.1})

    # Create an instance of the AuroraIAMDatabase class
    db = AuroraIAMDatabase(**db_config)

    # Use pytest's `raises` to assert that the exception is raised after retries
    with pytest.raises(Exception, match="Connection failed"):
        db._connect()

