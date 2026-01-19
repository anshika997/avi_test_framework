import logging
from src.mock_components import MockSSH, MockRDP

logger = logging.getLogger(__name__)

class TestExecutor:
    def __init__(self, api_client):
        self.api_client = api_client
        self.test_results = []
    
    def run_test_case(self, test_case):
        logger.info(f"\n{'='*60}")
        logger.info(f"Running Test: {test_case['name']}")
        logger.info(f"{'='*60}\n")
        
        result = {
            'name': test_case['name'],
            'status': 'PASS',
            'stages': {}
        }
        
        try:
            if 'pre_fetch' in test_case['stages']:
                self.pre_fetcher()
                result['stages']['pre_fetch'] = 'PASS'
            
            if 'pre_validate' in test_case['stages']:
                vs_name = test_case['vs_name']
                vs_data = self.pre_validate(vs_name, test_case['expected'])
                if not vs_data:
                    result['status'] = 'FAIL'
                    result['stages']['pre_validate'] = 'FAIL'
                    return result
                result['stages']['pre_validate'] = 'PASS'
                result['vs_uuid'] = vs_data['uuid']
            
            if 'task_trigger' in test_case['stages']:
                success = self.task_trigger(result['vs_uuid'])
                result['stages']['task_trigger'] = 'PASS' if success else 'FAIL'
                if not success:
                    result['status'] = 'FAIL'
            
            if 'post_validate' in test_case['stages']:
                success = self.post_validate(result['vs_uuid'], test_case['expected'])
                result['stages']['post_validate'] = 'PASS' if success else 'FAIL'
                if not success:
                    result['status'] = 'FAIL'
            
            self.use_mock_components()
            
        except Exception as e:
            logger.error(f"Test execution failed with exception: {e}")
            result['status'] = 'FAIL'
            result['error'] = str(e)
        
        self.test_results.append(result)
        
        status_icon = "PASS" if result['status'] == 'PASS' else "FAIL"
        logger.info(f"\nTest '{test_case['name']}': {status_icon}\n")
        
        return result
    
    def pre_fetcher(self):
        logger.info("\nSTAGE 1: PRE-FETCHER")
        logger.info("-" * 40)
        self.api_client.fetch_all_tenants()
        self.api_client.fetch_all_virtual_services()
        self.api_client.fetch_all_service_engines()
        logger.info("Pre-fetcher completed\n")
    
    def pre_validate(self, vs_name, expected):
        logger.info("\nSTAGE 2: PRE-VALIDATION")
        logger.info("-" * 40)
        
        vs_data = self.api_client.get_virtual_service_by_name(vs_name)
        if not vs_data:
            logger.error(f"Virtual Service '{vs_name}' not found")
            return None
        
        uuid = vs_data.get('uuid')
        logger.info(f"VS UUID: {uuid}")
        
        vs_detail = self.api_client.get_virtual_service(uuid)
        if not vs_detail:
            logger.error("Failed to fetch VS details")
            return None
        
        is_enabled = vs_detail.get('enabled')
        expected_enabled = expected.get('pre_validate_enabled')
        
        logger.info(f"Current state: enabled={is_enabled}")
        logger.info(f"Expected state: enabled={expected_enabled}")
        
        if is_enabled == expected_enabled:
            logger.info(f"Pre-validation PASSED")
            return vs_detail
        else:
            logger.error(f"Pre-validation FAILED")
            return None
    
    def task_trigger(self, uuid):
        logger.info("\nSTAGE 3: TASK/TRIGGER")
        logger.info("-" * 40)
        logger.info(f"Action: Disabling Virtual Service")
        
        payload = {"enabled": False}
        result = self.api_client.update_virtual_service(uuid, payload)
        
        if not result:
            logger.error("Failed to update Virtual Service")
            return False
        
        is_enabled = result.get('enabled')
        if is_enabled == False:
            logger.info("Virtual Service disabled successfully")
            return True
        else:
            logger.error(f"Failed to disable VS. Current state: enabled={is_enabled}")
            return False
    
    def post_validate(self, uuid, expected):
        logger.info("\nSTAGE 4: POST-VALIDATION")
        logger.info("-" * 40)
        
        vs_detail = self.api_client.get_virtual_service(uuid)
        if not vs_detail:
            logger.error("Failed to fetch VS for post-validation")
            return False
        
        is_enabled = vs_detail.get('enabled')
        expected_enabled = expected.get('post_validate_enabled')
        
        logger.info(f"Current state: enabled={is_enabled}")
        logger.info(f"Expected state: enabled={expected_enabled}")
        
        if is_enabled == expected_enabled:
            logger.info(f"Post-validation PASSED")
            return True
        else:
            logger.error(f"Post-validation FAILED")
            return False
    
    def use_mock_components(self):
        logger.info("\nMOCK COMPONENTS DEMONSTRATION")
        logger.info("-" * 40)
        
        logger.info("\n--- SSH Demo ---")
        MockSSH.connect("192.168.1.100", "admin", "password123")
        MockSSH.execute_command("show virtualservice backend-vs-t1r_1000-1")
        MockSSH.disconnect()
        
        logger.info("\n--- RDP Demo ---")
        MockRDP.connect("192.168.1.101", "administrator", "admin@123")
        MockRDP.validate_connection("192.168.1.101")
        MockRDP.disconnect()
        
        logger.info("Mock components demo completed\n")