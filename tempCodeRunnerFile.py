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