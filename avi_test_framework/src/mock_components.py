import logging

logger = logging.getLogger(__name__)

class MockSSH:
    @staticmethod
    def connect(host, username, password=None):
        logger.info(f"MOCK_SSH: Connecting to {host} as {username}...")
        logger.info(f"MOCK_SSH: Connection established to {host}")
        return True
    
    @staticmethod
    def execute_command(command):
        logger.info(f"MOCK_SSH: Executing command: '{command}'")
        mock_output = f"MOCK_OUTPUT: Command '{command}' executed successfully"
        logger.info(f"{mock_output}")
        return mock_output
    
    @staticmethod
    def disconnect():
        logger.info("MOCK_SSH: Disconnecting...")
        logger.info("MOCK_SSH: Disconnected successfully")
        return True

class MockRDP:
    @staticmethod
    def connect(host, username, password=None):
        logger.info(f"MOCK_RDP: Initiating RDP connection to {host}...")
        logger.info(f"MOCK_RDP: Logging in as {username}")
        logger.info(f"MOCK_RDP: Connected to {host}")
        return True
    
    @staticmethod
    def validate_connection(host):
        logger.info(f"MOCK_RDP: Validating remote connection to {host}...")
        logger.info(f"MOCK_RDP: Checking network connectivity...")
        logger.info(f"MOCK_RDP: Verifying RDP service...")
        logger.info(f"MOCK_RDP: Validation successful for {host}")
        return True
    
    @staticmethod
    def disconnect():
        logger.info("MOCK_RDP: Closing remote desktop session...")
        logger.info("MOCK_RDP: Disconnected successfully")
        return True