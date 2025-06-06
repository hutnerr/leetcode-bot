from testing import int_services as services_testing
from testing import int_mediator as mediator_testing
from testing import int_bucket as bucket_testing

def services_integration_tests() -> None:
    print("===== Services Integration Tests =====")
    tests = [
        ("CacheService\t", services_testing.testCacheService),
        ("ProblemService\t", services_testing.testProblemService),
        ("QueryService\t", services_testing.testQueryService), # api query heavy
        ("Lifecycle\t", services_testing.lifecycleTest),
    ]
    performTests(tests)
    
def buckets_integration_tests() -> None:
    print("===== Buckets Integration Tests =====")
    tests = [
        ("StaticTime\t", bucket_testing.testStaticTimeBucket),
        ("ContestTime\t", bucket_testing.testContestTimeBucket),
        ("ProblemBucket\t", bucket_testing.testProblemBucket),
    ]
    performTests(tests)
    
    
def mediators_integration_tests() -> None:
    print("===== Mediator Integration Tests =====")
    tests = [
        ("Mediator\t", mediator_testing.testAlertBuilder),
    ]
    performTests(tests)
    

def performTests(tests) -> None:
    all_passed = True
    for name, test_func in tests:
        try:
            test_func() 
            print(f"{name}: PASSED")
        except AssertionError as e:
            print(f"{name}: FAILED - {e}")
            all_passed = False
    print()
    return all_passed

def testAll() -> None:
    res1 = services_integration_tests()
    res2 = buckets_integration_tests()
    res3 = mediators_integration_tests()

    # No need to check results, as asserts will raise on failure
    print("======================\n")
    print("ALL TESTS COMPLETED")

# testAll()
# services_integration_tests()
buckets_integration_tests()
# mediators_integration_tests()
