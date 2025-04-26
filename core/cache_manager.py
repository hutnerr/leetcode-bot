from utils import file_helper
from core.problem import titleToSlug
import os

class CacheManager():
    
    CACHELOCATION = os.path.join("data", "problem_cache")
    
    cachedProblems = dict()
    
    def writeProblemToJSON(self, json):
        info = json["data"]["question"]
        id = info["questionFrontendId"]
        slug = titleToSlug(info["title"])
        path = os.path.join(self.CACHELOCATION, f"{slug}.json")
        file_helper.write_to_json(path, json)
        self.cachedProblems[slug] = json # write the mf name
        
    def updateCache(self):
        
        problems = file_helper.list_files_without_extension(self.CACHELOCATION)
        
        for problem in problems:
            path = os.path.join(self.CACHELOCATION, f"{problem}.json")
            json_data = file_helper.read_from_json(path)
            self.cachedProblems[problem] = json_data