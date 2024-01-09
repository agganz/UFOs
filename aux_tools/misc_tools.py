# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 14:38:15 2024

@author: Alejandro Gonzalez

Changelog:
    0.1 (AG): First version.
    0.2 (AG): Added synchronise_video_with_time
"""

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
      
    # font 
    font = cv2.FONT_HERSHEY_SIMPLEX 
    time_frame = real_time[frame_number]
      
    # org 
    org = (50, 50) 
      
    # fontScale 
    fontScale = 1
       
    # Blue color in BGR 
    color = (255, 255, 0) 
      
    # Line thickness of 2 px 
    thickness = 2
       
    # Using cv2.putText() method 
    frame = cv2.putText(frame, str(time_frame), org, font,  
                       fontScale, color, thickness, cv2.LINE_AA) 
    
    return frame
        