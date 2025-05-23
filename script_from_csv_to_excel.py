import os
import time
import pandas as pd
from tqdm import tqdm, trange
from openpyxl.utils import get_column_letter
from colorama import Fore, Style, init

init(autoreset=True)

INPUT_DIR = '.'  # or set your CSV folder path
OUTPUT_FILE = 'output.xlsx'
MAX_EXCEL_ROWS = 1048576

# Color variables
GREEN = Fore.GREEN
RED = Fore.RED
CYAN = Fore.CYAN
YELLOW = Fore.YELLOW
RESET = Style.RESET_ALL


def write_df_chunks_to_excel(df, base_name, writer):
    total_rows = len(df)
    max_data_rows = MAX_EXCEL_ROWS - 1  # Reserve row for header
    chunks = (total_rows + max_data_rows - 1) // max_data_rows

    for i in trange(chunks, desc=f"📄 Splitting '{base_name}'", leave=False, colour='green'):
        start = i * max_data_rows
        end = min(start + max_data_rows, total_rows)
        chunk = df.iloc[start:end]
        sheet_name = f"{base_name}_part{i + 1}" if chunks > 1 else base_name
        chunk.to_excel(writer, sheet_name=sheet_name, index=False)

        # Autofit columns (optional, but slow for very wide sheets)
        worksheet = writer.sheets[sheet_name]
        for col_idx, col in enumerate(chunk.columns, 1):
            max_length = max(chunk[col].astype(str).map(len).max(), len(str(col)))
            worksheet.column_dimensions[get_column_letter(col_idx)].width = min(max_length + 2, 50)


def main():
    csv_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.csv')]
    if not csv_files:
        print("❌ No CSV files found.")
        return

    print(f"{Fore.BLUE + Style.BRIGHT}📂 Found {Fore.CYAN + str(len(csv_files))} CSV file(s) in the directory:\n")

    for f in csv_files:
        print(f"  {Fore.GREEN}🗂️  {f} {Fore.MAGENTA}({len(f)} characters)")

    print(f"\n{Fore.YELLOW}🔄 Starting conversion to {Fore.LIGHTBLUE_EX}'{OUTPUT_FILE}'{Style.RESET_ALL}...\n")

    sheets_created = 0

    with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
        for csv_file in tqdm(csv_files, desc=f"{CYAN}📝 Writing CSVs to Excel{RESET}", colour='cyan', ncols=100):
            start_time = time.time()
            file_path = os.path.join(INPUT_DIR, csv_file)

            try:
                df = pd.read_csv(file_path, on_bad_lines='skip')
                sheet_base = os.path.splitext(csv_file)[0][:31]

                write_df_chunks_to_excel(df, sheet_base, writer)

                elapsed = time.time() - start_time
                print(f"{GREEN}✅ Finished '{csv_file}' → Sheet '{sheet_base}' in {elapsed:.2f} sec{RESET}")
                sheets_created += 1

            except Exception as e:
                print(f"{RED}❌ Error processing {csv_file}: {e}{RESET}")

        if sheets_created == 0:
            raise RuntimeError(f"{RED}No valid CSVs processed. Aborting Excel file creation.{RESET}")

    print(f"\n{GREEN}🎉 All {sheets_created} CSVs successfully merged into '{OUTPUT_FILE}'!{RESET}\n")


if __name__ == "__main__":
    main()
