from objects.parameter import Parameter
from objects.failureMode import FailureMode
from utils.logger import log
from utils.config import PARAMETER_PREFIX

class Failure():
    def __init__(self, functionName, failureMode, rate, minLatency=None, maxLatency=None, exceptionMsg=None, statusCode=None, diskSpace=None, denylist=None):
        self.parameter = Parameter(PARAMETER_PREFIX+functionName)
        self.functionName = functionName
        self.failureMode = failureMode
        self.rate = rate
        self.minLatency = minLatency
        self.maxLatency = maxLatency
        self.exceptionMsg = exceptionMsg
        self.statusCode = statusCode
        self.diskSpace = diskSpace
        self.denylist = denylist

    def run(self):
        log("info", f"Preparing failure on {self.functionName} with failure mode {self.failureMode.value}.")
        self.parameter.setRate(self.rate)
        
        if(self.failureMode == FailureMode.LATENCY):
            if(self.minLatency == None or self.maxLatency == None):
                raise Exception(f"minLatency and maxLatency must be set for failureMode={self.failureMode.value}")
            self.parameter.setMinLatency(self.minLatency).setMaxLatency(self.maxLatency)
        elif(self.failureMode == FailureMode.EXCEPTION):
            if(self.exceptionMsg == None):
                raise Exception(f"exceptionMsg  must be set for failureMode={self.failureMode.value}")
            self.parameter.setExceptionMessage(self.exceptionMsg)
        elif(self.failureMode == FailureMode.DENYLIST):
            if(self.denylist == None):
                raise Exception(f"denylist  must be set for failureMode={self.failureMode.value}")
            self.parameter.setDenylist(self.denylist)
        elif(self.failureMode == FailureMode.DISKSPACE):
            if(self.diskSpace == None):
                raise Exception(f"diskSpace  must be set for failureMode={self.failureMode.value}")
            self.parameter.setDiskSpace(self.diskSpace)
        elif(self.failureMode == FailureMode.STATUSCODE):
            if(self.statusCode == None):
                raise Exception(f"statusCode  must be set for failureMode={self.failureMode.value}")
            self.parameter.setStatusCode(self.statusCode)

        self.parameter.setEnabled(True)
        self.parameter.save()
        log("info", f"Failure on {self.functionName} launched.")

    def stop(self):
        log("info", f"Stopping failure on {self.functionName}.")
        self.parameter.setEnabled(False)
        self.parameter.save()
        log("info", f"Failure on {self.functionName} stopped.")