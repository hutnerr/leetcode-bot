import csv
from utils import file_helper as fh

# this module is util functions for working w/ CSV files
# readFromCSV: reads a CSV file and returns its content as a list of lists
# writeLineToCSV: appends a single line to a CSV file
# writeLinesToCSV: appends multiple lines to a CSV file

def readFromCSV(file_path: str) -> list[list[str]] | None:
    if not fh.fileExists(file_path):
        return None
    
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return [row for row in reader]


def writeLineToCSV(file_path: str, line: list[str], overwrite: bool = False) -> bool:
    try:
        mode = 'w' if overwrite else 'a'
        with open(file_path, mode, newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(line)
        return True
    except Exception as e:
        print(f"Error writing to CSV {file_path}: {e}")
        return False


def writeLinesToCSV(file_path: str, lines: list[list[str]], overwrite: bool = False) -> bool:
    try:
        mode = 'w' if overwrite else 'a'
        with open(file_path, mode, newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(lines)
        return True
    except Exception as e:
        print(f"Error writing multiple lines to CSV {file_path}: {e}")
        return False
