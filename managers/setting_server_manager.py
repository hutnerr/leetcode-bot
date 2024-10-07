import os

# ----------------------------------------------------
# Problem Time Functions 
# ----------------------------------------------------

# This should allow for a server to have like 3 problems on the same day for example
# and it should only remove one of them
def toggleTime(serverID, day_of_week, hour):
    filepath = os.path.join("data", "problem_times", day_of_week, f"{hour}.txt")
    
    with open(filepath, "r+") as file:
        lines = file.readlines()

        lines = [line.strip() for line in lines]

        # FIXME
        # This wont work because I want to have more than
        # 1 occurence allowed per file
        if serverID in lines:            
            lines.remove(serverID)
        else:
            lines.append(serverID)

        # add the newlines back in as i retrieved them
        lines = [line + "\n" for line in lines]

        file.seek(0)
        file.writelines(lines)
        file.truncate()



