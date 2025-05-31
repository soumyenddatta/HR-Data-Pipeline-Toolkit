import os
import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# File icons by extension
FILE_ICONS = {
    '.py': '🐍',
    '.csv': '📊',
    '.md': '📝',
    '.txt': '📝',
    '.jpg': '🖼️',
    '.jpeg': '🖼️',
    '.png': '🖼️',
    '.gif': '🖼️',
    '.pdf': '📄',
    '.zip': '📦',
    '.tar': '📦',
    '.gz': '📦',
}

def format_size(bytes_size):
    """Format bytes into KB, MB, or GB."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} PB"

def format_date(timestamp):
    """Format timestamp into human-readable date."""
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def get_file_icon(filename):
    """Return icon based on file extension."""
    ext = os.path.splitext(filename)[1].lower()
    return FILE_ICONS.get(ext, '📄')

def scan_directory_recursive(directory='.'):
    """Recursively list all files, skipping dot-directories, in a colorful tree view with icons."""
    print(f"\n{Fore.YELLOW}📂 Scanning directory: {os.path.abspath(directory)}")
    print("=" * 90)

    for root, dirs, files in os.walk(directory):
        # Skip dot-directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        level = root.replace(directory, '').count(os.sep)
        indent = '│   ' * level + '├── ' if level > 0 else ''
        print(f"{Fore.BLUE}{indent}📁 {os.path.basename(root)}/")
        sub_indent = '│   ' * (level + 1)
        for f in files:
            file_path = os.path.join(root, f)
            try:
                size = format_size(os.path.getsize(file_path))
                modified = format_date(os.path.getmtime(file_path))
                icon = get_file_icon(f)
                print(f"{sub_indent}{Fore.GREEN}{icon} {f} "
                      f"{Fore.YELLOW}- {size} "
                      f"{Fore.MAGENTA}- {modified}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{sub_indent}{Fore.RED}⚠️ {f} (Error: {e})")

    print(f"\n{Fore.GREEN}🌲 Scan complete!\n")

if __name__ == '__main__':
    directory_path = input("Enter directory path (press Enter for current directory): ").strip()
    if not directory_path:
        directory_path = '.'
    scan_directory_recursive(directory_path)
