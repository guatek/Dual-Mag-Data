import sys 
import configparser
from loguru import logger

sys.path.append('..')
from libs.rois import ROI


if __name__=="__main__":

    logger.remove()
    logger.add(sys.stderr, level="INFO")

    with logger.catch():

        config = configparser.ConfigParser()
        config.read("..\\config\\settings.ini")

        filename = 'low_mag_cam-1573061176528793-1555336490760-30908-005-1282-608-68-68.tif'
        filepath = '..\\resources\\'
        roi = ROI(filepath, filename, output_path)
        roi.process(save_to_disk=True, abs_path=filepath, file_prefix=filename.split('.')[0], cfg=config)