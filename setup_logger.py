import logging

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(
    filename='data_requests.Log', 
    level=logging.DEBUG,
    format=LOG_FORMAT
)

logger = logging.getLogger()
