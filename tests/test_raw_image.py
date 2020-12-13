import sys 
from loguru import logger
sys.path.append('..')

from libs.raw_image import RawImage

logger.remove()
logger.add(sys.stderr, level="INFO")
ri = RawImage('..\\resources\\2019-11-06-17-02-31.219660232.bin')
ri.export_as_tiff()