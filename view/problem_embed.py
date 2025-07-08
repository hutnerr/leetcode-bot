import discord.embeds
from utils import problem_helper as probh
from utils import markdown_helper as markdownh
import json
import re

class ProblemEmbed(discord.Embed):
    
    CHAR_LIMIT = 4096
    
    def __init__(self, slug: str, problemInfo: dict):
                
        problemInfo = problemInfo["data"]["question"]
        premium = problemInfo["isPaidOnly"]
        pid = problemInfo["questionFrontendId"]
        title = problemInfo["title"]
        difficulty = problemInfo["difficulty"]
        text = problemInfo["content"] if not premium else "This is a [premium](https://leetcode.com/subscribe/) problem. Please visit the LeetCode website to view the content."
        acceptance = json.loads(problemInfo["stats"])["acRate"]
        
        super().__init__(title=f"{pid} - {title}", url=probh.slugToURL(slug))

        text = re.sub(r'<img[^>]*>', '', text)  # remove <img> tags from the text bc they just showed up as ![](imglink)

        self.description = f"**Acceptance:** {acceptance}\n\n{markdownh.convertHTMLToMarkdown(text)}"
        self.color = self.getColor(difficulty)
        # self.set_thumbnail(url="https://leetcode.com/static/images/LeetCode_logo_rvs.png")

        # enforce a max embed text limit
        if len(self.description) > self.CHAR_LIMIT:
            self.description = self.description[:self.CHAR_LIMIT - 3] + "..."

    def getColor(self, difficulty: str) -> discord.Color:
        if difficulty == "Easy":
            return discord.Color.green()
        elif difficulty == "Medium":
            return discord.Color.orange()
        elif difficulty == "Hard":
            return discord.Color.red()
        else:
            return discord.Color.default()