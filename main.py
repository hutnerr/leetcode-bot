from managers import daily_problem_manager as dpm
from managers import problem_info_manager as pim
from tools import printer as pr

slug = dpm.getOfficialDailyProblemSlug()
info = pim.getProblemInfo(slug)

pr.printDict(info)

