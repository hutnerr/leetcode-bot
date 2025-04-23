import csv
import os

from utils import logger

# =======================================
# =======================================
# CSV OPERATIONS
# =======================================
# =======================================

def write_line_to_csv(file_path:str, line:str, encoding:str='utf-8') -> bool:
    try:
        ensure_directory_exists(file_path)
        with open(file_path, 'a', newline='', encoding=encoding) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(line.split(","))
        return True
    except Exception as e:
        logger.error(f"Error writing line to CSV: {e}")
        return False



def write_to_csv(file_path:str, lines:list | tuple, mode:str='a', encoding:str='utf-8') -> bool:
    # write multiple lines to a CSV file.
    # default behavior is to append to the file, not overwrite it.
    # change mode to 'w' to overwrite
    try:
        ensure_directory_exists(file_path)

        # write one line at a time
        if mode == 'a':
            success = True
            for line in lines:
                result = write_line_to_csv(file_path, line, encoding)
                if not result:
                    success = False
            return success

        # overwrite and write all at once
        else:
            with open(file_path, mode, newline='', encoding=encoding) as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(lines)
            return True
    except Exception as e:
        logger.error(f"Error writing to CSV: {e}")
        return False


def read_from_csv(file_path:str, encoding:str='utf-8') -> list[str]:
    # read all lines from csv
    lines = []
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return lines

        with open(file_path, 'r', newline='', encoding=encoding) as csvfile:
            for row in csvfile:
                lines.append(row.strip())
        return lines
    except Exception as e:
        logger.error(f"Error reading from CSV: {e}")
        return lines

# =======================================
# =======================================
# GENERAL FILE OPERATIONS
# =======================================
# =======================================


def write_text_to_file(file_path:str, text:str, mode:str='a', encoding:str='utf-8') -> bool:
    try:
        ensure_directory_exists(file_path)
        with open(file_path, mode, encoding=encoding) as file:
            file.write(text)
        return True
    except Exception as e:
        logger.error(f"Error writing to file: {e}")
        return False

def write_line_to_file(file_path:str, line:str, add_newline:bool=True, encoding:str='utf-8') -> bool:
    # write a single line to a file, appending to the end.
    text = line
    if add_newline:
        text += '\n'
    return write_text_to_file(file_path, text, 'a', encoding)


def write_lines_to_file(file_path:str, lines:list | tuple, mode:str='a', encoding:str='utf-8') -> bool:
    # write multiple lines to a file.
    try:
        ensure_directory_exists(file_path)

        with open(file_path, mode, encoding=encoding) as file:
            for line in lines:
                file.write(line + '\n')
        return True
    except Exception as e:
        logger.error(f"Error writing lines to file: {e}")
        return False


def read_lines_from_file(file_path:str, encoding:str='utf-8') -> list[str] | list:
    # reads all lines
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return []

        with open(file_path, 'r', encoding=encoding) as file:
            return file.readlines()
    except Exception as e:
        logger.error(f"Error reading lines from file: {e}")
        return []

# =======================================
# =======================================
# CHECKS
# =======================================
# =======================================

def file_exists(file_path:str) -> bool:
    return os.path.isfile(file_path)


def ensure_directory_exists(file_path:str) -> bool:
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        return True
    except Exception as e:
        logger.error(f"Error creating directory: {e}")
        return False