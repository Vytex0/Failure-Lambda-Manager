import logging
from utils.config import DEBUG_MODE 

logging.basicConfig(format='[%(asctime)s] - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.getLogger().setLevel(logging.INFO)

def log(type, message):
    if(not(DEBUG_MODE)):
        return
    type = type.lower()
    if(type == "debug"):
        logging.debug(message)
    elif(type == "warning"):
        logging.warning(message)
    elif(type == "error"):
        logging.error(message)
    elif(type == "critical"):
        logging.critical(message)
    else:
        logging.info(message)