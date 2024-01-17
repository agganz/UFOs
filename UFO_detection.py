# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 14:32:46 2024

@author: Alejandro Gonzalez

Changelog:
    0.1 (AG): First version. Works for local files.
    0.1.1 (AG): tested support for jet2video. Added time_vec support
    0.1.2 (AG): added basic command line support. To be tested.
    0.1.3 (AG): added support for background extraction.
    0.1.4 (AG): added frame rate. TBT
"""
    
from aux_tools import misc_tools
import main_hsv
import fast_camera_detection
import os
import sys
import warnings


def main(camera_name, pulse_id, trange = None, sub_bkg = False, frame_rate = 400):
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
    sub_bkg : bool
        Substracts bkg if possible.

    Returns
    -------
    int
        1 if finished.
    """
    
    try:
        import jet2video
        jet2video_flag = True
    except ModuleNotFoundError:
        warnings.warn('Could not import jet2video.')
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
        time_vec = jet2video.export_jet_video(camera_name, pulse_id, output_filename, fps = None, bitrate = 5000, dynamic_clim = True, clim = None, meta = ['jpn','camera','time'], time_range = trange, extract_bkg = sub_bkg)
        if len(time_vec) == 0:
            time_vec = None
    else:
        print('Local search')
        time_vec = None
        
    if '-O' in camera_name.upper():
        print('Operational camera detected.')
        res_UFO_search = main_hsv.examine_video_for_UFOs(output_filename, pulse_id, camera_name, time_vec)
    else:
        print('Fast camera')
        res_UFO_search = fast_camera_detection.examine_video_for_UFOs(output_filename, pulse_id, camera_name, time_vec, frame_rate = 400)
        
    return 1


if __name__ == '__main__':
    camera_name = sys.argv[1]
    pulse_id = sys.argv[2]
    trange = sys.argv[3]
    main(camera_name, pulse_id, trange)
