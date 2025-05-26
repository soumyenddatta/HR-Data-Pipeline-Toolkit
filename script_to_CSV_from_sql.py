import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
from tqdm import tqdm
import os  # ← ADDED: To manage the dump directory
import time  # ← ADDED: For timestamps in logging

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

# Create dump directory if not exists
DUMP_DIR = os.path.join('.', 'dump')  # ← ADDED
os.makedirs(DUMP_DIR, exist_ok=True)

LOG_FILE = os.path.join(DUMP_DIR, 'process.log')  # ← ADDED: Log file path
with open(LOG_FILE, 'a', encoding='utf-8') as log:
    log.write(f"___________________________________________________________________________________________"
              f"\n [{time.strftime('%Y-%m-%d %H:%M:%S')}] || CSV Conversion Log || Database = '{MYSQL_DB}' \n")

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

    # Save CSV to dump folder
    output_path = os.path.join(DUMP_DIR, f"{table}.csv")
    df.to_csv(output_path, index=False)  # ← MODIFIED

    # Log to process.log
    with open(LOG_FILE, 'a', encoding='utf-8') as log:
        log.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Exported '{table}' "
                  f" with {len(df)} rows to '{output_path}'\n")  # ← ADDED

cursor.close()
conn.close()

with open(LOG_FILE, 'a', encoding='utf-8') as log:
    log.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Exported to CSV form Database '{MYSQL_DB}' \n\n")

print(f"\n{GREEN}✅ Export completed. All tables written to CSV.{RESET}")
