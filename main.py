import threading
import logging
from src.utils import load_yaml, setup_logging
from src.auth_manager import AuthManager
from src.api_client import APIClient
from src.test_executor import TestExecutor

def run_single_test(api_client, test_case):
    executor = TestExecutor(api_client)
    result = executor.run_test_case(test_case)
    return result

def main():
    print("\n" + "="*60)
    print("AVI LOAD BALANCER TEST AUTOMATION FRAMEWORK")
    print("="*60 + "\n")
    
    print("Loading configuration files...")
    api_config = load_yaml('config/api_config.yaml')
    test_cases_config = load_yaml('config/test_cases.yaml')
    
    if not api_config or not test_cases_config:
        print("Failed to load configuration files. Exiting.")
        return
    
    print("Configuration loaded successfully\n")
    
    logger = setup_logging(api_config)
    logger.info("="*60)
    logger.info("Starting AVI Test Framework")
    logger.info("="*60 + "\n")
    
    logger.info("Initiating authentication...")
    auth_manager = AuthManager(api_config['api']['base_url'], api_config['credentials'])
    
    logger.info("Attempting registration...")
    auth_manager.register()
    
    logger.info("Logging in...")
    token = auth_manager.login()
    
    if not token:
        logger.error("Authentication failed. Cannot proceed.")
        return
    
    logger.info("Authentication successful\n")
    
    api_client = APIClient(api_config['api']['base_url'], auth_manager)
    logger.info("API Client initialized\n")
    
    test_cases = test_cases_config['test_cases']
    threads = []
    results = []
    
    logger.info(f"Preparing to run {len(test_cases)} test case(s) in parallel...")
    logger.info("="*60 + "\n")
    
    for test_case in test_cases:
        thread = threading.Thread(
            target=lambda tc=test_case: results.append(run_single_test(api_client, tc))
        )
        threads.append(thread)
        thread.start()
        logger.info(f"Started thread for: {test_case['name']}")
    
    logger.info(f"\nWaiting for all threads to complete...\n")
    
    for thread in threads:
        thread.join()
    
    logger.info("\n" + "="*60)
    logger.info("TEST EXECUTION SUMMARY")
    logger.info("="*60)
    
    passed = 0
    failed = 0
    
    for result in results:
        status_icon = "PASS" if result['status'] == 'PASS' else "FAIL"
        logger.info(f"{status_icon} - {result['name']}: {result['status']}")
        
        for stage, status in result.get('stages', {}).items():
            logger.info(f"  {stage}: {status}")
        
        if result['status'] == 'PASS':
            passed += 1
        else:
            failed += 1
    
    logger.info("="*60)
    logger.info(f"Passed: {passed}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Total: {len(results)}")
    logger.info("="*60 + "\n")
    
    logger.info("Test execution completed!")
    logger.info(f"Detailed logs saved to: {api_config['logging']['file']}\n")

if __name__ == "__main__":
    main()