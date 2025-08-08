from models.app import App
from utils import initializer

app: App = initializer.Initializer.initApp()

# bulk cache all problems

for key in app.problemService.problemSets:
    for difficulty in app.problemService.problemSets[key]:
        for problem in app.problemService.problemSets[key][difficulty]:
        
            if not app.cacheService.existsInCache(problem):
                print(f"Adding {problem} to cache...")
                qinfo = app.queryService.getQuestionInfoRequests(problem)
                app.cacheService.cacheProblem(qinfo)