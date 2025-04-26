import csv
import json
import os
from typing import List, Dict, Union, Any, Tuple

from utils import logger

# =======================================
# UTILITY FUNCTIONS
# =======================================

def ensure_directory_exists(file_path: str) -> bool:
    """Create directory for file_path if it doesn't exist."""
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        return True
    except Exception as e:
        logger.error(f"Error creating directory: {e}")
        return False


def file_exists(file_path: str) -> bool:
    """Check if a file exists."""
    return os.path.isfile(file_path)


# =======================================
# TEXT FILE OPERATIONS
# =======================================

def write_text_to_file(file_path: str, text: str, mode: str = 'a', encoding: str = 'utf-8') -> bool:
    """Write text to a file."""
    try:
        ensure_directory_exists(file_path)
        with open(file_path, mode, encoding=encoding) as file:
            file.write(text)
        return True
    except Exception as e:
        logger.error(f"Error writing to file: {e}")
        return False


def write_line_to_file(file_path: str, line: str, add_newline: bool = True, encoding: str = 'utf-8') -> bool:
    """Write a single line to a file, appending to the end."""
    text = line + ('\n' if add_newline else '')
    return write_text_to_file(file_path, text, 'a', encoding)


def write_lines_to_file(file_path: str, lines: Union[List[str], Tuple[str, ...]], 
                        mode: str = 'a', encoding: str = 'utf-8') -> bool:
    """Write multiple lines to a file."""
    try:
        ensure_directory_exists(file_path)
        with open(file_path, mode, encoding=encoding) as file:
            for line in lines:
                file.write(line + '\n')
        return True
    except Exception as e:
        logger.error(f"Error writing lines to file: {e}")
        return False


def read_lines_from_file(file_path: str, encoding: str = 'utf-8') -> List[str]:
    """Read all lines from a file."""
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return []

        with open(file_path, 'r', encoding=encoding) as file:
            return [line.rstrip('\n') for line in file.readlines()]
    except Exception as e:
        logger.error(f"Error reading lines from file: {e}")
        return []


# =======================================
# CSV OPERATIONS
# =======================================

def write_line_to_csv(file_path: str, line: str, encoding: str = 'utf-8') -> bool:
    """Write a single line to a CSV file."""
    try:
        ensure_directory_exists(file_path)
        with open(file_path, 'a', newline='', encoding=encoding) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(line.split(","))
        return True
    except Exception as e:
        logger.error(f"Error writing line to CSV: {e}")
        return False


def write_to_csv(file_path: str, lines: Union[List[str], Tuple[str, ...]], 
                mode: str = 'a', encoding: str = 'utf-8') -> bool:
    """
    Write multiple lines to a CSV file.
    Default behavior is to append to the file, not overwrite it.
    Change mode to 'w' to overwrite.
    """
    try:
        ensure_directory_exists(file_path)

        # Write one line at a time for append mode
        if mode == 'a':
            success = True
            for line in lines:
                result = write_line_to_csv(file_path, line, encoding)
                if not result:
                    success = False
            return success

        # Overwrite and write all at once
        else:
            with open(file_path, mode, newline='', encoding=encoding) as csvfile:
                writer = csv.writer(csvfile)
                for line in lines:
                    writer.writerow(line.split(","))
            return True
    except Exception as e:
        logger.error(f"Error writing to CSV: {e}")
        return False


def read_from_csv(file_path: str, encoding: str = 'utf-8') -> List[str]:
    """Read all lines from a CSV file."""
    lines = []
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return lines

        with open(file_path, 'r', newline='', encoding=encoding) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                lines.append(",".join(row))
        return lines
    except Exception as e:
        logger.error(f"Error reading from CSV: {e}")
        return lines


# =======================================
# JSON OPERATIONS
# =======================================

def write_to_json(file_path: str, data: Union[Dict, List], indent: int = 4, 
                  encoding: str = 'utf-8') -> bool:
    """Write dictionary or list data to a JSON file."""
    try:
        ensure_directory_exists(file_path)
        with open(file_path, 'w', encoding=encoding) as json_file:
            json.dump(data, json_file, indent=indent)
        return True
    except Exception as e:
        logger.error(f"Error writing to JSON file: {e}")
        return False


def update_json(file_path: str, data: Dict, encoding: str = 'utf-8') -> bool:
    """Update an existing JSON file with new data, preserving existing data."""
    try:
        current_data = {}
        if os.path.exists(file_path):
            current_data = read_from_json(file_path, encoding)
            if current_data is None:
                current_data = {}
        
        # Update the current data with new data
        if isinstance(current_data, dict):
            current_data.update(data)
            return write_to_json(file_path, current_data, encoding=encoding)
        else:
            logger.error(f"Existing JSON is not a dictionary: {file_path}")
            return False
    except Exception as e:
        logger.error(f"Error updating JSON file: {e}")
        return False


def read_from_json(file_path: str, encoding: str = 'utf-8') -> Union[Dict, List, None]:
    """Read data from a JSON file."""
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None

        with open(file_path, 'r', encoding=encoding) as json_file:
            return json.load(json_file)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return None
    except Exception as e:
        logger.error(f"Error reading from JSON file: {e}")
        return None
    
    
# =======================================
# OTHER HELPERS
# =======================================

def list_files_without_extension(directory_path: str) -> List[str]:
    try:
        if not os.path.exists(directory_path):
            logger.error(f"Directory not found: {directory_path}")
            return []
            
        result = []
        
        for file in os.listdir(directory_path):
            if os.path.isfile(os.path.join(directory_path, file)):
                filename_without_ext = os.path.splitext(file)[0]
                result.append(filename_without_ext)
                
        return result
        
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        return []