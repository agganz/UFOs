# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 14:38:15 2024

@author: Alejandro Gonzalez

Changelog:
    0.1 (AG): First version.
    0.2 (AG): Added synchronise_video_with_time
    0.3 (AG): fixed minor bug in synchronise_video_with_time.
        Now the size of the text is adapted for each camera.
"""

import math
import cv2

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
        
