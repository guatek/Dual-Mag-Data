# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
import datetime

from math import pi
from loguru import logger
from scipy import ndimage, spatial
from skimage import transform
from skimage import morphology, measure, exposure, restoration
from skimage.feature import register_translation
from skimage.filters import threshold_otsu, scharr, gaussian

__author__ = "Paul Roberts"
__copyright__ = "Copyright 2020 Guatek"
__credits__ = ["Guatek"]
__license__ = "MIT"
__maintainer__ = "Paul Roberts"
__email__ = "proberts@guatek.com"
__doc__ = '''

Handle loading, converting and storing ROIs, borrows heavily from:
https://github.com/planktivore/SPCConvert/blob/master/cvtools.py

@author: __author__
@status: __status__
@license: __license__
'''

def make_gaussian(size, fwhm = 3, center=None):
    """Make a square gaussian kernel.
    size is the length of a side of the square
    fwhm is full-width-half-maximum, which
    can be thought of as an effective radius.

    Args:
        size (tuple): Shape of the kernel
        fwhm (int, optional): Width of the kernel. Defaults to 3.
        center (tuple, optional): Offset from center. Defaults to None.

    Returns:
        [type]: [description]
    """

    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]

    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]

    output = np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2)
    output = output/np.sum(output)

    return output


def import_image(abs_path, filename, raw=True, bayer_pattern=cv2.COLOR_BAYER_RG2RGB):
    """Read image and convert color if requested

    Args:
        abs_path (string): absolute path to the file
        filename (string): Name of the image file
        raw (bool, optional): If the image is "raw" bayer pattern. Defaults to True.
        bayer_pattern (cv2.COLOR_*, optional): Bayer pattern spec. Defaults to cv2.COLOR_BAYER_RG2RGB.

    Returns:
        ndarray: the resulting image
    """
    img_c = cv2.imread(os.path.join(abs_path,filename),cv2.IMREAD_UNCHANGED)
    if raw:
        img_c = cv2.cvtColor(img_c,bayer_pattern)

    return img_c

def convert_to_8bit(img, auto_scale=True):
    """Convert image to 8-bits with scaling

    Args:
        img (ndarray): the image to convert
        auto_scale (bool, optional): Auto-scale the image. Defaults to True.

    Returns:
        ndarray: The image converted to 8-bits
    """
    if auto_scale:
        result = np.float32(img)-np.min(img)
        result[result<0.0] = 0.0
        if np.max(img) != 0:
            result = result/np.max(img)

        img_8bit = np.uint8(255*result)
    else:
        img_8bit = np.unit8(img)

    return img_8bit

def intensity_features(img, obj_mask):
    res = {}

    # assume that obj_mask contains one connected component
    prop = measure.regionprops(obj_mask.astype(np.uint8), img)[0]
    res["mean_intensity"] = prop.mean_intensity

    intensities = prop.intensity_image[prop.image]
    res["median_intensity"] = np.median(intensities)
    res["std_intensity"] = np.std(intensities)
    res["perc_25_intensity"] = np.percentile(intensities, 25)
    res["perc_75_intensity"] = np.percentile(intensities, 75)

    centroid = np.array(prop.centroid)
    weighted_centroid = np.array(prop.weighted_centroid)
    displacement = weighted_centroid - centroid
    displacement_image = np.linalg.norm(displacement / img.shape)
    if prop.minor_axis_length > 0:
        displacement_minors = np.linalg.norm(displacement) / prop.minor_axis_length
    else:
        displacement_minors = np.linalg.norm(displacement)
    res['mass_displace_in_images'] = displacement_image
    res['mass_displace_in_minors'] = displacement_minors

    res["moment_hu_1"] = prop.weighted_moments_hu[0]
    res["moment_hu_2"] = prop.weighted_moments_hu[1]
    res["moment_hu_3"] = prop.weighted_moments_hu[2]
    res["moment_hu_4"] = prop.weighted_moments_hu[3]
    res["moment_hu_5"] = prop.weighted_moments_hu[4]
    res["moment_hu_6"] = prop.weighted_moments_hu[5]
    res["moment_hu_7"] = prop.weighted_moments_hu[6]

    return res


