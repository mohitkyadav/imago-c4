import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logging_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(logging_format)
logger.addHandler(handler)

LOG = logger
