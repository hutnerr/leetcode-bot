import csv
from core.utils import file_helper as fh

# reads a CSV file and returns its content as a list of lists
def readFromCSV(filePath: str) -> list[list[str]] | None:
    if not fh.fileExists(filePath):
        return None
    
    with open(filePath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return [[cell.strip() for cell in row] for row in reader]

# appends a single line to a CSV file
def writeLineToCSV(filePath: str, line: list[str], overwrite: bool = False) -> bool:
    try:
        mode = 'w' if overwrite else 'a'
        with open(filePath, mode, newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(line)
        return True
    except Exception as e:
        print(f"Error writing to CSV {filePath}: {e}")
        return False

# appends multiple lines to a CSV file
def writeLinesToCSV(filePath: str, lines: list[list[str]], overwrite: bool = False) -> bool:
    try:
        mode = 'w' if overwrite else 'a'
        with open(filePath, mode, newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(lines)
        return True
    except Exception as e:
        print(f"Error writing multiple lines to CSV {filePath}: {e}")
        return False
