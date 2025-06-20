import os

# if create is false, just check if the directory exists.
def directoryExists(filePath: str, create: bool = False) -> bool:
    try:
        directory = os.path.dirname(filePath)
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


def fileExists(filePath: str) -> bool:
    return os.path.isfile(filePath)


# returns a list of files in the given directory
# does not include other directories or subdirectories
def getFilesInDirectory(directory: str, showExtensions: bool = True) -> list[str]:
    if not os.path.isdir(directory):
        return []

    # if show_extensions is true, return the full file names with extensions
    # e.g. ['file1.txt', 'file2.py'] otherwise return just the file names without extensions
    # e.g. ['file1', 'file2']
    if showExtensions:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    else:
        return [os.path.splitext(f)[0] for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    
def deleteFile(filePath: str) -> bool:
    try:
        if os.path.isfile(filePath):
            os.remove(filePath)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False