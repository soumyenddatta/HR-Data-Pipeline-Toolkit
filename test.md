# 📂 Chapter 1: Toolkit Overview & Vision

> Focus on the **why** of the project.
> This chapter stays lean — only **vision, mission, and goals**.

### 1.1 Project Vision & Mission

* **Vision**: Bridge the gap between raw data and meaningful understanding by offering a scalable, educational HR data pipeline.
* **Mission**: Democratize data engineering by enabling anyone to simulate, explore, and learn from realistic HR data.

### 1.2 Who Is This Toolkit For?

* HR teams
* Developers & QA engineers
* Data analysts & BI specialists
* Educators & students

### 1.3 What Problems Does It Solve?

* Lack of accessible, realistic HR data for testing and learning
* Manual setup headaches for developers, educators, and analysts
* Need for a self-contained, reproducible data environment

### 1.4 Benefits of Using the Toolkit

* Generate realistic HR data at scale
* Learn SQL, Excel, and data workflows hands-on
* Build and test projects without risking sensitive data

---

# 📦 Chapter 2: Toolkit Structure & Setup

> Move **technical details** here — everything users need to **set up** the project.
> This becomes the **technical preface** for the toolkit.

### 2.1 System Requirements & Prerequisites

* Python 3.8+
* MySQL 8.0+
* Required Python libraries (`pip install -r requirements.txt`)
* Recommended: 4GB+ RAM, 2GB+ disk space

### 2.2 Directory Structure & File Roles

```
hr-data-pipeline/
├── main.py
├── script_for_sql_loading.py
├── script_to_CSV_from_sql.py
├── script_from_csv_to_excel.py
├── script_to_excel_from_sql.py
├── company_database_full.sql
├── README.md
├── dump/
│   ├── *.csv                # CSV exports per table
│   ├── output.xlsx          # Final Excel workbook
│   ├── process.log          # Logs from conversion scripts
│   ├── hr_er_diagram.png    # Visual ER diagram
```

### 2.3 Output Files & Formats

| File                        | Description                               |
| --------------------------- | ----------------------------------------- |
| `company_database_full.sql` | Full SQL script with HR schema & data     |
| `dump/*.csv`                | CSV exports per table                     |
| `dump/output.xlsx`          | Combined Excel from CSV/SQL               |
| `dump/process.log`          | Logs from export and conversion processes |

### 2.4 Installation Guide

```
git clone https://github.com/yourusername/hr-data-pipeline.git
cd hr-data-pipeline
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
```

### 2.5 MySQL Configuration Notes

* Update MySQL credentials (`MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`) in scripts.
* Ensure MySQL is running before using SQL-loading scripts.

### 2.6 ER Diagram: HR Database Schema Overview

> 📊 **Visualizing the Data Pipeline: The HR Database Schema**
>
> Understanding the relationships between tables is crucial for exploring and using the HR Data Pipeline Toolkit effectively.
> This ER diagram provides a clear, high-level overview of the core data model — illustrating how employees, departments, projects, and HR processes like payroll, bonuses, and training are interconnected.

#### ER Diagram (Mermaid Code)

```mermaid
erDiagram
    departments ||--o{ employees : has
    departments ||--o{ projects : has
    employees ||--o{ employee_project : assigned
    projects ||--o{ employee_project : includes

    employees ||--o{ attendance : logs
    employees ||--o{ bonuses : receives
    employees ||--o{ payroll : paid
    employees ||--o{ leaves : applies
    employees ||--o{ training : attends
    employees ||--o{ assets : assigned

    departments {
        int department_id PK
        varchar department_name
    }

    employees {
        int empID PK
        varchar employee_name
        int department_id FK
        ...
    }

    projects {
        int project_id PK
        int department_id FK
        ...
    }

    employee_project {
        int empID FK
        int project_id FK
        varchar role_in_project
        date assigned_date
    }

    attendance {
        int empID FK
        date date
        enum status
    }

    bonuses {
        int empID FK
        int hours_overtime
        int bonus_amount
        date bonus_date
    }

    payroll {
        int empID FK
        varchar month
        int base_salary
        ...
    }

    leaves {
        int empID FK
        enum leave_type
        date start_date
        date end_date
        enum status
    }

    training {
        int empID FK
        varchar training_name
        date start_date
        date end_date
        enum status
    }

    assets {
        int empID FK
        varchar asset_name
        varchar asset_type
        date purchase_date
        enum status
    }
```

#### ER Diagram (Visual)

![HR Database ER Diagram](./dump/hr_er_diagram.png)

---
