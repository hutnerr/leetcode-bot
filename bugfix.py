import asyncio
from models.app import App
from models.user import User
from utils import initializer

app: App = initializer.Initializer.initApp()

print(app.submitter.userCompletedProblem("hutnerr", "two-sum"))

user = User(0, "hutnerr", 0)

async def test():
    print(await app.submitter.userCompletedProblem(user, "two-sum"))
    
asyncio.run(test())
