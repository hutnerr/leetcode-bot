## Overview
The purpose of this bot is to encourage and enable LeetCoding within a Discord server. It achieves through the use of personalized server daily problems. Meaning that the server can select a set difficulty, the time it will be posted, if premium problems are included, and more. 

There is also other functionality that will notify the server about upcoming contests. The timing of these notifications can be set and modified. 

By default nothing is turned on. You must use the `/settings` command to set the server's config. If you want a full walkthrough use the `/tutorial` command. 

[Invite Link]()

## Commands
**Main Commands**
- `/p <dif> <premium>` - Posts a problem for users to solve.

**Config & Status Commands**
- `/tutorial` - Explains and walk you through feature setup.
- `/settings <setting>` - Display a UI that allows for the modification of settings.
- `/opt <event>` - Allows a user to opt in/out of server daily events & contest notifications.
- `/toggleroles` - Creates roles to be used in notifcation messages. Deletes when toggled off.
- `/setchannel` - Sets the channel for the bot output. 
- `/sinfo` - Displays the servers current config settings as well as other misc info.
- `/about` - Displays some information about the bot itself. 

**Misc. Commands**
- `/contestwhen <contest>` - Displays the time until the next contest (weekly/biweekly).
- `/problemset` - Posts a CSV file of the LeetCode Problemset.
- `/help <command>` - Explains and give details about an individual command.

## Future Goals
- Swap to using the Leetcode API.
- Display the official Leetcode daily problem.
- Display more info in the output embed.
    - Description
    - Accepted %
- Add friendly server competition functionality.
- Functionality regarding user-specific study plans. 
