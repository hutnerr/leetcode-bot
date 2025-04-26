from core.query_manager import QueryManager, Query
from core.cache_manager import CacheManager
from pprint import pprint

cman = CacheManager()
cman.updateCache()

qman = QueryManager()
vars = {}

# get the daily problem
out = qman.performQuery(Query.DAILY_PROBLEM, vars)
slug = out["data"]["challenge"]["question"]["titleSlug"]

if slug not in cman.cachedProblems:
    out = qman.performQuery(Query.QUESTION_INFO, {"titleSlug" : slug})
    print("Performed Query")
else:
    out = cman.cachedProblems[slug]
    print("Got from Cache")
    
slug = "two-sum"
if slug not in cman.cachedProblems:
    out = qman.performQuery(Query.QUESTION_INFO, {"titleSlug" : slug})
    print("Performed Query")
else:
    out = cman.cachedProblems[slug]
    print("Got from Cache")
    
# pprint(out)

cman.writeProblemToJSON(out) # cache the problem 