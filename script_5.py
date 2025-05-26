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

batch_size = 1000


def write_multi_insert(f, table, columns, values_list):
    # Writes multi-row INSERT statements with given values list
    if not values_list:
        return
    f.write(f"INSERT INTO {table} ({', '.join(columns)}) VALUES\n")
    f.write(",\n".join(values_list) + ";\n")


with open('company_database_full.sql', 'w') as f:
    f.write("CREATE DATABASE IF NOT EXISTS company_db;\nUSE company_db;\n\n")
    f.write("SET FOREIGN_KEY_CHECKS=0;\nSET UNIQUE_CHECKS=0;\n\n")

    # Departments (small, no batching needed)
    f.write(
        "CREATE TABLE departments (department_id INT PRIMARY KEY AUTO_INCREMENT, department_name VARCHAR(50) UNIQUE);\n")
    for dept in departments:
        f.write(f"INSERT INTO departments (department_name) VALUES ('{dept}');\n")
    f.write("\n")

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
    f.write("START TRANSACTION;\n")
    batch = []
    for i in tqdm(range(1, 5001), desc="Employees"):
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
        val = f"('{name}', {age}, '{gender}', '{dob}', '{doj}', '{role}', {salary}, {dept_id}, '{address}', '{contact_number}', '{email}', '{marital}')"
        batch.append(val)
        if len(batch) >= batch_size:
            write_multi_insert(f, "employees", [
                "employee_name", "age", "gender", "date_of_birth", "date_of_joining", "role", "salary",
                "department_id", "address", "contact_number", "email_id", "marital_status"
            ], batch)
            batch = []
    if batch:
        write_multi_insert(f, "employees", [
            "employee_name", "age", "gender", "date_of_birth", "date_of_joining", "role", "salary",
            "department_id", "address", "contact_number", "email_id", "marital_status"
        ], batch)
    f.write("COMMIT;\n\n")

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
    f.write("START TRANSACTION;\n")
    batch = []
    for i in tqdm(range(1, 12001), desc="Projects"):
        pname = fake.catch_phrase().replace("'", "")
        s_date = fake.date_between(start_date='-3y', end_date='-6m').strftime('%Y-%m-%d')
        e_date = fake.date_between_dates(date_start=date.fromisoformat(s_date), date_end=date.today()).strftime(
            '%Y-%m-%d')
        status = random.choice(statuses)
        budget = random.randint(500000, 4000000)
        dept_id = random.randint(1, len(departments))
        val = f"('{pname}', '{s_date}', '{e_date}', '{status}', {budget}, {dept_id})"
        batch.append(val)
        if len(batch) >= batch_size:
            write_multi_insert(f, "projects",
                               ["project_name", "start_date", "end_date", "status", "budget", "department_id"], batch)
            batch = []
    if batch:
        write_multi_insert(f, "projects",
                           ["project_name", "start_date", "end_date", "status", "budget", "department_id"], batch)
    f.write("COMMIT;\n\n")

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
    f.write("START TRANSACTION;\n")
    batch = []
    for emp_id in tqdm(range(1, 5001), desc="Employee_Project"):
        assigned_projects = random.sample(range(1, 12001), random.randint(1, 5))
        for proj_id in assigned_projects:
            role = random.choice(roles)
            assigned_date = fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d')
            val = f"({emp_id}, {proj_id}, '{role}', '{assigned_date}')"
            batch.append(val)
            if len(batch) >= batch_size:
                write_multi_insert(f, "employee_project", ["empID", "project_id", "role_in_project", "assigned_date"],
                                   batch)
                batch = []
    if batch:
        write_multi_insert(f, "employee_project", ["empID", "project_id", "role_in_project", "assigned_date"], batch)
    f.write("COMMIT;\n\n")

    # Attendance
    f.write("""
CREATE TABLE attendance (
  attendance_id INT PRIMARY KEY AUTO_INCREMENT,
  empID INT,
  date DATE,
  status ENUM('Present', 'Absent', 'Half Day', 'Leave'),
  FOREIGN KEY (empID) REFERENCES employees(empID)
);\n""")

    start_date = date(2020, 1, 1)
    end_date = date(2025, 12, 31)
    delta = timedelta(days=1)
    total_days = (end_date - start_date).days + 1

    f.write("START TRANSACTION;\n")
    batch = []
    current_date = start_date
    for _ in tqdm(range(total_days), desc="Attendance"):
        for emp_id in range(1, 5001):
            status = random.choices(['Present', 'Absent', 'Half Day', 'Leave'], weights=[70, 10, 40, 40])[0]
            val = f"({emp_id}, '{current_date}', '{status}')"
            batch.append(val)
            if len(batch) >= batch_size:
                write_multi_insert(f, "attendance", ["empID", "date", "status"], batch)
                batch = []
        current_date += delta
    if batch:
        write_multi_insert(f, "attendance", ["empID", "date", "status"], batch)
    f.write("COMMIT;\n\n")

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
    f.write("START TRANSACTION;\n")
    batch = []
    for emp_id in tqdm(range(1, 5001), desc="Bonuses"):
        for _ in range(random.randint(0, 3)):
            hours = random.randint(1, 10)
            bonus = hours * 1000
            bdate = fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d')
            val = f"({emp_id}, {hours}, {bonus}, '{bdate}')"
            batch.append(val)
            if len(batch) >= batch_size:
                write_multi_insert(f, "bonuses", ["empID", "hours_overtime", "bonus_amount", "bonus_date"], batch)
                batch = []
    if batch:
        write_multi_insert(f, "bonuses", ["empID", "hours_overtime", "bonus_amount", "bonus_date"], batch)
    f.write("COMMIT;\n\n")

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
    f.write("START TRANSACTION;\n")
    batch = []
    for emp_id in tqdm(range(1, 5001), desc="Payroll"):
        base_salary = random.randint(70000, 290000)
        for month in months:
            bonus_paid = random.randint(0, 5000)
            deductions = random.randint(0, 3000)
            net_salary = base_salary + bonus_paid - deductions
            pay_date = fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d')
            val = f"({emp_id}, '{month}', {base_salary}, {bonus_paid}, {deductions}, {net_salary}, '{pay_date}')"
            batch.append(val)
            if len(batch) >= batch_size:
                write_multi_insert(f, "payroll",
                                   ["empID", "month", "base_salary", "bonus_paid", "deductions", "net_salary",
                                    "payment_date"], batch)
                batch = []
    if batch:
        write_multi_insert(f, "payroll",
                           ["empID", "month", "base_salary", "bonus_paid", "deductions", "net_salary", "payment_date"],
                           batch)
    f.write("COMMIT;\n\n")

    # Leaves
    f.write("""
CREATE TABLE leaves (
  leave_id INT PRIMARY KEY AUTO_INCREMENT,
  empID INT,
  start_date DATE,
  end_date DATE,
  leave_type ENUM('Casual', 'Sick', 'Paid', 'Unpaid'),
  status ENUM('Approved', 'Rejected', 'Pending'),
  FOREIGN KEY (empID) REFERENCES employees(empID)
);\n""")
    f.write("START TRANSACTION;\n")
    batch = []
    for emp_id in tqdm(range(1, 5001), desc="Leaves"):
        for _ in range(random.randint(0, 5)):
            start_leave = fake.date_between(start_date='-2y', end_date='today')
            end_leave = start_leave + timedelta(days=random.randint(1, 15))
            leave_type = random.choice(leave_types)
            status = random.choice(leave_statuses)
            val = f"({emp_id}, '{start_leave}', '{end_leave}', '{leave_type}', '{status}')"
            batch.append(val)
            if len(batch) >= batch_size:
                write_multi_insert(f, "leaves", ["empID", "start_date", "end_date", "leave_type", "status"], batch)
                batch = []
    if batch:
        write_multi_insert(f, "leaves", ["empID", "start_date", "end_date", "leave_type", "status"], batch)
    f.write("COMMIT;\n\n")

    # Add your other tables similarly...

    f.write("SET FOREIGN_KEY_CHECKS=1;\nSET UNIQUE_CHECKS=1;\n")

print("SQL dump generation complete.")
