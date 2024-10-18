from managers import server_settings_manager as ssm
from tools import database_helper as dbh
from tools.consts import DatabaseTables as dbt

# dbh.printRows(dbt.SERVERS.value)
# x = ssm.getAndParseServerSettings('335526354206326786')

x = ssm.getServerSettings(335526354206326786)


print(x)