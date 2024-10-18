from tools import printer as pr
from tools import time_helper as th
from tools import database_helper as dbh
from tools.consts import DatabaseTables as dbt

from managers import contest_time_manager as ctm

SID = 335526354206326786

# dbh.updateRow(dbt.PROBLEMS.value, "dow", 1, f"serverID = {SID}")

dbh.printRows(dbt.PROBLEMS.value)

