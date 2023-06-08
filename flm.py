import typer
from objects.parameter import disableAllParameters as disableAllParams
import os
from utils.logger import log

TESTS_DIR = "tests"

def main(run: str = None, disableAllParameters: bool = False):
   if(disableAllParameters):
      log("INFO", f"Disabling all parameters.")
      disableAllParams()
      log("INFO", f"All parameters have been successfully disabled.")
   
   if(run is not None):
      if(os.path.exists("./"+TESTS_DIR+"/"+run+".py")):
         log("INFO", f"Importing test '{run}'.")
         __import__(f"{TESTS_DIR}.{run}")
      else:
         log("ERROR", f"Test '{run}' does not exist in folder '{TESTS_DIR}'.")

if __name__ == "__main__":
   typer.run(main)