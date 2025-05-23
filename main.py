from tqdm import tqdm
import random
from faker import Faker
from datetime import date, timedelta, datetime

fake = Faker()
departments = ['IT', 'HR', 'Finance', 'Marketing', 'Sales', 'Operations', 'R&D', 'Security']
roles = ['Developer', 'Manager', 'Analyst', 'Lead', 'Executive']
marital_status_options = ['Married', 'Single', 'Non-married']
genders = ['Male', 'Female']
statuses = ['Active', 'Completed', 'On Hold', 'Cancelled']
leave_types = ['Casual', 'Sick', 'Paid', 'Unpaid']
training_statuses = ['Completed', 'Ongoing', 'Not Started']
asset_types = ['Laptop', 'Mobile', 'Access Card', 'Monitor', 'Keyboard', 'Mouse', 'Mac']
asset_statuses = ['Issued', 'Returned', 'Lost']
benefits = ['Health Insurance', 'Stock Options', 'Paid Vacation', 'Gym Membership', 'Transport Allowance']
leave_statuses = ['Approved', 'Rejected', 'Pending']
months = [datetime(2023, m, 1).strftime('%B %Y') for m in range(1, 13)]

with open('company_database_full.sql', 'w') as f:
    f.write("CREATE DATABASE IF NOT EXISTS company_db;\nUSE company_db;\n\n")

    # Departments
    f.write("CREATE TABLE departments (department_id INT PRIMARY KEY AUTO_INCREMENT, department_name VARCHAR(50) UNIQUE);\n")
    for dept in departments:
        f.write(f"INSERT INTO departments (department_name) VALUES ('{dept}');\n")

    # Employees
    f.write("""
CREATE TABLE employees (
  empID INT PRIMARY KEY AUTO_INCREMENT,
  employee_name VARCHAR(50),
  age INT,
  gender ENUM('Male', 'Female'),
  date_of_birth DATE,
  date_of_joining DATE,
  role VARCHAR(50),
  salary INT,
  department_id INT,
  address VARCHAR(100),
  contact_number VARCHAR(12),
  email_id VARCHAR(100),
  marital_status ENUM('Married', 'Single', 'Non-married'),
  FOREIGN KEY (department_id) REFERENCES departments(department_id)
);\n""")
    for i in tqdm(range(1, 1001), desc="Generating SQL Scripts for Employees Details..."):
        name = fake.name().replace("'", "")
        age = random.randint(25, 60)
        gender = random.choice(genders)
        dob = fake.date_of_birth(minimum_age=age, maximum_age=age).strftime('%Y-%m-%d')
        doj = fake.date_between(start_date='-10y', end_date='today').strftime('%Y-%m-%d')
        role = random.choice(roles)
        salary = random.randint(70000, 290000)
        dept_id = random.randint(1, len(departments))
        address = fake.address().replace('\n', ', ').replace("'", "")
        contact_number = ''.join(str(random.randint(0, 9)) for _ in range(random.randint(10, 12)))
        email = fake.email().replace("'", "")
        marital = random.choice(marital_status_options)
        f.write(f"INSERT INTO employees (employee_name, age, gender, date_of_birth, date_of_joining, role, salary, department_id, address, contact_number, email_id, marital_status) VALUES ('{name}', {age}, '{gender}', '{dob}', '{doj}', '{role}', {salary}, {dept_id}, '{address}', '{contact_number}', '{email}', '{marital}');\n")

    # Projects
    f.write("""
CREATE TABLE projects (
  project_id INT PRIMARY KEY AUTO_INCREMENT,
  project_name VARCHAR(100),
  start_date DATE,
  end_date DATE,
  status ENUM('Active', 'Completed', 'On Hold', 'Cancelled'),
  budget INT,
  department_id INT,
  FOREIGN KEY (department_id) REFERENCES departments(department_id)
);\n""")
    for i in tqdm(range(1, 25001), desc="Generating SQL Scripts for Projects Details..."):
        pname = fake.catch_phrase().replace("'", "")
        s_date = fake.date_between(start_date='-3y', end_date='-6m').strftime('%Y-%m-%d')
        e_date = fake.date_between_dates(date_start=date.fromisoformat(s_date), date_end=date.today()).strftime('%Y-%m-%d')
        status = random.choice(statuses)
        budget = random.randint(500000, 4000000)
        dept_id = random.randint(1, len(departments))
        f.write(f"INSERT INTO projects (project_name, start_date, end_date, status, budget, department_id) VALUES ('{pname}', '{s_date}', '{e_date}', '{status}', {budget}, {dept_id});\n")

    # Employee_Project
    f.write("""
CREATE TABLE employee_project (
  empID INT,
  project_id INT,
  role_in_project VARCHAR(100),
  assigned_date DATE,
  PRIMARY KEY (empID, project_id),
  FOREIGN KEY (empID) REFERENCES employees(empID),
  FOREIGN KEY (project_id) REFERENCES projects(project_id)
);\n""")
    for emp_id in tqdm(range(1, 1001), desc="Generating SQL Scripts for Projects Assigned to Employees Details..."):
        for proj_id in random.sample(range(1, 25001), random.randint(1, 5)):
            role = random.choice(roles)
            assigned_date = fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d')
            f.write(f"INSERT INTO employee_project (empID, project_id, role_in_project, assigned_date) VALUES ({emp_id}, {proj_id}, '{role}', '{assigned_date}');\n")

    # Attendance
    f.write("""
    CREATE TABLE attendance (
      attendance_id INT PRIMARY KEY AUTO_INCREMENT,
      empID INT,
      date DATE,
      status ENUM('Present', 'Absent', 'Half Day', 'Leave'),
      FOREIGN KEY (empID) REFERENCES employees(empID)
    );\n""")

    start_date = date(2024, 1, 1)
    end_date = date(2024, 12, 31)
    delta = timedelta(days=1)

    # Calculate total days
    total_days = (end_date - start_date).days + 1

    current_date = start_date
    for _ in tqdm(range(total_days), desc="Generating SQL Scripts for Attendance Records Details..."):
        for emp_id in range(1, 1001):
            status = random.choices(['Present', 'Absent', 'Half Day', 'Leave'], weights=[70, 10, 40, 40])[0]
            f.write(f"INSERT INTO attendance (empID, date, status) VALUES ({emp_id}, '{current_date}', '{status}');\n")
        current_date += delta

    # Bonuses
    f.write("""
CREATE TABLE bonuses (
  bonus_id INT PRIMARY KEY AUTO_INCREMENT,
  empID INT,
  hours_overtime INT,
  bonus_amount INT,
  bonus_date DATE,
  FOREIGN KEY (empID) REFERENCES employees(empID)
);\n""")
    for emp_id in tqdm(range(1, 1001), desc="Generating SQL Scripts for Bonus Details for Employees.."):
        for _ in range(random.randint(0, 3)):
            hours = random.randint(1, 10)
            bonus = hours * 1000
            bdate = fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d')
            f.write(f"INSERT INTO bonuses (empID, hours_overtime, bonus_amount, bonus_date) VALUES ({emp_id}, {hours}, {bonus}, '{bdate}');\n")

    # Payroll
    f.write("""
CREATE TABLE payroll (
  payroll_id INT PRIMARY KEY AUTO_INCREMENT,
  empID INT,
  month VARCHAR(20),
  base_salary INT,
  bonus_paid INT,
  deductions INT,
  net_salary INT,
  payment_date DATE,
  FOREIGN KEY (empID) REFERENCES employees(empID)
);\n""")
    for emp_id in tqdm(range(1, 1001), desc="Generating SQL Scripts for Payroll Detail..."):
        base_salary = random.randint(70000, 290000)
        for month in months:
            bonus_paid = random.choice([0, 1000, 2000, 3000])
            deductions = random.randint(0, 2000)
            net_salary = base_salary + bonus_paid - deductions
            payment_date = fake.date_between_dates(date_start=date(2022, 1, 1), date_end=date(2025, 12, 31)).strftime('%Y-%m-%d')
            f.write(f"INSERT INTO payroll (empID, month, base_salary, bonus_paid, deductions, net_salary, payment_date) VALUES ({emp_id}, '{month}', {base_salary}, {bonus_paid}, {deductions}, {net_salary}, '{payment_date}');\n")

    # Leaves
    f.write("""
CREATE TABLE leaves (
  leave_id INT PRIMARY KEY AUTO_INCREMENT,
  empID INT,
  leave_type ENUM('Casual', 'Sick', 'Paid', 'Unpaid'),
  start_date DATE,
  end_date DATE,
  status ENUM('Approved', 'Rejected', 'Pending'),
  FOREIGN KEY (empID) REFERENCES employees(empID)
);\n""")
    for emp_id in tqdm(range(1, 1001), desc="Generating SQL Scripts for Leave Details..."):
        for _ in range(random.randint(0, 4)):
            ltype = random.choice(leave_types)
            s_date = fake.date_between(start_date='-1y', end_date='today')
            e_date = s_date + timedelta(days=random.randint(1, 10))
            status = random.choice(leave_statuses)
            f.write(f"INSERT INTO leaves (empID, leave_type, start_date, end_date, status) VALUES ({emp_id}, '{ltype}', '{s_date}', '{e_date}', '{status}');\n")

    # Training
    f.write("""
CREATE TABLE training (
  training_id INT PRIMARY KEY AUTO_INCREMENT,
  empID INT,
  training_name VARCHAR(100),
  start_date DATE,
  end_date DATE,
  status ENUM('Completed', 'Ongoing', 'Not Started'),
  FOREIGN KEY (empID) REFERENCES employees(empID)
);\n""")
    training_courses = ['Python Basics', 'Project Management', 'Data Analysis', 'Leadership', 'Communication Skills']
    for emp_id in tqdm(range(1, 1001), desc="Generating SQL Scripts for Employee Training Details..."):
        for _ in range(random.randint(0, 2)):
            tname = random.choice(training_courses)
            s_date = fake.date_between(start_date='-2y', end_date='-6m')
            e_date = s_date + timedelta(days=random.randint(5, 30))
            status = random.choice(training_statuses)
            f.write(f"INSERT INTO training (empID, training_name, start_date, end_date, status) VALUES ({emp_id}, '{tname}', '{s_date}', '{e_date}', '{status}');\n")

    # Assets
    f.write("""
CREATE TABLE assets (
  asset_id INT PRIMARY KEY AUTO_INCREMENT,
  empID INT,
  asset_name VARCHAR(100),
  asset_type VARCHAR(50),
  purchase_date DATE,
  status ENUM('Issued', 'Returned', 'Lost'),
  FOREIGN KEY (empID) REFERENCES employees(empID)
);\n""")
    for emp_id in tqdm(range(1, 1001), desc="Generating SQL Scripts for Assigned Assets Details..."):
        for _ in range(random.randint(0, 3)):
            aname = random.choice(asset_types) + ' ' + fake.word().capitalize()
            atype = random.choice(asset_types)
            p_date = fake.date_between(start_date='-3y', end_date='today')
            status = random.choice(asset_statuses)
            f.write(f"INSERT INTO assets (empID, asset_name, asset_type, purchase_date, status) VALUES ({emp_id}, '{aname}', '{atype}', '{p_date}', '{status}');\n")

    # Employee_Benefits
    f.write("""
CREATE TABLE employee_benefits (
  benefit_id INT PRIMARY KEY AUTO_INCREMENT,
  empID INT,
  benefit_name VARCHAR(100),
  benefit_value VARCHAR(100),
  FOREIGN KEY (empID) REFERENCES employees(empID)
);\n""")
    for emp_id in tqdm(range(1, 1001), desc="Generating SQL Scripts for Employee Benefits Details..."):
        for _ in range(random.randint(0, 3)):
            bname = random.choice(benefits)
            bvalue = f"{random.randint(1, 100)} units" if "Stock" in bname else f"${random.randint(100, 2000)}"
            f.write(f"INSERT INTO employee_benefits (empID, benefit_name, benefit_value) VALUES ({emp_id}, '{bname}', '{bvalue}');\n")

print("Full company database SQL script generated as 'company_database_full.sql'.")

