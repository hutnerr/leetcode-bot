from managers import server_settings_manager as ssm
from managers import problem_setting_manager as psm
from tools import printer as pr

ssm.resetServer(1234567890)

# shouldnt exist
print(ssm.serverExists(1234567890))

# try and add 
ssm.addNewServer(1234567890, 123, "UTC")

# should exist
print(ssm.serverExists(1234567890))

# add problems 
psm.addProblem(1234567890, 1, "Mon", 12, "Easy", "Free")
psm.addProblem(1234567890, 2, "Tue", 12, "Easy", "Free")
psm.addProblem(1234567890, 3, "Wed", 12, "Easy", "Free")

# print out the default settings 
pr.printDict(ssm.getAndParseServerSettings(1234567890))
for p in psm.getAndParseAllProblems(1234567890):
    pr.printDict(p)

# delete all traces of server 
ssm.resetServer(1234567890)

# prove the server is gone 
print(ssm.serverExists(1234567890))

# prove it all got deleted 
pr.printDict(ssm.getAndParseServerSettings(1234567890))

for p in psm.getAndParseAllProblems(1234567890):
    pr.printDict(p)
