import asyncio
from models.app import App
from models.user import User
from utils import initializer

app: App = initializer.Initializer.initApp()

pinfo = asyncio.run(app.queryService.getQuestionInfo("two-sum"))
app.cacheService.cacheProblem(pinfo)

userinfo = asyncio.run(app.queryService.getUserProblemsSolved("hutnerr"))
print(userinfo)

