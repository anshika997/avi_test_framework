import requests
import base64
import logging

logger = logging.getLogger(__name__)

class AuthManager:
    def __init__(self, base_url, credentials):
        self.base_url = base_url
        self.username = credentials['username']
        self.password = credentials['password']
        self.token = None
    
    def register(self):
        url = f"{self.base_url}/register"
        payload = {
            "username": self.username,
            "password": self.password
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 201:
                logger.info("Registration successful")
                return True
            elif response.status_code == 409:
                logger.info("User already registered")
                return True
            else:
                logger.warning(f"Registration response: {response.status_code}")
                return True
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return False
    
    def login(self):
        endpoints_to_try = ["/login1", "/login", "/api/login"]
        
        for endpoint in endpoints_to_try:
            url = f"{self.base_url}{endpoint}"
            logger.info(f"Trying login endpoint: {endpoint}")
            
            credentials = f"{self.username}:{self.password}"
            encoded = base64.b64encode(credentials.encode()).decode()
            headers = {"Authorization": f"Basic {encoded}"}
            
            try:
                response = requests.post(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    self.token = data.get('token')
                    if self.token:
                        logger.info(f"Login successful using endpoint: {endpoint}")
                        return self.token
                    else:
                        logger.warning(f"No token in response from {endpoint}")
                elif response.status_code == 404:
                    logger.debug(f"Endpoint {endpoint} not found, trying next...")
                    continue
                else:
                    logger.error(f"Login failed with status {response.status_code}: {response.text}")
                    
            except requests.exceptions.Timeout:
                logger.error(f"Timeout on {endpoint}")
                continue
            except Exception as e:
                logger.error(f"Error on {endpoint}: {e}")
                continue
        
        logger.error("All login endpoints failed")
        return None
    
    def get_headers(self):
        if not self.token:
            logger.error("No token available")
            return None
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
