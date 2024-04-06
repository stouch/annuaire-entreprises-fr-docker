from dotenv import load_dotenv
import sys
load_dotenv(override=True)

import logging
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

from dag_datalake_sirene import import_data 

