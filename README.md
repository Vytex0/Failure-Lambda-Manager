
# 🧨 Failure Lambda Manager 

This purpose of this project is to provide a simple tool to use the "failure-lambda" library for chaos engineering tests on NodeJS lambda functions.




## 📝 Preparing and deploying failure-lambda

You need to install and deploy failure-lambda into all your AWS lambda functions.

### Create the failure-lambda layer

First, go to the AWS lambda page. In the side-bar, click on "Layers" and then "Create layer". For the layer name, you can fill "failure-lambda", check all compatible architectures and upload a zip which contains the library installed into a folder named "nodejs". [An example is provided in the repository](./failure-lambda-layer.zip).

### Preparing all your lambda functions

Then, for each lambda function that you want to test: 

Go into its configuration page. At the bottom of the page, click on "Add a layer", "Custom layers" and choose your previously added layer.

You can now edit your function code to add these both lines at the beginning:
```javascript
const failureLambda = require('failure-lambda')
process.env['FAILURE_INJECTION_PARAM'] = "failure-lambda-[REPLACE_BY_THE_NAME_OF_YOUR_FUNCTION]"; // ex : failure-lambda-test
```
You also need to wrap the function of your "event.handler":
```javascript
// Example of handler function
exports.handler = failureLambda(async (event, context) => {
    return event.key1;
});
```

The library is now configured, now you need to create the corresponding parameter and give to your function the access to this parameter.

For creating the parameter, go into the parameter store page from the AWS console (subpage of AWS Systems Manager). Here, click on "Create parameter", give the same name as you chose in your function, check standard tier and string type, select text data type and fill the value with :
```
{"isEnabled": false, "failureMode": "latency", "rate": 1, "minLatency": 100, "maxLatency": 400, "exceptionMsg": "Exception message!", "statusCode": 404, "diskSpace": 100, "denylist": ["s3.*.amazonaws.com", "dynamodb.*.amazonaws.com"]}
```

Finally, you need to give to your lambda function the access to read the parameter. Go back to your function page, click on Configuration -> Permissions, and click on the "Role name". On this new page, click on Add permissions -> Attach policies, select "AmazonSSMReadOnlyAccess" and confirm. For security purposes, it would be better to create a policy giving only access to your parameter and not the others.

Your lambda function is now ready to be tested by chaos-engineering. You can repeat all the steps for all your functions.
## 💻 Prepare and use Failure Lambda Manager (FLM)

If you only want to do basic testing, you could manually change testing parameters directly into the parameter store or by AWS CLI. However, this method does not really scale well for large tests. This is the reason why Failure Lambda Manager has been developped to add a second layer for automating your chaos engineering tests.

### Create an IAM role for FLM

Failure Lambda Manager is operating through a local python script. Thus, you have to give it read and update access to your parameters for working.

From the AWS Console, go to the IAM page. There, click on "Users" -> "Add Users". Choose a name for your user, and click next. Select "Attach policies directly" and add the policy "AmazonSSMFullAccess". For security purposes, it would be better to create a more precise policy. Click "Next" and finally "Create User". Once your new user is created, click on it and click on the "Security credentials" tab. Scroll to "Access keys" and click on "Create access key". Select "Other" and click "Next", give the description you want and create the access key. You now have access to the "Access key" and the "Secret access key".

On your computer, once you have cloned the repository, navigate inside with your terminal. You need to create a virtual environment and add some environment variables:
```bash
python -m venv venv
source venv/bin/activate
export FLM_REGION_NAME="YOU AWS REGION, EX: us-east-1"
export FLM_AWS_ACCESS_KEY_ID="YOUR USER ACCES KEY"
export FLM_AWS_SECRET_ACCESS_KEY="YOU USER SECRET ACCESS KEY"
```


### Configuring FLM

Failure Lambda Manager has two parameters that you can modify as you need. These parameters can be found in utils/config.py
```
DEBUG_MODE: True if you want debug printing and False otherwise, default: True
PARAMETER_PREFIX: The prefix of you parameters, default: "lambda-failure"
```


### Running FLM

#### Prepare your first FLM test campaign

In the folder 'tests', you can set up your own tests for your chaos engineering campaign. You will find [an example of a test file which is self-explanatory](./tests/example1.py).

A test file is responsible for defining and orchastrating your test campaign. Inside of a test object, you will define your failures. A failure is a specific collapse on a defined function with a defined failure mode and its parameters: latency, exception, denylist, ... All the needed documentation is available at the end of this README file.

### Run your test campaign

You can now run your test campaign from the flm python file. Here are the possible parameters:

```bash
--disableallparameters # Disable all failures in parameters to be sure that your app is functionning in its normal mode (automatically done after the end of a test)
--run TEST_FILE # Run your test campaign

# Example: python flm.py --run example1
```
## 📜 Documentation

### FailureMode enum

```
FailureMode():
    LATENCY
    EXCEPTION
    DENYLIST
    DISKSPACE
    STATUSCODE
```


### Parameter class and external functions

```
Parameter():
    __init__(name: str):
        self.name: str
        self.value: dict
    setEnabled(enabled: boolean)
    setFailureMode(failureMode: FailureMode)
    setRate(rate: float)
    setMinLatency(latency: int)
    setMaxLatency(latency: int)
    setExceptionMessage(message: str)
    setStatusCode(code: int)
    setDiskSpace(diskSpace: int)
    setDenylist(denylist: list)
    getValue()
    save()

getAllParameters() -> list of parameter value (dict)
getParameter(name: str) -> parameter value (dict)
updateParameter(name: str, value: dict)
disableAllParameters()
```

### Failure class

```
Failure():
    __init__(functionName: str, failureMode: FailureMode, rate: float, minLatency: int = None, maxLatency : int = None, exceptionMsg : str = None, statusCode : int = None, diskSpace : int = None, denylist : list = None):
        self.parameter: Parameter
        self.functionName: str
        self.failureMode: FailureMode
        self.rate: float
        self.minLatency: int
        self.maxLatency: int
        self.exceptionMsg: str
        self.statusCode: int
        self.diskSpace: int
        self.denylist: list
    run()
    stop()
```

### Test class

```
Test():
    __init__(name: str, failures: list)
        self.name: str
        self.functionName: str
        self.failureMode: FailureMode
        self.rate: float
        self.minLatency: int
        self.maxLatency: int
        self.exceptionMsg: str
        self.statusCode: int
        self.diskSpace: int
        self.denylist: list
    getName() -> str
    run()
    stop()
```


## 👨‍💻 Authors

- [Vincent Gobbi @Vytex0](https://github.com/Vytex0)


## Related

[Failure Lambda](https://github.com/gunnargrosch/failure-lambda)
