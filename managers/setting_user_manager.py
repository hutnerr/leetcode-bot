import os

# helper function to determine the filepath 
def determineFilePath(serverID: str, userID: str, event: str) -> str:
    if event.lower().strip() == "problems":
        eventFN = "p_opt_users.txt"
    elif event.lower().strip() == "contests":
        eventFN = "contest_opt_users.txt"
    else:
        print("ERROR")

    filepath = os.path.join("data", "server_configs", serverID, eventFN)
    return filepath

# helper function to check if a user is opted in
def isOpted(serverID: str, userID: str, event: str) -> bool:
    filepath = determineFilePath(serverID, userID, event)

    with open(filepath, "r") as file:
        lines = file.readlines()

        print(lines)
        
        lines = [line.strip() for line in lines]
        return userID in lines

# Main opt in / out functions
# checks if a user from a server is opted in / out and toggles it on / off
# event is either "problems" or "contests"
def opt(serverID: str, userID: str, event: str) -> None:
    filepath = determineFilePath(serverID, userID, event)

    with open(filepath, "r+") as file:
        lines = file.readlines()

        # have to remove the /n from the lines I read in 
        lines = [line.strip() for line in lines]

        if userID in lines:            
            lines.remove(userID)
        else:
            lines.append(userID)

        # add the newlines back in as i retrieved them
        lines = [line + "\n" for line in lines]

        file.seek(0)
        file.writelines(lines)
        file.truncate()