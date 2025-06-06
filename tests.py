from testing import int_services as services_testing
from testing import int_mediator as mediator_testing
from testing import int_bucket as bucket_testing

def services_integration_tests() -> bool:
    print("===== Services Integration Tests =====")
    tests = [
        ("CacheService\t", services_testing.testCacheService),
        ("ProblemService\t", services_testing.testProblemService),
        ("QueryService\t", services_testing.testQueryService), # api query heavy
        ("Lifecycle\t", services_testing.lifecycleTest),
    ]
    return performTests(tests)
    
def buckets_integration_tests() -> bool:
    print("===== Buckets Integration Tests =====")
    tests = [
        ("StaticTime\t", bucket_testing.testStaticTimeBucket),
        ("ContestTime\t", bucket_testing.testContestTimeBucket),
        ("ProblemBucket\t", bucket_testing.testProblemBucket),
    ]
    return performTests(tests)
    
    
def mediators_integration_tests() -> bool:
    print("===== Mediator Integration Tests =====")
    tests = [
        ("Mediator\t", mediator_testing.testAlertBuilder),
    ]
    return performTests(tests)
    

def performTests(tests) -> bool:
    all_passed = True
    for name, test_func in tests:
        result, reason = test_func()
        if result:
            print(f"{name}: PASSED")
        else:
            print(f"{name}: FAILED - {reason}")
            all_passed = False
    print()
    return all_passed

def testAll() -> bool:
    res1 = services_integration_tests()
    res2 = buckets_integration_tests()
    res3 = mediators_integration_tests()

    if res1 and res2 and res3:
        print("======================\n")
        print("ALL TESTS SUCCESS")
    else:
        print("FAILED :(")

# testAll()
# services_integration_tests()
# buckets_integration_tests()
mediators_integration_tests()