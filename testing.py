from core.managers.query_manager import QueryManager

PROBLEM = "two-sum"
USERNAME = "hutnerr"

man = QueryManager()

# out = man.getDailyProblem()
# print(out)

# out = man.getUpcomingContests()
# print(out)

# out = man.getUserProfile(USERNAME)
# print(out)

# out = man.getUserRecentAcceptedSubmissions(USERNAME, 1)
# print(out)

out = man.getQuestionInfo(PROBLEM)
print(out)