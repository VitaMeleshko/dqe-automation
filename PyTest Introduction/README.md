# PyTest Introduction

## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Project Structure](#project-structure)
- [Configuration Files](#configuration-files)
- [Running Tests](#running-tests)
- [Generated Reports](#generated-reports)
- [Test Markers](#test-markers)

---
## 🔧 Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

## 📦 Installation

### Step 1: Create Virtual Environment

#### Navigate to project directory
```
cd "PyTest Introduction"
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
PyTest Introduction
├── README.md # This file
├── requirements.txt # Python dependencies
├── src/
│ └── data/
│ │ └── data.csv # Test data file
└── tests/
│ ├── test_csv/
│ │ └── test_csv_file.py # Test cases
│ ├── conftest.py # PyTest configuration and fixtures
│ └── pytest.ini # PyTest settings
├── reports/ # Generated HTML reports
```
---

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
**1. `csv_data`** automatically injects CSV data\
**2. `expected_schema`** provides expected schema for validation
#### Hooks:
**`pytest_collection_modifyitems`** enables filtering tests without explicit markers

## Running Tests

All commands should be executed from the project root directory (PyTest Introduction/).

1. **Run Tests unmarked tests**

```
pytest tests/ -m unmarked --html=reports/report_unmarked.html -v 
```
2. **Run Tests with validate_csv and not xfail**
```
pytest tests/ -m "validate_csv and not xfail" --html=reports/report_validate_csv.html -v
```
3. **Run All Tests**

```
pytest tests/ --html=reports/report_all.html -v
```
## Generated Reports
After running tests, HTML reports are generated in reports/ directory:
```markdown
reports/
├── report_unmarked.html         # Unmarked tests results
├── report_validate_csv.html     # validate_csv tests results
├── report_all.html              # All tests results
└── assets/                       # (Optional) CSS and JS files
│ ├── style.css
│ └── main.js
```
## Assets Folder

Reports with Assets Folder with separate CSS/JS files

## Viewing Reports
_Open in default browser_

```
start .\reports\report_all.html
```
```
start .\reports\report_validate_csv.html 
```
```
start .\reports\report_unmarked.html 
```

## Test Markers
The project uses the following PyTest markers:

| Marker       |                  	Description                   |
|:-------------|:-----------------------------------------------:|
| validate_csv |       Marks tests as CSV validation tests       |
| skip	        |            Marks tests to be skipped            |
| xfail	       |          Marks tests expected to fail           |
| unmarked     | Auto-assigned to tests without explicit markers |

