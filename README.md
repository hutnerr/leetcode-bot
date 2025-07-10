## Overview
The goal of this bot is to encourage and enable LeetCoding within a Discord server. It achieves through the use of distributing personalized reoccurinng server problems. 

There is also other functionality that will notify the server about upcoming contests. The timing of these notifications can be set and modified. 

This was a personal project and has no official affiliation with LeetCode. 

**Links**
- [Invite Link](https://discord.com/oauth2/authorize?client_id=1392738606120173719&permissions=2147616768&integration_type=0&scope=bot)
- [Top.gg Link]()
- [Blog Post]()
- [Project Reflection]()

## Getting Started
To get started, I recommend using `/help`. It will briefly explain a majority of the implicit aspects of the bot. After that, you can start configuring your server through `/sconfig`. Then configure your problems with `/pconfig`. There is a limit of 5 reoccurning problems, but each one can be sent on numerous days as well as have variable difficulty. 

## Commands
**Main Commands**
- `problem <dif> <premium*>` - Posts a problem for users to solve.
- `dailyproblem` - Posts the LeetCode daily problem.
- `contests` - Displays upcoming contest times

**Competition Commands**
- `submit` - Submits recently completed problems. Get's points if they were active. 
- `leaderboard` - Displays the current point leaderboard.
- `rank <user*>` - Displays the current leaderboard position of a user. 

**Config & Status Commands**
- `uinfo <user*>` - Displays user information.
- `setusername <username>` - Sets the LeetCode username of the user.
- `deluser` - Deletes a user's config.
- `pconfig <problemID>` - Allows configuration of problems.
- `pinfo` - Displays information about all configured problems. 
- `pactive` - Displays the problems that can be submitted for points.
- `delproblem <problemID>` - Deletes a problem's config.
- `sconfig <setting group>` - Allows configuration of server settings.
- `sinfo` - Displays information about a server's config. 
- `resetdupes` - Clears a server's duplicate problems. 
- `delserver` - Deletes a server's config. 

**Misc. Commands**
- `about` - Displays some information about the bot.
- `report` - Provides the GitHub link so users can report bugs. 
- `help <command*>` - Explains and give details about an individual command.
