# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 17:43:20 2023

@author: Alejandro Gonzalez Ganzabal

ChangeLog:
    0.1 (AG): First version
    0.1.1 (AG): Added reliance on aux_tools. Removed get_video.
    0.1.2 (AG): added support for linux and windows paths
    0.1.3 (AG): added support for real time vectors.
    0.1.4 (AG): added code for Canny algorithm
    0.2 (AG): now size/brightness ratio are evaluated.
    (AG): changes in parameters and bugs. No version issued.
    0.2.1 (AG): added instant. speed to the arrows (in pixels)
    0.2.2 (AG): increased modularity
    0.3 (AG): several changes to the adjust_frame function
        NOTE: 0.3 has not been checked in Heimdall without GUI
"""

import numpy as np
import cv2
from scipy.spatial import distance_matrix
import os
import sys
import math
from aux_tools import misc_tools
import matplotlib.pyplot as plt



def keypoint_to_xy(keypoint):
    """
    Returns the tuple containing the coordinates from the given keypoints.

    Parameters
    ----------
    keypoint : cv2.keypoints
        The cv2.keypoints to evaluate.

    Returns
    -------
    xy_coords : tuple
        Tuple containing the pixel coordinates.
    """
    
    xy_coords = (int(keypoint.pt[0]), int(keypoint.pt[1]))

    return xy_coords


def filter_points_with_distance_matrix(keypoints_A, keypoints_B, threshold = 10):
    """
    Filters the given keypoints for tracking depending on their euclidean 
    distance measured in pixels. It works with cv2 keypoints.

    Parameters
    ----------
    keypoints_A : list of keypoints (cv2)
        The current cv2.keypoints.
    keypoints_B : list of keypoints (cv2)
        The cv2.keypoints of the previous frame.
    threshold : int - 10 by default.
        the distance theshold in pixels. 
    check_brightness : float - 0 by default.
        Will check the ratio between the given points as well as the distance.
        The accepted ratio is 1+-check_brightness. Can be left as 0 to skip.

    Returns
    -------
    start_points : list
        The xy coordinates of the starting points..
    end_points : list
        The xy coordinates of the ending points.
    """
    
    start_points = []
    end_points = []
    
    if len(keypoints_A) == 0 or len(keypoints_B) == 0:
        return (None, None)
    
    current_points = np.array([keypoints_A])
    past_points = np.array([keypoints_B])
 
    distance_vector = distance_matrix(current_points, past_points)
    keypositions = np.argwhere(np.logical_and(distance_vector < threshold, distance_vector >= 3))

    for elem in keypositions:
        start_points.append(past_points[elem[1]])
        end_points.append(current_points[elem[0]])
        
    return start_points, end_points

    
def draw_arrow_in_frame(frame, start_points, end_points, frame_number = None, time_vec = None, delta_time = None):
    """
    Draws arrows int othe given frame following the positions 

    If either frame-number or time_vec are left non-specified, the arrows 
    will be drawn, but no calculations regarding speed will be done.
    
    Parameters
    ----------
    frame : cv2 image
        The frame in which the arrow will be painted
    start_points : list of starting positions
        tuples of pixel coordinates.
    end_points : list of final positions
        tuples of pixel coordinates.
    frame_number : int
        The number of the current frame.
    time_vec : array. None by default.
        The real time array in seconds.
    delta_time : int. None by default
        The frame rate without time vec.

    Returns
    -------
    frame : cv2 image
        frame edited with the arrow
    """

    if frame_number is not None and time_vec is not None:
        time_flag = True
        delta_time = time_vec[frame_number] - time_vec[frame_number - 1]
    else:
        if delta_time is None:
            time_flag = False
        else:
            time_flag = True
    
    speed_dict = dict()

    for p in range(0, len(start_points)):
        initial_point = start_points[p]
        final_point = end_points[p]
        if time_flag:
            disp_mod = math.dist(initial_point, final_point)
            coords = (int((final_point[0] + initial_point[0]) / 2), int((final_point[1] + initial_point[1]) / 2))
            ins_speed = int(disp_mod / delta_time)  # displacement in pixels
            frame = misc_tools.add_small_annotation(str(ins_speed), frame, coords)
            speed_dict.update({tuple(final_point) : ins_speed})
        frame = cv2.arrowedLine(frame, initial_point, final_point, (0, 255, 0), 3, 1, 0, 0.2)

    return frame, speed_dict


def get_detected_shapes(frame):
    """
    """

    print('size original: ', frame.shape)
    try:
        col_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    except:
        img_float32 = np.float32(frame)
        col_frame = cv2.cvtColor(img_float32, cv2.COLOR_GRAY2RGB)

    try:
        cnts = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    except:
        thres_im = frame.astype(np.uint8)
        cnts = cv2.findContours(thres_im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    min_area = 5
    white_dots = []
    cX_l = []
    cY_l = []

    for c in cnts:
        area = cv2.contourArea(c)
        if area > min_area:
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cX_l.append(cX)
            cY_l.append(cY)
            cv2.drawContours(col_frame, [c], -1, (0, 0, 255), 2)
            white_dots.append(c)

    for i in range(0, len(cX_l)):
        keypoints = (cX_l[i], cY_l[i])

    print(keypoints)
    print(col_frame.shape)
    return col_frame, keypoints