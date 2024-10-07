# Statement
This is meant to be a practice bot that facilitates LeetCoding within a discord server. It does this through allowing a user to set parameters and then provide them with problems. 

Parameters Include:
- Frequency of problem. (days of week, time)
- Difficulty of problem. (easy, med, hard, all)
- Include premium problems (y / n)

The result is a customized bot that outputs a tailed problemset to a server at the times they want it. 

# Design Overview
Discord Commands
- problems.py
    - /p <dif> <premium>: Gets the user a problem based on the specified parameters
- help.py
    - /tutorial : provides a walkthrough or examples on how to use the bot. likely ephemeral
    - /help <cmd> : individual help per each command  
- info.py
    - /about : posts serverinfo. contains the mission statement. github repo. last dataset update, etc. in an embed 
    - /contestwhen : posts an embed that tells the user when the next contests are. embed contains both weekly and biweekly. 
- server.py
    - /toggleroles : change if you want the server to have roles that get @ messages. create and assign them when toggled initially. if toggled off delete the roles. perform an admin check, same as settings. since creating roles probably needs admin, make this command perform a self admin check, if it doesnt have it, give an ephemeral back that says give me admin pls so i can do this. 
    - /setchannel : sets the channel the bots output should be in. 
    - /sconfig
	    - displays the servers current config settings
	    - displays how many people in the server are opted in
- users.py
    - /opt <event> : lets the user opt into / out of an event. works as a toggle. can opt into the problems or opt into the contests. output that signals the change should be ephemeral. will add / remove a role if roles are active. sends an error if server isn't setup. 
- settings.py
    - perform an admin check on anyone who called this. epehemeral result if they don't match check 
    - set <setting> : gives the user a UI interface that allows them to interact with their settings

Utilities
- looper.py (will be in cogs)
    - this handles everything that needs to be checked repeatedely and is on a loop. i.e. the main backbone of the bot
    - loop to send out dailies
    - loop to send out contest reminders
    - loop to scrape a new dataset. should refresh once a week
- problem_set_builder.py
    - this is what scrapes and builds the problemset we use for our selection. 
    - buildList()
        - scrapes the web to get a proper List of the problems that exist. 
    - buildCSV()
        - turns the list we got from scraping into a formatted CSV file
    - scrapeAndBuild()
        - combines the two functions above.
- contest_utils.py
    - increaseContestNum(contest)
        - increases the current contest number to keep track
    - getContestTime()
        - Gets the time between now and the next contest. 

Managers
- problem_manager.py:
    - getProblem()
        - returns a problem of a specific difficulty. needs to get a of up to 3 things, 
        split it then filter the dataset. then do a random Selection
    - assignColor()
        - assigns the embed a color based on its difficulty 
    - prettifyProblem()
        - turns the problem list output into an embed that looks good. the title of the embed should be a hyperlink to the problem 
- server_settings_manager.py
    - newServerFile(serverid)
        - This is a helper method for getServerFile for when it needs to add a new server
        - Will have to handle making a folder, making a json (copied from the base), and making two txt files. 
    - updateServerFile(sid, key1, key2, value)
        - Will update the base server config json file. 
    - getServerFile(sid)
        - makes a new server folder config if it doesnt exist using newServerFile
        - otherwise retuns the server file json so it can be viewed / changed. 
- user_settings_manager.py
    - addUser(file) <- the file will be contests / dailies. 
        - Will add a user to the txt file they want.
        - Used when opt is toggled.
    - removeUser(file) <- the file will be contests / dailies. 
        - Will remove a user from the txt file
        - Used when opt is toggled off. 

UI
- problem_config_selector.py
    - should be a multiple select window. 
    - has a problem field with the values, easy, medium, hard. but allow for selection of multiple values. therefore the list returned by this should be what types of problems the users want. 
- contest_alert_selector.py
    - selectbox 
    - first field is which contest
    - next field has options of which time they would like to be alerted relative to the contests. 
        - 1 hr before? 15 mins? 24 hours?
- alert_message_selector.py
    - lets you choose if you your alerts sent to:
        - @messages to all selected members
        - @message to the role if /togglerole is active
        - simple text message, no alerts
        - off, only the problem

# Data Storage
Each server gets its own folder. This folder will contain a .json config file as well
as two txt files (one for contests and one for dailies) that contains each and every user
who has "opted" in or out that way I know who to @ and include. 

contest_times
- this folder contains notepads that will contain the server ids of server that want to be notified in the occurence of this time. 
- ex. a server that is located within 6hrs and 1hrs will be notified 6 hours away from the contest as well as 1 hour away from the contest

daily_problem_times
- this folder contains a notepad of the number 0-23 which represent the hours 12am - 11pm. 
- inside of these notepads will be the ids of servers that want to be notified at this time

problems
- these simply contain the csv files of the problems that are going to be used for selection. 
- there exist 3, all, free, and paid problems to make selection a little easier 

server_configs
- this folder will contain other folder named on the server ids. 
- inside of these id folders, will be a p_opt_users.txt file. this will store the ids of all of the users who opted into participating in the server problems
- also will include a w_contest_opt_users.txt (weekly) and a biw_contest_opt_users.txt (biweekly) file which will naturally contain the users who opted into these particular contests
- a settings.json which is going to be used to store the main server functionality commands 

misc json fiesl
- contests.json : this json is used to keep track of the servers. it has the times of them hardcoded because its easier than scraping, it also contains the contest num so that i can avoid scraping entirely
- data.json : this json contains important info like the bot key
- serverbase : this is the template for the settings.json file that will be used above. it has a simple default config. it will be copied for each server then the users can change it accordingly. 

# Server Settings
Dailies
- problems: 
- premium: only, none, both

# Other Notes
Use relative filepaths. I.E. one that do NOT start with a / and go from the directory of the code running. Also use os.path.join

I think the discord.Interaction.created_at parameter is in UTC, so maybe I can use that as a subtractor

I want to be explicit where I can. Like explicit return types, explicit function args, etc. 