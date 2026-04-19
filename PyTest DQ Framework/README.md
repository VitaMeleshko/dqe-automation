# PyTest DQ Framework
Data Quality testing framework built with PyTest for validating ETL transformations between PostgreSQL and Parquet data formats
## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Configuration Files](#configuration-files)
- [Running Tests](#running-tests)
- [Generated Reports](#generated-reports)
- [Test Markers](#test-markers)

---
## 🔧 Prerequisites

- Python: Python 3.8 or higher is required.
- Git: Git is required to clone the repository.


## 📦 Installation

### Step 1: Create Virtual Environment

#### Navigate to project directory
```
cd "PyTest DQ Framework"
```
#### Create virtual environment
```
python -m venv venv
```
#### Activate virtual environment
```
.\venv\Scripts\Activate.ps1
```
### Step 2: Install Dependencies
_Make sure virtual environment is activated_
```
pip install -r requirements.txt
```
### Step 3: Verify Installation

```
pytest --version 
```
```
pip list
```

## Project Structure
```markdown
PyTest DQ Framework/
├── Jenkinsfile                      # CI/CD pipeline definition
├── requirements.txt                 # Python dependencies
├── README.md                        
│
├── src/                             # Source code
│   ├── __init__.py
│   ├── connectors/                  # Data connectors
│   │   ├── __init__.py
│   │   ├── file_system/
│   │   │   ├── __init__.py
│   │   │   └── parquet_reader.py   # Parquet file reader
│   │   └── postgres/
│   │       ├── __init__.py
│   │       └── postgres_connector.py # PostgreSQL connector
│   │
│   └── data_quality/                # Validation library
│       ├── __init__.py
│       └── data_quality_validation_library.py
│
└── tests/                           # Test suite
    ├── __init__.py
    ├── conftest.py                  # PyTest configuration
    ├── pytest.ini                   # PyTest settings
    ├── test_examples.py             # Example tests
    │
    └── dq checks/                   # Data quality tests
        ├── __init__.py
        └── parquet_files/
            ├── __init__.py
            └── test_facility_name_min_time_spent_per_visit_date.py
```
## Configuration
### Database Connection
```
--db_host       # Database hostname (default: localhost)
--db_port       # Database port (default: 5434)
--db_name       # Database name (default: mydatabase)
--db_user       # Database username (REQUIRED)
--db_password   # Database password (REQUIRED)
```
### Jenkins Credentials
1. Manage Jenkins → Credentials → Global
2. Add Credentials:
```
Kind: Username with password
ID: jenkins-postgres-credentials
Username: myuser
Password: mypassword
```
## Configuration Files


### pytest.ini

**Purpose:** Defines custom markers and default PyTest options.

**Key configurations:**
- **Markers:** Custom labels for test categorization
- **python_files:** Pattern for test file discovery (`test_*.py`)
- **addopts:** Default command-line options (verbose, HTML reports)

### conftest.py

**Purpose:** Contains shared fixtures and hooks for all tests.

#### Fixtures:
##### Session scope:
**1. `db_connection`** PostgreSQL database connection\
**2. `parquet_reader`** ParquetReader instance for reading Parquet files\
**3. `data_quality_library`** DataQualityLibrary instance with validation methods.\
##### Module scope:
**4. `source_data`** loads source data  fro PostgreSQL database\
**5. `target_data`** loads target data from parquet file

## Jenkins Pipeline
### Jenkinsfile
#### Overview
The pipeline consists of 2 stages:
1. Setup & Test: Installs dependencies and runs tests
2. Archive Test Report: Saves HTML report as Jenkins artifact

#### Trigger Build
1. Open Jenkins: http://localhost:8080
2. Navigate to PyTest-DQ-Framework job
3. Click Build Now 
#### View Results
* Console Output: Real-time test execution log
* PyTest DQ Report: HTML report in build artifacts
* Test Trends: Historical pass/fail statistics