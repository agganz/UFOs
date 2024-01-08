# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 14:32:46 2024

@author: Alejandro Gonzalez

Changelog:
    V.-0.1 (AG): First version. Works for local files.
"""
    
from aux_tools import misc_tools
import main_hsv
import fast_camera_detection
import os


def main(camera_name, pulse_id, trange = None):
    """
    Examines a given video in search of UFOs.
    
    If the video can be found locally, 
    
    Currently supports video from fast cameras (expected as -E) and operational 
    cameras (expected as -O). For the first type, the UFOs are located by blob 
    detection in black and white. A basic trackability register is performed as 
    well. For Operational camera videos, a switch to HSV base is performed in 
    order to detatch the background colours to make better detection.

    Parameters
    ----------
    camera_name : str
        The complete name of the camera by JET's standards (whatever they are)
    pulse_id : int
        The pulse id number.
    trange : tuple, optional
        The time range. The default is None.

    Returns
    -------
    int
        1 if finished.
    """
    
    try:
        import jet2video
        jet2video_flag = True
    except ModuleNotFoundError:
        jet2video_flag = False
        
    pulse_str = misc_tools.get_pulse_str(pulse_id)
    output_filename = camera_name + '_' + str(pulse_id) + '.mp4'

    if not jet2video_flag:
        # search locally
        if os.path.isfile(output_filename):
            print('Found file locally.')
            jet2video_flag = False
        else:
            jet2video_flag = True
    
    if jet2video_flag:
        time_vec = jet2video.export_jet_video(camera_name, pulse_id, output_filename, fps = None, bitrate = 5000, dynamic_clim = True, clim = None, meta = ['jpn','camera','time'], time_range = trange)
    else:
        print('Local search')
        
    if '-O' in camera_name.upper():
        print('Operational camera detected.')
        res_UFO_search = main_hsv.examine_video_for_UFOs(output_filename, pulse_id, camera_name)
    else:
        print('Fast camera')
        res_UFO_search= fast_camera_detection.examine_video_for_UFOs(output_filename, pulse_id, camera_name)
        
    return 1