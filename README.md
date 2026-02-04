## Overview
The goal of this bot is to encourage and enable LeetCoding within a Discord server. It achieves through the use of distributing personalized reoccurring server problems.

These problems can be configured to be sent out on specific days of the week at specific times. The difficulty as well as if selection of premium problems can also be configured.

Besides the configurable problems, the bot also provides a more baseline set of features. Such as the ability to receive a notification based on how far away a contest is, notifications for the official daily problem, as well as notifications for when the contests become active.

This was a personal project and has no official affiliation with LeetCode. 

**Links**
- [Invite Link](https://discord.com/oauth2/authorize?client_id=1392738606120173719&permissions=2147616768&integration_type=0&scope=bot)
- [Top.gg Link](https://top.gg/bot/1392738606120173719)
- [Blog Post](https://www.hunter-baker.com/pages/blog/blog-07-14-2025.html)
- [Project Reflection](https://www.hunter-baker.com/pages/projects/leetcode-bot.html)
- [Help & Tutorial Page](https://www.hunter-baker.com/pages/other/beastcode-help.html)

## Getting Started
To get started, I recommend using `/help`. It will briefly explain a majority of the implicit aspects of the bot. After that, you can start configuring your server through `/serverconfig`. Then configure your problems with `/problemconfig`. There is a limit of 5 reoccurning problems, but each one can be sent on numerous days as well as have variable difficulty. For a full walkthrough, simply visit the tutorial page [here](https://www.hunter-baker.com/pages/other/beastcode-help.html).

## Commands
**Main Commands**
- `lcproblem <dif> <premium*>` - Posts a problem for users to solve.
- `dailylcproblem` - Posts the LeetCode daily problem.
- `contests` - Displays upcoming contest times

**Competition Commands**
- `submitproblems` - Submits recently completed problems. Get's points if they were active. 
- `leaderboard` - Displays the current point leaderboard.
- `rank <user*>` - Displays the current leaderboard position of a user. 

**Config & Status Commands**
- `userinfo <user*>` - Displays user information.
- `setusername <username>` - Sets the LeetCode username of the user.
- `deleteuser` - Deletes a user's config.
- `problemconfig <problemID>` - Allows configuration of problems.
- `probleminfo` - Displays information about all configured problems. 
- `problemactive` - Displays the problems that can be submitted for points.
- `deleteproblem <problemID>` - Deletes a problem's config.
- `serverconfig <setting group>` - Allows configuration of server settings.
- `serverinfo` - Displays information about a server's config. 
- `resetdupes` - Clears a server's duplicate problems. 
- `deleteserver` - Deletes a server's config. 

**Misc. Commands**
- `about` - Displays some information about the bot.
- `report` - Provides the GitHub link so users can report bugs. 
- `help <command*>` - Explains background info and give details about an individual command.
- `vote` - Provides a link to Top.gg to show support
- `tutorial` - Provides a link to the [Help & Tutorial Page](https://www.hunter-baker.com/pages/other/beastcode-help.html).

## Setup
To set this up locally, you would need to provide your own Discord key. You would have to have a `key.json` file within the data folder. You also would need to `pip install -r requirements.txt` which is located in the root.

```json
{
  "key": "string — production API key",
  "testkey": "string — local testing API key",
  "id": int — Discord user ID for error logging
}
```

## Showcase
<img src="https://www.hunter-baker.com/resources/images/projects/leetcode-bot.png">
<img src="https://www.hunter-baker.com/resources/images/beastcode-walkthrough/bc-example.png">
<img src="https://www.hunter-baker.com/resources/images/beastcode-walkthrough/bc-example2.png">

