import mysql.connector
from tqdm import tqdm
import os
import re
import io

# ANSI Terminal Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
DEEP_BLUE = '\033[38;5;18m'
RESET = '\033[0m'

# MySQL config
config_no_db = {
    'user': 'root',
    'password': '17111998',
    'host': 'localhost',
    'use_pure': True,
    'autocommit': False
}

sql_file_path = 'company_database_full.sql'


def extract_database_name(sql_script):
    match = re.search(r'CREATE DATABASE IF NOT EXISTS\s+`?(\w+)`?|USE\s+`?(\w+)`?', sql_script, re.IGNORECASE)
    return match.group(1) or match.group(2) if match else None


def run_sql_script_with_progress(cursor, filename, buffer_size=16 * 1024 * 1024):
    file_size = os.path.getsize(filename)
    buffer = io.StringIO()

    with open(filename, 'r', encoding='utf-8') as file:
        with tqdm(total=file_size, unit='B', unit_scale=True, desc="📥 Reading SQL file", colour='cyan') as read_bar:
            while True:
                chunk = file.read(buffer_size)
                if not chunk:
                    break
                buffer.write(chunk)
                read_bar.update(len(chunk))

    sql_script = buffer.getvalue()
    buffer.close()

    # Split by ; outside strings (basic safe split)
    statements = re.split(r';\s*\n', sql_script)
    total_statements = len(statements)

    with tqdm(total=total_statements, desc="⚙️ Executing SQL", bar_format=(
        GREEN + "({percentage:6.2f}%)" + RESET + DEEP_BLUE + " {bar} " + RESET +
        GREEN + "| {n_fmt}/{total_fmt} |" + YELLOW + " ({rate_fmt})" + RESET),
              unit='stmts', colour='green') as exec_bar:
        for stmt in statements:
            stmt = stmt.strip()
            if not stmt:
                exec_bar.update(1)
                continue
            try:
                cursor.execute(stmt)
            except mysql.connector.Error as err:
                preview = stmt[:300].replace('\n', ' ')
                print(f"\n{RED}❌ Error executing statement: {preview}...\n{err}{RESET}")
            exec_bar.update(1)


def main():
    conn = None
    cursor = None
    try:
        # Pre-read to get DB name
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_preview = file.read(512 * 1024)
        database_name = extract_database_name(sql_preview)
        if not database_name:
            print(f"{RED}❌ Could not determine DB name from SQL.{RESET}")
            return

        # Connect to MySQL server (no DB yet)
        conn = mysql.connector.connect(**config_no_db)
        cursor = conn.cursor()

        # Drop and create DB
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        cursor.execute("SET UNIQUE_CHECKS=0;")
        cursor.execute(f"DROP DATABASE IF EXISTS `{database_name}`;")
        print(f"{GREEN}✅ Dropped database '{YELLOW}{database_name}{GREEN}' (if it existed).{RESET}")

        # Execute script
        run_sql_script_with_progress(cursor, sql_file_path)
        conn.commit()

        print(f"{GREEN}✅ Recreated and populated DB '{database_name}' successfully.{RESET}")

    except mysql.connector.Error as err:
        print(f"{RED}❌ MySQL Error: {err}{RESET}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
