> This project is completed and likely will not receive any new features, only maintenance updates.

## Overview
A Discord bot that encourages LeetCode practice within a server by automatically posting personalized, recurring coding problems.

It's intended for servers that want structured, recurring practice with light competition elements. Server administrators choose which days and times problems are posted, their difficulty, and whether premium problems are included.

**Features:**
- **Scheduled Problems**: Up to 5 recurring problems, each posted on any number of days with its own difficulty
- **Competition**: Users submit problems they've solved for points on a server leaderboard
- **Contest Notifications**: Reminders for upcoming contests and alerts when they go live
- **Daily Problem**: Notifications for the official daily LeetCode problem

**Links:**
- [Invite Link](https://discord.com/oauth2/authorize?client_id=1392738606120173719&permissions=2147616768&integration_type=0&scope=bot)
- [Top.gg](https://top.gg/bot/1392738606120173719)
- [Help Page](https://www.hunter-baker.com/pages/other/beastcode-help.html)

> View more about the project on its [showcase page](https://www.hunter-baker.com/pages/projects/leetcode-bot.html).

## Usage
To get started, I recommend using `/help`, which briefly explains most of the implicit parts of the bot. After that, configure your server with `/serverconfig`, then your problems with `/problemconfig`. For a full walkthrough, visit the [Help Page](https://www.hunter-baker.com/pages/other/beastcode-help.html).

> Arguments marked with `*` are optional.

**Main Commands**
- `/lcproblem <dif> <premium*>` - Posts a problem for users to solve.
- `/dailylcproblem` - Posts the LeetCode daily problem.
- `/contests` - Displays upcoming contest times.

**Competition Commands**
- `/submitproblems` - Submits recently completed problems. Earns points if they were active.
- `/leaderboard` - Displays the current point leaderboard.
- `/rank <user*>` - Displays the current leaderboard position of a user.

**Config & Status Commands**
- `/userinfo <user*>` - Displays user information.
- `/setusername <username>` - Sets the LeetCode username of the user.
- `/deleteuser` - Deletes a user's config.
- `/problemconfig <problemID>` - Configures a problem.
- `/probleminfo` - Displays information about all configured problems.
- `/problemactive` - Displays the problems that can be submitted for points.
- `/deleteproblem <problemID>` - Deletes a problem's config.
- `/serverconfig <setting group>` - Configures server settings.
- `/serverinfo` - Displays information about a server's config.
- `/resetdupes` - Clears a server's duplicate problems.
- `/deleteserver` - Deletes a server's config.

**Misc. Commands**
- `/about` - Displays some information about the bot.
- `/report` - Provides the GitHub link so users can report bugs.
- `/help <command*>` - Explains background info and gives details about an individual command.
- `/vote` - Provides a link to Top.gg to show support.
- `/tutorial` - Provides a link to the [Help Page](https://www.hunter-baker.com/pages/other/beastcode-help.html).

## Showcase
<img src="https://www.hunter-baker.com/assets/projects/beast_code/leetcode-bot.png" alt="BeastCode bot overview">
<img src="https://www.hunter-baker.com/assets/projects/beast_code/bc-example.png" alt="Example problem posted by the bot">
<img src="https://www.hunter-baker.com/assets/projects/beast_code/bc-example2.png" alt="Example problem posted by the bot">

## Setup
To run this locally, you need your own Discord key, stored in a `key.json` file in the `data` folder.

```bash
pip install -r requirements.txt
```

```json
{
  "key": "string — production API key",
  "testkey": "string — local testing API key",
  "id": int — Discord user ID for error logging
}
```

## License & Credits
The project is licensed under the MIT License.

This is a personal project and has no official affiliation with LeetCode.

## Support
If you found this project helpful or enjoyable, and want to support future work, you can buy me a coffee on Ko-fi
<br><br>
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/S6S71TM9XT)
