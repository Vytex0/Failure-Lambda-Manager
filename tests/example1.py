from objects.test import Test
from objects.failureMode import FailureMode
from objects.failure import Failure

### This file can have any shape you want, the only important part is that it must run the tests itself

# We define a first test which will affect the following functions at the same time:
#  ConfigChangedFunction in latency failure mode, 50% of the time, with a random latency between 1000ms and 2500ms
#  FillDatabasesCustomResource in exception failure mode, 30% of the time, with a fixed exception message
#  GetIoTEndpointFunction in denylist failure mode, 100% of the time, which blocks access to all S3 and DynamoDB services
test1 = Test("Test n°1", [
    Failure("ConfigChangedFunction", FailureMode.LATENCY, 0.5, minLatency=1000, maxLatency=2500),
    Failure("FillDatabasesCustomResource", FailureMode.EXCEPTION, 0.3, exceptionMsg="An exception has occured."),
    Failure("GetIoTEndpointFunction", FailureMode.DENYLIST, 1, denylist=["s3.*.amazonaws.com", "dynamodb.*.amazonaws.com"]),
    ])

# We define a second test which will affect the following functions at the same time:
#  GetOrderByIdFunction in diskspace failure mode, 10% of the time, which will create 120 Mb file in the temporary folder
#  PublisherFunctionAdmin in status code failure mode, 80% of the time, with 501 returned status code
test2 = Test("Test n°2", [
    Failure("GetOrderByIdFunction", FailureMode.DISKSPACE, 0.1, diskSpace=120),
    Failure("PublisherFunctionAdmin", FailureMode.STATUSCODE, 0.8, statusCode=501),
    ])

# We put all tests in a list to handle them afterwards
tests = [test1, test2]

# For each test, we can decide when to run and when to stop it manually
for test in tests:
    while(str(input(f"Please write 'run' to start the test '{test.getName()}': ")).lower() != "run"):
        pass
    test.run()
    while(str(input("Please write 'stop' to interrupt the current test: ")).lower() != "stop"):
        pass
    test.stop()
    print("="*20)