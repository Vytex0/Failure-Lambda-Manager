from enum import Enum

class FailureMode(Enum):
    LATENCY = "latency"
    EXCEPTION = "exception"
    DENYLIST = "denylist"
    DISKSPACE = "diskspace"
    STATUSCODE = "statuscode"