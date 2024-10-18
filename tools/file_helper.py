def fileToList(filepath: str) -> list:
    with open(filepath, "r") as file:
        return file.read().splitlines()

def listToFile(filepath: str, data: list):
    with open(filepath, "w") as file:
        file.truncate(0)  # Wipe the file content
        for line in data:
            file.write(f"{line}\n")