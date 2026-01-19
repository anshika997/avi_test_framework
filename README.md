# AVI Load Balancer Test Automation Framework

## Overview
Python-based modular test automation framework for VMware AVI Load Balancer API testing.

## Prerequisites
- Python 3.7 or higher
- pip
- Internet connection

## Installation

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Update credentials in config/api_config.yaml

## Running Tests
```
python main.py
```

## Project Structure
```
avi_test_framework/
├── config/
│   ├── api_config.yaml
│   └── test_cases.yaml
├── src/
│   ├── __init__.py
│   ├── utils.py
│   ├── auth_manager.py
│   ├── api_client.py
│   ├── mock_components.py
│   └── test_executor.py
├── logs/
├── main.py
├── requirements.txt
└── README.md
```

## Test Workflow

1. Pre-Fetcher: Fetch all resources
2. Pre-Validation: Verify initial state
3. Task/Trigger: Execute action
4. Post-Validation: Verify final state

## Logs

Logs are saved to logs/test_execution.log
```

---

## How to Set Up and Run

### Step 1: Create Folders
```
mkdir avi_test_framework
cd avi_test_framework
mkdir config
mkdir src
mkdir logs
```

### Step 2: Create All Files

Copy each code section above into corresponding files.

### Step 3: Install Dependencies
```
pip install -r requirements.txt
```

### Step 4: Update Configuration

Open config/api_config.yaml and change:
- username
- password

### Step 5: Run
```
python main.py