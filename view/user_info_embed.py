import discord.embeds
from models.user import User

class UserInfoEmbed(discord.Embed):
    def __init__(self, discUser: discord.User, user: User, problemInfo: dict):
        super().__init__(title=discUser.name)
        self.color = discUser.accent_color or discord.Color.blurple()

        self.set_thumbnail(url=discUser.display_avatar.url)
        self.add_field(name="Points", value=user.points, inline=False)
        
        if leetcodeUsername := user.leetcodeUsername:
            self.add_field(name="LeetCode Username", value=f"[{leetcodeUsername}](https://leetcode.com/u/{leetcodeUsername})", inline=False)
        else:
            self.add_field(name="LeetCode Username", value="set using `/setusername`", inline=False)

        if problemInfo:
            data = problemInfo["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]
            result = {item['difficulty']: item['count'] for item in data}

            strbuilder = ""
            for difficulty, count in result.items():
                strbuilder += f"**{difficulty.capitalize()}**: {count}\n"
            self.add_field(name="Problem Completed", value=strbuilder, inline=False)