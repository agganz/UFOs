# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 16:53:57 2023

@author: Doctorando1
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2
from VVideo import VVideo


def rot_frames(list_of_frames, rotations = 3):
    """
    

    Parameters
    ----------
    list_of_frames : TYPE
        DESCRIPTION.
    rotations : TYPE, optional
        DESCRIPTION. The default is 3.

    Returns
    -------
    None.

    """
    
    new_list = [] * len(list_of_frames)
    
    for count, frame in enumerate(list_of_frames):
        new_frame = np.rot90(frame, rotations)
        new_list[count] = new_frame
    
    return(new_list)