class ROI:
    """Region Of Interest handler for loading, converting and storing
    """
    def __init__(self, filepath, filename, output_path=None, bayer_pattern=cv2.COLOR_BAYER_RG2RGB, is_flipped=False, cfg=None):
        """Instantiate an ROI object

        Args:
            filepath (string): aboslute path to the location of the file
            filename (string): name of the file
            output_path (string): absolute path to output directory
            bayer_pattern (cv2.COLOR_*, optional): Color convertion type. Defaults to cv2.COLOR_BAYER_RG2RGB.
            is_flipped (bool, optional): when true, flip the image up-down. Defaults to False.
            cfg (configparser, optional): loaded configparser object or None
        """
        try:
            self.basepath = filepath
            self.filename = filename

            self.timestamp = datetime.datetime.fromtimestamp(float(self.filename.split('-')[1])/1000000)
            self.timestring = self.timestamp.isoformat()

            self.output_path = output_path
            self.is_flipped = is_flipped
            self.img = import_image(self.basepath, self.filename, bayer_pattern is not None, bayer_pattern)
            if self.is_flipped:
                self.img = np.flipud(self.img)
            self.img_8bit = convert_to_8bit(self.img)
            self.loaded = True
            self.cfg = cfg
            self.url = ''
            self.features = {}
        except IOError as e:
            self.loaded = False
            logger.error(e)

    def get_item(self):
        """Returns a simplified representation of the ROI for web apps

        Returns:
            dict: roi item with fields
        """

        output = {}

        if 'area' in self.features:
            output['image_id'] = self.filename[:-4]
            output['area'] = self.features['area']
            output['maj_axis_len'] = self.features['major_axis_length']
            output['min_axis_len'] = self.features['minor_axis_length']
            output['aspect_ratio'] = self.features['aspect_ratio']
            output['orientation'] = self.features['orientation']
            output['clipped_fraction'] = self.features['clipped_fraction']
            output['timestamp'] = self.filename.split('-')[1]
            output['timestring'] = self.timestring
            output['thumbnailWidth'] = self.img.shape[1]
            output['thumbnailHeight'] = self.img.shape[0]
            output['fullWidth'] = self.img.shape[1]
            output['fullHeight'] = self.img.shape[0]
            output['src'] = self.url + '.jpeg'
            output['thumbnail'] = self.url + '.jpeg'
        
        return output


    def process(self, save_to_disk=False, abs_path='', file_prefix=''):
        """Process roi and extract features

        Args:
            save_to_disk (bool, optional): Save the results to disk. Defaults to False.
            abs_path (str, optional): absolute path to location to save to. Defaults to ''.
            file_prefix (str, optional): roi file prefix. Defaults to ''.
            cfg (configparser, optional): loaded configparser object. Defaults to None.

        Returns:
            [dict]: all features and images
        """

        # set the file path
        if file_prefix == '':
            file_prefix = self.filename[:-4]

        # set the output path
        if abs_path == '' and self.output_path is not None:
            abs_path = self.output_path
        
        # store the url
        subdir = os.path.basename(os.path.normpath(abs_path))
        basedir = os.path.basename(os.path.normpath(os.path.dirname(os.path.normpath(abs_path))))
        self.url = basedir + '/' + subdir + '/' + file_prefix

        # get a reference to 8bit version of the image
        img = self.img_8bit

        # Pull out some settings from cfg if available
        if self.cfg:
            min_obj_area = self.cfg['rois'].getint("min_obj_area",100)
            objs_per_roi = self.cfg['rois'].getint("objs_per_roi",1)
            deconv = self.cfg['rois'].getboolean("deconv",False)
            edge_thresh = self.cfg['rois'].getfloat("edge_threshold",2.5)
            use_jpeg = self.cfg['rois'].getboolean("use_jpeg",False)
            raw_color = self.cfg['rois'].getboolean("raw_color",False)
        else:
            min_obj_area = 100
            objs_per_roi = 1
            deconv = False
            use_jpeg = False
            raw_color = True
            edge_thresh = 2.5

        # Define an empty dictionary to hold all features
        features = {}

        features['rawcolor'] = np.copy(img)
        gray = np.uint8(np.mean(img,2))

        # edge-based segmentation
        edges_mag = scharr(gray)
        edges_med = np.median(edges_mag)
        edges_thresh = edge_thresh*edges_med
        edges = edges_mag >= edges_thresh
        edges = morphology.closing(edges,morphology.square(3))
        filled_edges = ndimage.binary_fill_holes(edges)
        edges = morphology.erosion(filled_edges,morphology.square(3))

        # Store the edge image
        bw_img = edges

        # Compute morphological descriptors
        label_img = morphology.label(bw_img,connectivity=2,background=0)
        props = measure.regionprops(label_img,gray)

        # clear bw_img
        bw_img = 0*bw_img

        # sort the region props
        props = sorted(props, reverse=True, key=lambda k: k.area)

        if len(props) > 0:

            # Init mask with the largest area object in the roi
            bw_img = (label_img)== props[0].label
            bw_img_all = bw_img.copy()

            base_area = props[0].area

            # use only the features from the object with the largest area
            max_area = 0
            max_area_ind = 0
            avg_area = 0.0
            avg_maj = 0.0
            avg_min = 0.0
            avg_or = 0.0
            avg_count = 0

            if len(props) > objs_per_roi:
                n_objs = objs_per_roi
            else:
                n_objs = len(props)

            for f in range(0,n_objs):

                if props[f].area > min_obj_area:
                    bw_img_all = bw_img_all + ((label_img)== props[f].label)
                    avg_count = avg_count + 1

                if f >= objs_per_roi:
                    break

            # Take the largest object area as the roi area
            # no average
            avg_area = props[0].area
            avg_maj = props[0].major_axis_length
            avg_min = props[0].minor_axis_length
            avg_or = props[0].orientation
            avg_eccentricity = props[0].eccentricity
            avg_solidity = props[0].solidity

            # Calculate intensity features only for largest
            features_intensity = intensity_features(gray, bw_img)
            features['intensity_gray'] = features_intensity

            features_intensity = intensity_features(img[::, ::, 0], bw_img)
            features['intensity_red'] = features_intensity

            features_intensity = intensity_features(img[::, ::, 1], bw_img)
            features['intensity_green'] = features_intensity

            features_intensity = intensity_features(img[::, ::, 2], bw_img)
            features['intensity_blue'] = features_intensity

            # Check for clipped image
            if np.max(bw_img_all) == 0:
                bw = bw_img_all
            else:
                bw = bw_img_all/np.max(bw_img_all)

            clip_frac = float(np.sum(bw[:,1]) +
                    np.sum(bw[:,-2]) +
                    np.sum(bw[1,:]) +
                    np.sum(bw[-2,:]))/(2*bw.shape[0]+2*bw.shape[1])
            features['clipped_fraction'] = clip_frac

            # Save simple features of the object
            features['area'] = avg_area
            features['minor_axis_length'] = avg_min
            features['major_axis_length'] = avg_maj
            if avg_maj == 0:
                features['aspect_ratio'] = 1
            else:
                features['aspect_ratio'] = avg_min/avg_maj
            features['orientation'] = avg_or
            features['eccentricity'] = avg_eccentricity
            features['solidity'] = avg_solidity
            features['estimated_volume'] = 4.0 / 3 * pi * avg_maj * avg_min * avg_min

        else:

            features['clipped_fraction'] = 0.0

            # Save simple features of the object
            features['area'] = 0.0
            features['minor_axis_length'] = 0.0
            features['major_axis_length'] = 0.0
            features['aspect_ratio'] = 1
            features['orientation'] = 0.0
            features['eccentricity'] = 0
            features['solidity'] = 0
            features['estimated_volume'] = 0

            self.features = features

            return features

        stats_only_features = features

        # Masked background with Gaussian smoothing, image sharpening, and
        # reduction of chromatic aberration

        # mask the raw image with smoothed foreground mask
        blurd_bw_img = gaussian(bw_img_all,3)
        img[:,:,0] = img[:,:,0]*blurd_bw_img
        img[:,:,1] = img[:,:,1]*blurd_bw_img
        img[:,:,2] = img[:,:,2]*blurd_bw_img

        # Make a guess of the PSF for sharpening
        psf = make_gaussian(5, 3, center=None)

        # renormalize
        if np.max(img) == 0:
            img = np.float32(img)
        else:
            img = np.float32(img)/np.max(img)

        # sharpen each color channel and then reconbine
        if deconv:

            img[img == 0] = 0.0001
            img[:,:,0] = restoration.richardson_lucy(img[:,:,0], psf, 7)
            img[:,:,1] = restoration.richardson_lucy(img[:,:,1], psf, 7)
            img[:,:,2] = restoration.richardson_lucy(img[:,:,2], psf, 7)

        # Rescale image to uint8 0-255
        img[img < 0] = 0

        if np.max(img) == 0:
            img = np.uint8(255*img)
        else:
            img = np.uint8(255*img/np.max(img))

        features['image'] = img
        features['binary'] = 255*bw_img_all

        # Save the binary image and also color image if requested
        if save_to_disk:

            try:

                # convert and save images

                # Raw color (no background removal)
                if use_jpeg:
                    if raw_color:
                        cv2.imwrite(os.path.join(abs_path,file_prefix+"_rawcolor.jpeg"),features['rawcolor'])
                    # Save the processed image and binary mask
                    cv2.imwrite(os.path.join(abs_path,file_prefix+".jpeg"),features['image'])
                else:
                    if raw_color:
                        cv2.imwrite(os.path.join(abs_path,file_prefix+"_rawcolor.png"),features['rawcolor'])
                    # Save the processed image and binary mask
                    cv2.imwrite(os.path.join(abs_path,file_prefix+".png"),features['image'])

                # Binary should also be saved png
                cv2.imwrite(os.path.join(abs_path,file_prefix+"_binary.png"),features['binary'])

            except IOError as e:
                logger.error(e)

        self.features = features

        return features





