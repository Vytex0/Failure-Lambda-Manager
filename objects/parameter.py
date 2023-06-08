from objects.failureMode import FailureMode
from utils.aws import ssm
import json
from utils.config import PARAMETER_PREFIX

class Parameter():
    def __init__(self, name):
        self.name = name
        self.value = getParameter(name)

    def setEnabled(self, enabled):
        if(type(enabled) != bool):
            raise Exception("Value 'enabled' must be a boolean.")
        self.value["isEnabled"] = enabled
        return self

    def setFailureMode(self, failureMode):
        if(type(failureMode) != FailureMode):
            raise Exception("Value 'enabled' must be a FailureMode.")
        self.value["failureMode"] = failureMode.value
        return self

    def setRate(self, rate):
        if((type(rate) != float and type(rate) != int) or rate < 0 or rate > 1):
            raise Exception("Value 'rate' must be a float between 0 and 1.")
        self.value["rate"] = rate
        return self

    def setMinLatency(self, latency):
        if(type(latency) != int or latency < 0):
            raise Exception("Value 'minLatency' must be an integer greater than 0.")
        self.value["minLatency"] = latency
        return self

    def setMaxLatency(self, latency):
        if(type(latency) != int or latency < 0):
            raise Exception("Value 'maxLatency' must be an integer greater than 0.")
        self.value["maxLatency"] = latency
        return self

    def setExceptionMessage(self, message):
        if(type(message) != str):
            raise Exception("Value 'exceptionMsg' must be a string.")
        self.value["exceptionMsg"] = message
        return self

    def setStatusCode(self, code):
        if(type(code) != int or code < 0):
            raise Exception("Value 'statusCode' must be an integer greater than 0.")
        self.value["statusCode"] = code
        return self

    def setDiskSpace(self, diskSpace):
        if(type(diskSpace) != int or diskSpace < 0):
            raise Exception("Value 'diskSpace' must be an integer greater than 0.")
        self.value["diskSpace"] = diskSpace
        return self

    def setDenylist(self, denylist):
        if(type(denylist) != list):
            raise Exception("Value 'denylist' must be an integer greater than 0.")
        self.value["denylist"] = denylist
        return self
    
    def getValue(self):
        return self.value

    def save(self):
        updateParameter(self.name, self.value)

def getAllParameters():
    next_token = ' '
    resources = []
    while next_token is not None:
        ssm_details = ssm.describe_parameters(MaxResults=50, NextToken=next_token)
        results = ssm_details['Parameters']
        current_batch = [result for result in results]
        next_token = ssm_details.get('NextToken', None)
        resources += current_batch
    
    return list(filter(lambda param: param["Name"].startswith(PARAMETER_PREFIX), resources))

def getParameter(name):
    parameter = ssm.get_parameter(Name=name)
    return json.loads(parameter["Parameter"]["Value"])

def updateParameter(name, value):
    return ssm.put_parameter(
        Name=name,
        Overwrite=True,
        Value=json.dumps(value),
    )

def disableAllParameters():
    for parameter in getAllParameters():
        name = parameter["Name"]
        parameterInstance = Parameter(name)
        parameterInstance.setEnabled(False).save()