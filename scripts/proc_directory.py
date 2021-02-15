import os
import sys 
import glob
import time
import shutil
import tarfile
import pystache
import datetime
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
    raw_image.export_as_tiff(flat_field=False)
    raw_image.export_8bit_jpegs(thumbnails=True, flat_field=False, gamma=0.5)
    return raw_image
    
def threaded_roi_proc(roi):
    roi.process(save_to_disk=True)
    return roi

def render_template(template_name, context, webapp_output):

    template = ""
    with open(os.path.join('..','templates','js',template_name),"r") as fconv:
        template = fconv.read()

    # render the javascript page and save to disk
    page = pystache.render(template,context)

    if not os.path.exists(webapp_output):
        os.makedirs(webapp_output)

    with open(os.path.join(webapp_output,context['database_name']+'.js'),"w") as fconv:
        fconv.write(page)

def summary_item(name, value):
    return {"name": name, "value": value}

if __name__=="__main__":

    logger.remove()
    logger.add(sys.stderr, level="INFO")

    with logger.catch():

        start_time = time.time()

        if len(sys.argv) != 2:
            logger.fatal("Please enter data directory as the first argument")

        # Load config file
        config = configparser.ConfigParser()
        config.read("..\\config\\settings.ini")

        # Check to make sure paths are okay
        dl = os.listdir(sys.argv[1])
        for roi_path in roi_paths:
            if not roi_path in dl:
                logger.warning("Could not find: " + roi_path)
        for video_path in video_paths:
            if not video_path in dl:
                logger.warning("Could not find: " + video_path)
        
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
                time.sleep(2)
                os.makedirs(output_dir)

        except IOError as e:
            logger.error(e)
            exit(1)

        # setup the webapp output
        webapp_dir = 'webapp'

        # copy over the base app 
        shutil.copytree(os.path.abspath(os.path.join('..', webapp_dir)),os.path.join(output_dir,webapp_dir))

        # # Process and export log file
        dml = DualMagLog(log_file)
        dml.parse_lines()
        dml.export(os.path.join(output_dir, os.path.basename(log_file)[:-4] + '.csv'))

        # start populating the summary array
        summary_items = []
        summary_items.append(summary_item("App Creation DateTime", datetime.datetime.now().isoformat()))
        summary_items.append(summary_item("Data Collection DateTime", dml.log_start_time))

        # set output to webapp dir for all remaing files
        output_dir = os.path.join(output_dir,webapp_dir)

        # # Process video files
        total_vids = [] 
        for vid_path in video_paths:

            if not os.path.exists(os.path.join(sys.argv[1], vid_path)):
                continue

            # create output path is needed
            output_path = os.path.join(output_dir, vid_path)
            logger.info(output_path)
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            vids = sorted(glob.glob(os.path.join(sys.argv[1], vid_path, '*.bin')))
            raw_videos = []
            for vid in vids:
                tmp = RawImage(vid, output_path)
                if tmp.file_valid:
                    raw_videos.append(tmp)
                else:
                    logger.warning("File: " + vid + " is bad, skipping.")

            with ThreadPool(processes=6) as p:
                result = p.map(threaded_video_proc, raw_videos)

            # Create image-grid
            video_frames = []
            for r in raw_videos:
                for item in r.image_items:
                    video_frames.append(item)
            
            total_vids.append(len(video_frames))

            # render the output for webapp
            context = {}
            context['image_items'] = video_frames
            context['database_name'] = vid_path
            render_template('image-grid.stache', context, output_dir)

        # Process ROIs
        total_rois = []
        for roi_path in roi_paths:

            if not os.path.exists(os.path.join(sys.argv[1], roi_path)):
                continue

            all_rois = []

            # create output path is needed
            output_path = os.path.join(output_dir, roi_path)
            
            logger.info(output_path)
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            # loop over tars, untar and then process subdirs
            subdirs = sorted(glob.glob(os.path.join(sys.argv[1], roi_path, '*')))

            extracted_path = None

            for subdir in subdirs:
            
                roi_per_sec_timer = time.time()
            
                if subdir[-3:] == 'tar':
                    logger.info('Processing tar archive: ' + subdir)
                    extracted_path = subdir + ".unpacked"
                    if not os.path.exists(extracted_path):
                        os.makedirs(extracted_path)
                    with tarfile.open(subdir) as archive:
                        for member in archive.getmembers():
                            if member.isreg():  # skip if the TarInfo is not files
                                member.name = os.path.basename(member.name) # remove the path by reset it
                                archive.extract(member,extracted_path) # extract

                    rois = sorted(glob.glob(os.path.join(extracted_path, '*.tif')))
                else:
                    rois = sorted(glob.glob(os.path.join(subdir, '*.tif')))

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
                    results = p.map(threaded_roi_proc, raw_rois)

                for roi in results:
                    all_rois.append(roi.get_item())

                # remove the extracted dir
                if extracted_path is not None and os.path.exists(extracted_path):
                    shutil.rmtree(extracted_path)

                logger.info('ROIs per second: ' + str(len(rois)/(time.time()-roi_per_sec_timer)))

            # Save the total number of ROIs processed
            total_rois.append(len(all_rois))

            template = ""
            with open(os.path.join('..','templates','js','image-grid.stache'),"r") as fconv:
                template = fconv.read()

            context = {}
            context['image_items'] = all_rois
            context['database_name'] = roi_path
            render_template('image-grid.stache', context, output_dir)

        # finalize the data summary
        names = ['Low Mag', 'High Mag']
        for i in range(0,len(total_rois)):
            summary_items.append(summary_item("Total " + names[i] + " ROIs", total_rois[i]))
        for i in range(0,len(total_vids)):
            summary_items.append(summary_item("Total " + names[i] + " Saved Images", total_vids[i]))

        summary_items.append(summary_item("Data Processing Time (s)", time.time() - start_time))
        summary_items.append(summary_item("Log file csv export path", os.path.join(output_dir, os.path.basename(log_file)[:-4] + '.csv').replace("\\","/")))

        context = {}
        context['database_name'] = 'dual_mag_summary'
        context['summary_items'] = summary_items
        render_template('summary.stache', context, output_dir)