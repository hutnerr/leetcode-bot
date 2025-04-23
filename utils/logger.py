from utils import file_helper
import datetime

LOG_FILE_PATH = "data/log.txt"

def log(message, level="INFO", include_timestamp=True):
    # log levels: INFO, ERROR
    try:
        log_entry = ""
        if include_timestamp:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] [{level}] {message}"
        else:
            log_entry = f"[{level}] {message}"
        
        return file_helper.write_line_to_file(LOG_FILE_PATH, log_entry)
            
    except Exception as e:
        print(f"Error writing to log file: {e}")
        print(f"Original message: [{level}] {message}")
        return False

def info(message):
    return log(message, "INFO")

def error(message):
    return log(message, "ERROR")