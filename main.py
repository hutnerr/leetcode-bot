import random
from utils.initializer import Initializer

def main():
    NSERVERS = 10
    NPROBLEMS = 500
    NUSERS = 100

    # app = Initializer.initApp(True, nservers=NSERVERS, nproblems=NPROBLEMS, nusers=NUSERS)
    app = Initializer.initApp()

    submitter = app.submitter
    user = random.choice(list(app.users.values()))
    user.leetcodeUsername = "hutnerr"
    slug = "maximum-difference-by-remapping-a-digit"
    
    print(submitter.userCompletedProblem(user, slug))



if __name__ == "__main__":
    main()