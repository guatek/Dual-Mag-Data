import sys 
from loguru import logger

sys.path.append('..')
from libs.raw_image import RawImage


if __name__=="__main__":

    logger.remove()
    logger.add(sys.stderr, level="INFO")

    with logger.catch():

        ri = RawImage('..\\resources\\2019-11-06-17-02-31.219660232.bin')
        ri.export_as_tiff()