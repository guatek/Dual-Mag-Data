import os
import sys 
import glob
import time
import shutil
import tarfile
import configparser
from loguru import logger

sys.path.append('..')
from libs.raw_image import RawImage
from libs.log_parser import DualMagLog
from multiprocessing.pool import ThreadPool
from libs.rois import ROI

roi_paths = ['low_mag_cam_rois','high_mag_cam_rois']
video_paths = ['low_mag_cam_video', 'high_mag_cam_video']

def threaded_video_proc(raw_image):
    raw_image.export_as_tiff()
    raw_image.export_8bit_jpegs()
    
def threaded_roi_proc(roi):
    roi.process(save_to_disk=True)


if __name__=="__main__":

    logger.remove()
    logger.add(sys.stderr, level="INFO")

    with logger.catch():

        if len(sys.argv) != 2:
            logger.fatal("Please enter data directory as the first argument")

        # Load config file
        config = configparser.ConfigParser()
        config.read("..\\config\\settings.ini")

        # Check to make sure paths are okay
        dl = os.listdir(sys.argv[1])
        for roi_path in roi_paths:
            if not roi_path in dl:
                logger.error("Could not find: " + roi_path)
                exit(1)
        for video_path in video_paths:
            if not video_path in dl:
                logger.error("Could not find: " + video_path)
                exit(1)
        
        log_file = glob.glob(os.path.join(sys.argv[1], '*.log'))
        if len(log_file) != 1:
            logger.error("Missing or multiple log files")
            exit(1)
        else:
            log_file = log_file[0]

        try:

            # create output directory and populate
            output_dir = os.path.join(sys.argv[1],'proccesed')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            else:
                shutil.rmtree(output_dir)
                os.makedirs(output_dir)

        except IOError as e:
            logger.error(e)
            exit(1)

        # Process and export log file
        dml = DualMagLog(log_file)
        dml.parse_lines()
        dml.export(os.path.join(output_dir, os.path.basename(log_file)[:-4] + '.csv'))

        # Process video files 
        for vid_path in video_paths:
            # create output path is needed
            output_path = os.path.join(output_dir, vid_path)
            logger.info(output_path)
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            vids = sorted(glob.glob(os.path.join(sys.argv[1], vid_path, '*.bin')))
            raw_videos = []
            for vid in vids:
                raw_videos.append(RawImage(vid, output_path))
            with ThreadPool(processes=6) as p:
                result = p.map(threaded_video_proc, raw_videos)

        # Process ROIs
        for roi_path in roi_paths:
            # create output path is needed
            output_path = os.path.join(output_dir, roi_path)
            
            logger.info(output_path)
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            # loop over tars, untar and then process subdirs
            archs = sorted(glob.glob(os.path.join(sys.argv[1], roi_path, '*.tar')))

            for arch in archs:
                roi_per_sec_timer = time.time()
                logger.info('Processing tar archive: ' + arch)
                extracted_path = arch + ".unpacked"
                if not os.path.exists(extracted_path):
                    os.makedirs(extracted_path)
                with tarfile.open(arch) as archive:
                    for member in archive.getmembers():
                        if member.isreg():  # skip if the TarInfo is not files
                            member.name = os.path.basename(member.name) # remove the path by reset it
                            archive.extract(member,extracted_path) # extract

                rois = sorted(glob.glob(os.path.join(extracted_path, '*.tif')))
                raw_rois = []
                for roi in rois:
                    roi_filename = os.path.basename(roi)
                    roi_filepath = os.path.dirname(roi)

                    # create output dir if needed
                    roi_timestamp = str(int(int(roi_filename.split('-')[1])/1000000/120))
                    roi_output_dir = os.path.join(output_path, roi_timestamp)
                    if not os.path.exists(roi_output_dir):
                        os.makedirs(roi_output_dir)

                    raw_rois.append(ROI(roi_filepath, roi_filename, roi_output_dir, cfg=config))

                with ThreadPool(processes=24) as p:
                    result = p.map(threaded_roi_proc, raw_rois)

                # remove the extracted dir
                shutil.rmtree(extracted_path)
                logger.info('ROIs per second: ' + str(len(rois)/(time.time()-roi_per_sec_timer)))