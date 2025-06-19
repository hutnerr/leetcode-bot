from testing.generator import GeneratedServers
from utils.initializer import Initializer
from models.app import App

# mediator integration testing
def makeApp() -> App:
    servers = GeneratedServers().collectServers()
    return Initializer.initApp(passedInServers=servers)


# test duplicates problem "previous-problems" in server
def testDuplicateProblem() -> bool:
    app = makeApp()
    server = app.servers[1]
    
    # check direct duplicates 
    slug = "two-sum"
    slug2 = "maximum-difference-by-remapping-a-digit"
    assert server.isProblemDuplicate(slug), f"Problem {slug} should be a duplicate in server {server.serverID}"
    assert not server.isProblemDuplicate(slug2), f"Problem {slug2} should not be a duplicate in server {server.serverID}"

    # check duplicates by trying to add an active problem that is already in previous problems
    assert not server.addActiveProblem(slug, "easy", 0), f"Should not be able to add active problem {slug} as it is a duplicate"
    assert server.addActiveProblem(slug2, "easy", 0), f"Should be able to add active problem {slug2} as it is not a duplicate"

    return True
