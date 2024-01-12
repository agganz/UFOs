# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 14:38:15 2024

@author: Alejandro Gonzalez

Changelog:
    0.1 (AG): First version.
    0.2 (AG): Added synchronise_video_with_time
    0.3 (AG): fixed minor bug in synchronise_video_with_time.
        Now the size of the text is adapted for each camera.
    0.4 (AG): added images_to_gif
    0.5 (AG): added get_info_from_keypoints and compare_UFO_brightness_in_two_frames
"""

import math
import cv2
import glob
import numpy as np
import contextlib
from PIL import Image
import os


def get_pulse_str(pulse_id):
    """
    Returns the 7-digit standarised pulse string.

    Parameters
    ----------
    pulse_id : TYPE : int
        The Pulse id as an integer.

    Returns
    -------
    pulse_str: the 7-digit corrected string pulse id.

    """
    
    pulse_str = str(pulse_id)
    
    while len(pulse_str) < 7:
        pulse_str = '0' + pulse_str
        
    return pulse_str


def synchronise_video_with_time(real_time, frame, frame_number):
    """
    Writes into a video frame the current physical time and the frame number.


    Parameters
    ----------
    real_time : float
        the time in seconds.
    frame : cv2 image
        The frame to be edited
    frame_number : int
        The frame of the number.

    Returns
    -------
    frame : cv2.image
        The edited frame.
    """

    real_time = round(real_time, 4)
      
    # font 
    font = cv2.FONT_HERSHEY_SIMPLEX 
      
    # org 
    org = (50, 50) 
      
    # fontScale 
    fontScale = 1
       
    # Blue color in BGR 
    color = (255, 240, 0) 
      
    # Line thickness of 2 px 
    thickness = 2

    first_scale = 2e-3  # Adjust for larger font size in all images
    thickness_scale = 1e-3  # Adjust for larger thickness in all images

    height, width, _ = frame.shape

    fontScale = min(width, height) * first_scale
    
    thickness = math.ceil(min(width, height) * thickness_scale + 0.5)
    # Using cv2.putText() method 
    frame = cv2.putText(frame, 't = ' + str(real_time) + 's', org, font,  
                       fontScale, color, thickness, cv2.LINE_AA) 
    
    return frame
        

def images_to_gifs(output_name, image_folder, image_format = 'png'):
    """
    Creates a gif image with all the image files present in the given folder.

    Parameters
    ----------
    output_name : str
        Name of the ouput gif.
    image_folder : str (path)
        Path to the image folder
    image_format : str. png by default
        Format of the images to be used.

    Returns
    -------
    1 when finished
    """
    
    # filepaths
    fp_in = "{0}/*.{1}".format(image_folder, image_format)

    # use exit stack to automatically close opened images
    with contextlib.ExitStack() as stack:
        # lazily load images
        try:
            imgs = (stack.enter_context(Image.open(f))
                    for f in sorted(glob.glob(fp_in)))
        except:
            raise IndexError('Could not locate any valid images.')

        # extract  first image from iterator
        img = next(imgs)
    
        # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
        img.save(fp = output_name, format='GIF', append_images=imgs,
                 save_all=True, duration=200, loop=0)
        
    return 1


def get_info_from_keypoint(frame, keypoint):
    """

    Parameters
    ----------
    real_time : float
        the time in seconds.
    frame : cv2 image
        The frame to be edited
    frame_number : int
        The frame of the number.

    Returns
    -------
    avg_background : float
        The average brightness of the keypoint.
    radius : float
        The radius of the keypoint.
    """
    
    height, width = frame.shape[0:2]
    (y, x) = (int(keypoint.pt[0]), int(keypoint.pt[1]))
    radius = keypoint.size
    xmin = int(x - radius / 2)

    if xmin < 0:
        xmin = 0
        
    ymin = int(y - radius / 2)
    if ymin < 0:
        ymin = 0
        
    xmax = int(x + radius / 2)
    if xmax >= width:
        xmax = width
        
    ymax = int(y + radius / 2)
    if ymax >= height:
        ymax = height
        
    avg_brightness = np.mean(frame[xmin : xmax, ymin : ymax])
    
    return avg_brightness, radius
    
    
def compare_UFO_brightness_in_two_frames(frame_A, frame_B, keypoints_A, keypoints_B):
    """
    Calculates the ratio between the average intensities of the detected 
    keypoints of two different frames.
    

    Parameters
    ----------
    frame_A : cv2.image
        Current frame.
    frame_B : cv2.image
        Previous  frame.
    keypoints_A : list
        Keypoints of the current frame.
    keypoints_B : list
        Keypoints of the previous frame.

    Returns
    -------
    brightness_ratios : np.ndarray
        Matricial product between the brightness of one frame and the inverse 
        of the other..
    """
    
    brightness_A = [None] * len(keypoints_A)
    brightness_B = [None] * len(keypoints_B)
    
    for i, keyp_A in enumerate(keypoints_A):
        avg_brightness, size = get_info_from_keypoint(frame_A, keyp_A)
        brightness_A[i] = avg_brightness * size
        
    for j, keyp_B in enumerate(keypoints_B):
        avg_brightness, size = get_info_from_keypoint(frame_B, keyp_B)
        brightness_B[j] = avg_brightness * size
        
    brightness_ratios = np.dot(brightness_A, 1 / brightness_B)
        
    return brightness_ratios
