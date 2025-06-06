from utils.initializer import Initializer

def main():
    NSERVERS = 10
    NPROBLEMS = 500
    NUSERS = 100

    # app = Initializer.initApp(True, nservers=NSERVERS, nproblems=NPROBLEMS, nusers=NUSERS)
    app = Initializer.initApp()
    # app.problemBucket.printBucketClean()
    print(app.users)
    


if __name__ == "__main__":
    main()