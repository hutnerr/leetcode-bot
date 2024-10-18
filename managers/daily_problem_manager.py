from tools.consts import Query as q
from tools import query_helper as qh

from managers import problem_info_manager as pim

def getOfficialDailyProblemSlug():
    out = qh.performQuery(q.DAILY_PROBLEM.value, {})
    return out['data']['challenge']['question']['titleSlug']

def getOfficialDailyProblemInfo():
    return pim.getProblemInfo(getOfficialDailyProblemSlug())