# Robot Framework

## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [How to Run](#how-to-run)
- [View results](#View-results)
- [Project Structure](#project-structure)

---
## 🔧 Prerequisites

- Python: Python 3.8 or higher is required.
- Git: Git is required to clone the repository.
- Selenium: Selenium 4.0 or higher is required.

## 📦  Installation
### Clone repository
```
git clone <your-repository-url>
cd '.\Robot Framework\'
```
###  Install dependecies
```
pip install -r requirements.txt
```
## How to run

### Run with custom output folder
```
robot --outputdir ./results test.robot
```
## View results
After test execution, open:
```markdown
results/report.html 
results/log.html 
results/output.xml
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