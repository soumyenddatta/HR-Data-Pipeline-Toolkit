# Import required libraries
from tqdm import tqdm  # For displaying progress bars
import random  # For generating random values
from faker import Faker  # For generating fake data
from datetime import date, timedelta, datetime  # For date operations

# Initialize Faker
fake = Faker()

# Predefined lists of values to use for fake data generation
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
months = [datetime(2023, m, 1).strftime('%B %Y') for m in range(1, 13)]  # Month names for payroll

# Open a file to write the SQL script
with open('company_database_full_test.sql', 'w') as f:
    # Write initial database creation and use statements
    f.write("CREATE DATABASE IF NOT EXISTS company_db_test;\nUSE company_db_test;\n\n")

    # --------------------- DEPARTMENTS ---------------------
    f.write("CREATE TABLE departments (department_id INT PRIMARY KEY AUTO_INCREMENT, department_name VARCHAR(50) UNIQUE);\n")
    for dept in departments:
        f.write(f"INSERT INTO departments (department_name) VALUES ('{dept}');\n")

    # --------------------- EMPLOYEES ---------------------
    f.write("""...employees table definition...\n""")
    for i in tqdm(range(1, 1001), desc="Generating SQL Scripts for Employees Details..."):
        # Generate random employee details
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
        # Write insert statement for employee
        f.write(f"INSERT INTO employees ... VALUES (...);\n")

    # --------------------- PROJECTS ---------------------
    f.write("""...projects table definition...\n""")
    for i in tqdm(range(1, 25001), desc="Generating SQL Scripts for Projects Details..."):
        # Generate project details
        pname = fake.catch_phrase().replace("'", "")
        s_date = fake.date_between(start_date='-3y', end_date='-6m').strftime('%Y-%m-%d')
        e_date = fake.date_between_dates(date_start=date.fromisoformat(s_date), date_end=date.today()).strftime('%Y-%m-%d')
        status = random.choice(statuses)
        budget = random.randint(500000, 4000000)
        dept_id = random.randint(1, len(departments))
        # Write insert statement for project
        f.write(f"INSERT INTO projects ... VALUES (...);\n")

    # --------------------- EMPLOYEE_PROJECT ---------------------
    f.write("""...employee_project table definition...\n""")
    for emp_id in tqdm(range(1, 1001), desc="Generating SQL Scripts for Projects Assigned to Employees Details..."):
        for proj_id in random.sample(range(1, 25001), random.randint(1, 5)):
            role = random.choice(roles)
            assigned_date = fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d')
            f.write(f"INSERT INTO employee_project ... VALUES (...);\n")

    # --------------------- ATTENDANCE ---------------------
    f.write("""...attendance table definition...\n""")
    start_date = date(2020, 1, 1)
    end_date = date(2025, 12, 31)
    delta = timedelta(days=1)
    total_days = (end_date - start_date).days + 1
    current_date = start_date
    for _ in tqdm(range(total_days), desc="Generating SQL Scripts for Attendance Records Details..."):
        for emp_id in range(1, 1001):
            # Weighted choice for attendance status
            status = random.choices(['Present', 'Absent', 'Half Day', 'Leave'], weights=[70, 10, 40, 40])[0]
            f.write(f"INSERT INTO attendance ... VALUES (...);\n")
        current_date += delta

    # --------------------- BONUSES ---------------------
    f.write("""...bonuses table definition...\n""")
    for emp_id in tqdm(range(1, 1001), desc="Generating SQL Scripts for Bonus Details for Employees.."):
        for _ in range(random.randint(0, 3)):
            hours = random.randint(1, 10)
            bonus = hours * 1000
            bdate = fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d')
            f.write(f"INSERT INTO bonuses ... VALUES (...);\n")

    # --------------------- PAYROLL ---------------------
    f.write("""...payroll table definition...\n""")
    for emp_id in tqdm(range(1, 1001), desc="Generating SQL Scripts for Payroll Detail..."):
        base_salary = random.randint(70000, 290000)
        for month in months:
            bonus_paid = random.choice([0, 1000, 2000, 3000])
            deductions = random.randint(0, 2000)
            net_salary = base_salary + bonus_paid - deductions
            payment_date = fake.date_between_dates(date_start=date(2022, 1, 1), date_end=date(2025, 12, 31)).strftime('%Y-%m-%d')
            f.write(f"INSERT INTO payroll ... VALUES (...);\n")

    # --------------------- LEAVES ---------------------
    f.write("""...leaves table definition...\n""")
    for emp_id in tqdm(range(1, 1001), desc="Generating SQL Scripts for Leave Details..."):
        for _ in range(random.randint(0, 4)):
            ltype = random.choice(leave_types)
            s_date = fake.date_between(start_date='-1y', end_date='today')
            e_date = s_date + timedelta(days=random.randint(1, 10))
            status = random.choice(leave_statuses)
            f.write(f"INSERT INTO leaves ... VALUES (...);\n")

    # --------------------- TRAINING ---------------------
    f.write("""...training table definition...\n""")
    training_courses = ['Python Basics', 'Project Management', 'Data Analysis', 'Leadership', 'Communication Skills']
    for emp_id in tqdm(range(1, 1001), desc="Generating SQL Scripts for Employee Training Details..."):
        for _ in range(random.randint(0, 2)):
            tname = random.choice(training_courses)
            s_date = fake.date_between(start_date='-2y', end_date='-6m')
            e_date = s_date + timedelta(days=random.randint(5, 30))
            status = random.choice(training_statuses)
            f.write(f"INSERT INTO training ... VALUES (...);\n")

    # --------------------- ASSETS ---------------------
    f.write("""...assets table definition...\n""")
    for emp_id in tqdm(range(1, 1001), desc="Generating SQL Scripts for Assigned Assets Details..."):
        for _ in range(random.randint(0, 3)):
            aname = random.choice(asset_types) + ' ' + fake.word().capitalize()
            atype = random.choice(asset_types)
            p_date = fake.date_between(start_date='-3y', end_date='today')
            status = random.choice(asset_statuses)
            f.write(f"INSERT INTO assets ... VALUES (...);\n")

    # --------------------- EMPLOYEE BENEFITS ---------------------
    f.write("""...employee_benefits table definition...\n""")
    for emp_id in tqdm(range(1, 1001), desc="Generating SQL Scripts for Employee Benefits Details..."):
        for _ in range(random.randint(0, 3)):
            bname = random.choice(benefits)
            bvalue = f"{random.randint(1, 100)} units" if "Stock" in bname else f"${random.randint(100, 2000)}"
            f.write(f"INSERT INTO employee_benefits ... VALUES (...);\n")

# Final output message
print("Full company database SQL script generated as 'company_database_full.sql'.")
