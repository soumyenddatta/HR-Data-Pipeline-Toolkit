import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
from tqdm import tqdm

# Terminal colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
DEEP_BLUE = '\033[38;5;18m'
RESET = '\033[0m'

# MySQL config
MYSQL_USER = 'root'
MYSQL_PASSWORD = '17111998'
MYSQL_HOST = 'localhost'
MYSQL_DB = 'company_db'

# Connect using mysql.connector
conn = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB,
    use_pure=True
)
cursor = conn.cursor()

# Use SQLAlchemy for pandas
engine_str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
engine = create_engine(engine_str)

# Get all tables
cursor.execute("SHOW TABLES")
tables = [row[0] for row in cursor.fetchall()]
total_tables = len(tables)

# ✅ Print table count and names
print(f"\n{YELLOW}📊 Total tables found in database: {total_tables}{RESET}")
print(f"{BLUE}📋 Table names:{RESET}")
for name in tables:
    print(f" - {name}")

# Export each table to CSV with a progress bar
print(f"\n{YELLOW}📁 Starting export to CSV files...{RESET}\n")
for i, table in enumerate(tqdm(tables, desc="Exporting Tables", unit="table", colour="blue")):
    tqdm.write(f"{GREEN}📤 Exporting table {i+1}/{total_tables}: {table}{RESET}")
    df = pd.read_sql(f"SELECT * FROM `{table}`", engine)
    df.to_csv(f"{table}.csv", index=False)

cursor.close()
conn.close()

print(f"\n{GREEN}✅ Export completed. All tables written to CSV.{RESET}")
