from utils.logger import log
from objects.parameter import disableAllParameters

class Test():
    def __init__(self, name, failures):
        self.name = name
        self.failures = failures

    def getName(self):
        return self.name

    def run(self):
        log("info", f"Praparing test {self.name}.")
        log("info", f"Reseting all previous parameters.")
        disableAllParameters()
        for failure in self.failures:
            failure.run()
        log("info", f"Test {self.name} launched.")

    def stop(self):
        log("info", f"Stopping test {self.name}.")
        for failure in self.failures:
            failure.stop()
        log("info", f"Test {self.name} stopped.")