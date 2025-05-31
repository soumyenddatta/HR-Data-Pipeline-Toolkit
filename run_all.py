# run_all.py

import os
import subprocess
import datetime
from tqdm import tqdm

# Define dump directory and log file
DUMP_DIR = os.path.join('.', 'dump')
LOG_FILE = os.path.join(DUMP_DIR, 'process.log')

# Ensure dump directory exists
os.makedirs(DUMP_DIR, exist_ok=True)

def log_console(msg):
    """Log to terminal with timestamp"""
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} {msg}")

def log_file(msg):
    """Append message to process.log with timestamp"""
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, 'a', encoding='utf-8') as log:
        log.write(f"{timestamp} {msg}\n")

def run_script(script_name):
    log_console(f"[...] Running {script_name}...")
    log_file(f"Started: {script_name}")
    result = subprocess.run(["python", script_name], capture_output=True, text=True)

    if result.returncode == 0:
        log_console(f"[✓] {script_name} completed successfully.\n")
        log_file(f"Success: {script_name}")
        return True
    else:
        log_console(f"[X] {script_name} failed. Stopping pipeline.\n")
        log_file(f"Failure: {script_name}\n{result.stderr.strip()}\n")
        return False

if __name__ == "__main__":
    log_console("🔁 Starting full HR Data Pipeline...")
    log_file("\n" + "="*40)
    log_file(f"Pipeline started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    steps = [
        "main.py",
        "script_for_sql_loading.py",
        "script_to_CSV_from_sql.py",
        "script_from_csv_to_excel.py",
        "script_to_excel_from_sql.py"
    ]

    success = True
    with tqdm(total=len(steps), bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} ✅", ncols=80) as pbar:
        for step in steps:
            if run_script(step):
                pbar.update(1)
            else:
                success = False
                break

    if success:
        log_console("🎉 All steps completed. Check the 'dump/' folder for output files.")
        log_file("Pipeline finished successfully.\n")
    else:
        log_console("⚠️ Pipeline terminated early due to errors.")
        log_file("Pipeline terminated with errors.\n")
