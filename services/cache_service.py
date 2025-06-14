import os

from utils import json_helper as jsonh
from utils import file_helper as fh
from utils import problem_helper as probHelper

# service that handles operations related to caching
class CacheService:
    CACHELOCATION: str = os.path.join("data", "problem_cache")

    def __init__(self):
        self.cachedProblems = dict()
        self.initCache()

    # initializes the cache by reading all json files in the cache directory
    # and storing them in the cachedProblems dict
    def initCache(self):
        problems = fh.getFilesInDirectory(self.CACHELOCATION, showExtensions=False)

        for prob in problems:
            path = os.path.join(self.CACHELOCATION, f"{prob}.json")
            json_data = jsonh.readJSON(path)
            self.cachedProblems[prob] = json_data

    # inserts a problem into the cache
    def cacheProblem(self, json):
        info = json["data"]["question"]
        slug = probHelper.titleToSlug(info["title"])
        path = os.path.join(self.CACHELOCATION, f"{slug}.json")
        jsonh.writeJSON(path, json)
        self.cachedProblems[slug] = json

    def existsInCache(self, slug: str) -> bool:
        return slug in self.cachedProblems

    def getFromCache(self, slug: str) -> dict | None:
        if slug in self.cachedProblems:
            return self.cachedProblems[slug]
        else:
            return None
