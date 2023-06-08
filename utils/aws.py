import os
import boto3
import logging
from utils.config import PARAMETER_PREFIX

REGION_NAME = os.getenv("FLM_REGION_NAME")
AWS_ACCESS_KEY_ID = os.getenv("FLM_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("FLM_AWS_SECRET_ACCESS_KEY")

if(REGION_NAME is None or AWS_ACCESS_KEY_ID is None or AWS_SECRET_ACCESS_KEY is None):
    logging.error("Please define FLM_REGION_NAME, FLM_AWS_ACCESS_KEY_ID and FLM_AWS_SECRET_ACCESS_KEY in your environnement variables.")
    exit(0)

ssm = boto3.client('ssm', 
    region_name=REGION_NAME, 
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    verify=True)