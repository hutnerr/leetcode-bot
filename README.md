## Overview
The purpose of this bot is to encourage and enable LeetCoding within a Discord server. It achieves through the use of personalized server daily problems. Meaning that the server can select a set difficulty, the time it will be posted, if premium problems are included, and more. 

There is also other functionality that will notify the server about upcoming contests. The timing of these notifications can be set and modified. 

By default nothing is turned on. You must use the `/settings` command to set the server's config and `/setchannel` to set an output channel. If you want a full walkthrough use the `/tutorial` command. 

[Invite Link]()

## Commands
Note: These are not set in stone will change during development. 

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
- Add friendly server competition functionality.
  - Badges, leaderboards, etc.
- Optional alert types and ways. 

