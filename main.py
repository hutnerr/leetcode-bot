import sqlite3

""" 
Users
    - userID           : int   : The ID of the user these settins pertain to 
    - leetcodeUsername : str   : The LeetCode username for this user
    - serverID         : int   : The server ID that this user is apart of
    - weeklyOpt        : bool  : Alerts for weekly contests
    - biweeklyOpt      : bool  : Alerts for biweekly contests
    - problemsOpt      : bool  : Alerts for server problems 
    - officialDailyOpt : bool  : Alerts for the official dailies 
"""

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('data/databases/users.db')
cursor = conn.cursor()

# Create Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    userID INTEGER PRIMARY KEY,
    leetcodeUsername TEXT NOT NULL,
    serverID INTEGER NOT NULL,
    weeklyOpt BOOLEAN NOT NULL,
    biweeklyOpt BOOLEAN NOT NULL,
    problemsOpt BOOLEAN NOT NULL,
    officialDailyOpt BOOLEAN NOT NULL
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()