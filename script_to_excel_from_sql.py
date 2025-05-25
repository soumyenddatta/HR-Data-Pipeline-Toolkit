import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
from tqdm import tqdm, trange
import math
from openpyxl.utils import get_column_letter
import logging
from openpyxl.styles import Font
from datetime import datetime
import os

# Terminal colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
DEEP_BLUE = '\033[38;5;18m'
RESET = '\033[0m'

# MySQL connection config
MYSQL_USER = 'root'
MYSQL_PASSWORD = '17111998'
MYSQL_HOST = 'localhost'
MYSQL_DB = 'company_db'

# Excel limits
MAX_EXCEL_ROWS = 1048576

# Connect to MySQL
conn = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB,
    use_pure=True
)
cursor = conn.cursor()

# Use SQLAlchemy for pandas read_sql
engine_str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
engine = create_engine(engine_str)

# Fetch all tables
cursor.execute("SHOW TABLES")
tables = [row[0] for row in cursor.fetchall()]

print(f"\n{YELLOW}Total tables to export: {len(tables)}{RESET}\n")

# Setup logging
log_file = "process.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
if os.path.exists(log_file):
    with open(log_file, 'a') as f:
        f.write("\n" + "="*40 + f"\nRun started at {datetime.now()}\n")

# Progress bar for exporting tables
excel_writer_progress = tqdm(total=1, desc=GREEN + "📁 Opening ExcelWriter..." + RESET, colour='green')
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    excel_writer_progress.update(1)
    excel_writer_progress.set_description_str(GREEN + "✅ ExcelWriter ready" + RESET)
    excel_writer_progress.close()

    # Tables loop
    for table in tqdm(tables, desc="📄 Exporting tables", colour='green', leave=True):
        print(f"{BLUE}📤 Exporting table: {table}{RESET}")
        logging.info(f"Exporting table: {table}")

        df = pd.read_sql(f"SELECT * FROM `{table}`", engine)
        total_rows = len(df)
        max_data_rows = MAX_EXCEL_ROWS - 1
        chunks = math.ceil(total_rows / max_data_rows)

        # Chunk loop
        for i in trange(chunks, desc=f"🧮 Chunking {table}", colour='yellow', leave=True):
            start = i * max_data_rows
            end = start + max_data_rows
            chunk_df = df.iloc[start:end]

            sheet_name = f"{table}_part{i+1}" if chunks > 1 else table
            chunk_df.to_excel(writer, sheet_name=sheet_name, index=False)

            worksheet = writer.sheets[sheet_name]
            logging.info(f"Wrote sheet: {sheet_name} with {len(chunk_df)} rows")

            # Column autofit
            autofit_iter = tqdm(
                enumerate(chunk_df.columns, 1),
                desc=f"✏️ Autofitting {sheet_name}",
                colour='blue',
                leave=False
            )
            for col_idx, col in autofit_iter:
                max_length = max(chunk_df[col].astype(str).map(len).max(), len(col))
                worksheet.column_dimensions[get_column_letter(col_idx)].width = max_length + 2
                logging.debug(f"Column {col} width set")

print(f"{GREEN}🎉 Export complete!{RESET}")

logging.info("Export process complete.")


print(f"\n{GREEN}Export completed successfully!{RESET}")
