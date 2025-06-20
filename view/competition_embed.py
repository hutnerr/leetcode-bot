import discord.embeds

class LeaderboardEmbed(discord.Embed):
    def __init__(self, leaderboard: tuple[int, str, int]):
        super().__init__(title="Point Leaderboard")
        
        leaderboardstr = ""
        for i in range(len(leaderboard)):
            if i == 15: # limit of 15 on the board
                break
            points, member = leaderboard[i]
            username = member.name
            
            leaderboardstr += f"{i + 1:>2}. `{username:<30}` {points:>6} pts\n"
            
        self.description = leaderboardstr
        self.color = discord.Color.green()
        self.set_footer(text="Use /rank to see your own rank")
