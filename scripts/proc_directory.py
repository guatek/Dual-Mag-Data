import os
import sys 
import glob
import time
import shutil
import tarfile
import cProfile
import pystache
import datetime
import numpy as np
import configparser
from loguru import logger

sys.path.append('..')
from libs.raw_image import RawImage
from libs.log_parser import DualMagLog
from multiprocessing.pool import ThreadPool, Pool
from multiprocessing import Process, Queue, cpu_count
from libs.rois import ROI

roi_paths = ['low_mag_cam_rois','high_mag_cam_rois']
video_paths = ['low_mag_cam_video', 'high_mag_cam_video']

output_path = ''

def threaded_video_proc(raw_image):
    raw_image.export_as_tiff(flat_field=False)
    raw_image.export_8bit_jpegs(thumbnails=True, flat_field=False, gamma=0.5)
    return raw_image
    
def threaded_roi_proc(roi):
    roi.process(save_to_disk=True)
    return roi

def process_bundle_list(bundle_queue,output_queue):

    while True:
        try:
            output_queue.put(threaded_subdir_proc(bundle_queue.get()))
        except:
            time.sleep(0.04*np.random.rand())

def threaded_subdir_proc(subdir_pack):

    extracted_path = None

    proc_time = time.time()

    subdir = subdir_pack['subdir']
    output_path = subdir_pack['output_path']
    config = subdir_pack['config']

    if subdir[-3:] == 'tar':
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

    all_rois = []
    
    # Process then save
    for i in range(0,len(raw_rois)):
        raw_rois[i].process(save_to_disk=False)

    for i in range(0,len(raw_rois)):
        all_rois.append(raw_rois[i].get_item())
        raw_rois[i].save_to_disk()

    # remove the extracted dir
    if extracted_path is not None and os.path.exists(extracted_path):
        shutil.rmtree(extracted_path)

    logger.info('Processed : ' + subdir + ' @ ' + str(len(all_rois)/(time.time() - proc_time + 1)) + ' roi/s')

    return all_rois

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

        pr = cProfile.Profile()
        pr.enable()

        start_time = time.time()

        tar_increment = [1,1]

        if len(sys.argv) < 2:
            logger.exception("Please enter data directory as the first argument")
            exit(1)

        if len(sys.argv) == 4:
            try:
                tar_increment[0] = int(sys.argv[2])
                tar_increment[1] = int(sys.argv[3])
                logger.info('Will process every ' + str(tar_increment[0]) + ' low_mag tar archive')
                logger.info('Will process every ' + str(tar_increment[1]) + ' high_mag tar archive')
            except:
                logger.exception('Could not parse tar increments, please enter for example: 10 10 to process every 10th archive')
                exit(1)

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
            output_dir = os.path.join(sys.argv[1],'processed-'+os.path.basename(sys.argv[1]))
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            else:
                pass
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

            with Pool(processes=6) as p:
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
        index = 0
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

            # select only a subset with tar_increment
            subdirs = subdirs[0::tar_increment[index]]

            subdir_packs = []
            #bundle_queue = Queue()
            for subdir in subdirs:
                subdir_pack = {}
                subdir_pack['subdir'] = subdir
                subdir_pack['output_path'] = output_path
                subdir_pack['config'] = config
                #bundle_queue.put(subdir_pack)
                subdir_packs.append(subdir_pack)

            roi_per_sec_timer = time.time()

            n_threads = cpu_count() - 1
            if n_threads < 1:
                n_threads = 1

            # output_queue = Queue()
            # processes = []
            # for i in range(0,n_threads):
            #     p = Process(target=process_bundle_list, args=(bundle_queue,output_queue))
            #     p.start()
            #     processes.append(p)

            # counter = 0

            # all_rois = []
            # while True:

            #     if counter >= len(subdirs):
            #         break

            #     try:
            #         output = output_queue.get(block=True,timeout=10)
            #         if output:
            #             all_rois += output
            #             counter += 1                
            #     except:
            #         logger.info("Queue empty")

            #     time.sleep(1.0)

            #     # Terminate the processes in case they are stuck
            # for p in processes:
            #     p.terminate()

            with Pool(processes=n_threads) as p:
                all_subdirs = p.map(threaded_subdir_proc, subdir_packs)

            all_rois = []
            for subdir in all_subdirs:
                all_rois += subdir

            logger.info('ROIs per second: ' + str(len(all_rois)/(time.time()-roi_per_sec_timer + 1)))

            # Save the total number of ROIs processed
            total_rois.append(len(all_rois))

            context = {}
            context['image_items'] = all_rois
            context['database_name'] = roi_path
            render_template('roi-grid.stache', context, output_dir)

            index += 1

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

        pr.disable()
        pr.dump_stats("profile_result.txt")