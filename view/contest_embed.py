import discord.embeds

class ContestEmbed(discord.Embed):
    def __init__(self, contests: dict):
        super().__init__(title="Upcoming Contests", url="https://leetcode.com/contest/")

        for contest in contests.values():
            self.add_field(
                name=f"{contest['title']}",
                value=f"{contest['startTime']}\n{contest['timeAway']} away\n**[Join Contest]({contest['url']})**",
                inline=False
            )

        # self.set_footer(text="LeetCode Contest")
        self.set_thumbnail(url="https://leetcode.com/static/images/LeetCode_logo_rvs.png")
        self.color = discord.Color.orange()
