import sys 
import configparser
from loguru import logger


if __name__=="__main__":

    logger.remove()
    logger.add(sys.stderr, level="INFO")

    with logger.catch():
        config = configparser.ConfigParser()
        config.read("..\\config\\settings.ini")
        try:
            for s in config['rois']:
                logger.info(s + " = " + config['rois'].get(s))
        except Exception as e:
            logger.error(e)

