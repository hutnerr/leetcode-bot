from testing import int_services as services_testing

def services_integration_tests():
    print("===== Services Integration Tests =====")
    tests = [
        ("CacheService\t", services_testing.testCacheService),
        ("ProblemService\t", services_testing.testProblemService),
        ("QueryService\t", services_testing.testQueryService), # api query heavy
        ("Lifecycle\t", services_testing.lifecycleTest),
    ]
    performTests(tests)

def performTests(tests):
    all_passed = True
    for name, test_func in tests:
        result, reason = test_func()
        if result:
            print(f"{name}: PASSED")
        else:
            print(f"{name}: FAILED - {reason}")
            all_passed = False
    print("All tests passed!" if all_passed else "Some tests failed.")

services_integration_tests()
