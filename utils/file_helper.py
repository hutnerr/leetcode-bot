import os

# if create is false, just check if the directory exists.
def directoryExists(file_path: str, create: bool = False) -> bool:
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            if create:
                os.makedirs(directory)
                return True # it exists now that we created it
            else:
                return False
        return True
    except Exception as e:
        print(f"Error creating directory: {e}")
        return False


def fileExists(file_path: str) -> bool:
    return os.path.isfile(file_path)


# returns a list of files in the given directory
# does not include other directories or subdirectories
def getFilesInDirectory(directory: str, show_extensions: bool = True) -> list[str]:
    if not os.path.isdir(directory):
        return []

    # if show_extensions is true, return the full file names with extensions
    # e.g. ['file1.txt', 'file2.py'] otherwise return just the file names without extensions
    # e.g. ['file1', 'file2']
    if show_extensions:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    else:
        return [os.path.splitext(f)[0] for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]