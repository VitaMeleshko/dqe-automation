# Selenium Introduction
This project automates a local HTML report using Selenium (Python) 
## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [How to Run](#how-to-run)
- [Project Structure](#project-structure)

---
## 🔧 Prerequisites

- Python: Python 3.8 or higher is required.
- Git: Git is required to clone the repository.
- Google Chrome installed
- Selenium: Selenium 4.0 or higher is required.

## 📦  Installation
```
pip install selenium
```
## How to run

### 1. Put your HTML report here:
```
generated_report/report.html
```
### 2. Run the script:
```
python main.py
```
### 3. Check outputs in:
```
result/
```
## Project Structure
```markdown
Selenium Introduction/
├─ generated_report/
│ └─ report.html
├─ result/ # created automatically
│ ├─ table.csv
│ ├─ doughnut0.csv
│ ├─ doughnut1.csv
│ ├─ screenshot0.png
│ └─ screenshot1.png
└─ main.py
```