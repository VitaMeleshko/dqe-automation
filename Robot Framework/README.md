# Robot Framework

## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [How to Run](#how-to-run)
- [Project Structure](#project-structure)

---
## 🔧 Prerequisites

- Python: Python 3.8 or higher is required.
- Git: Git is required to clone the repository.
- Selenium: Selenium 4.0 or higher is required.

## 📦  Installation
### Install Robot Framework
```
pip install robotframework
```
###  Install SeleniumLibrary (for web testing)
```
pip install robotframework-seleniumlibrary
```
###  Install DatabaseLibrary (for database testing)
```
pip install robotframework-databaselibrary
```
###  Install RequestsLibrary (for API testing)
```
pip install robotframework-requests
```
###  Install Robot Framework IDE Support
#### VS Code extensions like
```
Robot Framework Language Server
```
#### PyCharm plugin: 
```
Robot Framework Support
```
### 1. Put your HTML report here:
```
generated_report/report.html
```
### 2. Run the script:
```
robot --outputdir ./results test.robot
```
### 3. Check outputs in:
```
result/
```
## Project Structure
```markdown
Robot Framework/
│
├── test.robot              # Main test file
├── helper.py              # Python functions
├── report.html            # HTML file with table
├── requirements.txt       # Dependencies
│
├── parquet_data/          # Folder with Parquet files
│   └── facility_type_avg_time_spent_per_visit_date/
│
└── results/               # Test results (auto-generated)
    ├── log.html
    ├── output.xml
    └── report.html
```