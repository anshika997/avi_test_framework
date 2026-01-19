import requests
import logging

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url, auth_manager):
        self.base_url = base_url
        self.auth_manager = auth_manager
    
    def get(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        headers = self.auth_manager.get_headers()
        
        if not headers:
            logger.error("No auth headers available")
            return None
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"GET {endpoint} failed: {e}")
            return None
    
    def put(self, endpoint, payload):
        url = f"{self.base_url}{endpoint}"
        headers = self.auth_manager.get_headers()
        
        if not headers:
            logger.error("No auth headers available")
            return None
        
        try:
            response = requests.put(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"PUT {endpoint} failed: {e}")
            return None
    
    def fetch_all_tenants(self):
        logger.info("Fetching all tenants...")
        data = self.get("/api/tenant")
        if data and 'results' in data:
            count = data.get('count', 0)
            logger.info(f"Total Tenants: {count}")
            return data['results']
        return []
    
    def fetch_all_virtual_services(self):
        logger.info("Fetching all virtual services...")
        data = self.get("/api/virtualservice")
        if data and 'results' in data:
            count = data.get('count', 0)
            logger.info(f"Total Virtual Services: {count}")
            return data['results']
        return []
    
    def fetch_all_service_engines(self):
        logger.info("Fetching all service engines...")
        data = self.get("/api/serviceengine")
        if data and 'results' in data:
            count = data.get('count', 0)
            logger.info(f"Total Service Engines: {count}")
            return data['results']
        return []
    
    def get_virtual_service_by_name(self, vs_name):
        all_vs = self.fetch_all_virtual_services()
        for vs in all_vs:
            if vs.get('name') == vs_name:
                logger.info(f"Found VS: {vs_name}")
                return vs
        logger.warning(f"VS not found: {vs_name}")
        return None
    
    def get_virtual_service(self, uuid):
        logger.info(f"Fetching Virtual Service with UUID: {uuid}")
        return self.get(f"/api/virtualservice/{uuid}")
    
    def update_virtual_service(self, uuid, payload):
        logger.info(f"Updating Virtual Service: {uuid}")
        return self.put(f"/api/virtualservice/{uuid}", payload)