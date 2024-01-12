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
"""

import numpy as np
import cv2
from scipy.spatial import distance_matrix
import os
import sys
from aux_tools import misc_tools


def get_time_vector(pulse_id):
    """
    Returns the time-frame vector for the given pulse.
    
    WARNING: needs to have the SAL library installed correctly. Better run in 
    one of the JDC machines. This is way the library is imported here instead 
    of the beginning of the file - otherwise it will make the whole code 
    useless.
    
    It will also request user - password login, but not inside a JDC machine.

    Parameters
    ----------
    pulse_id : TYPE : int
        The pulse ID.

    Returns
    -------
    time_vec : TYPE : ndarray
        The time-frame equivalence.

    """
    
    from jet.data import sal 
    
    time_vec_obj = sal.get('/pulse/{0}/jpf/dj/kldt-o5wb_in_tim/data'.format(pulse_id))
    time_vec = time_vec_obj.data
    
    return time_vec

    
def examine_video_for_UFOs(vid_path, pulse_id, camera_name, time_vec = None):
    """
    Analyses the video passed and creates a frame-by-frame image set
    in a folder (<camera_name>_<pulse_id>) with a blob-based detection 
    with basic tracking.


    Parameters
    ----------
    vid_path : str
        The path to the video.
    pulse_id : int
        The pulse number identifier.
    camera_name : str
        The name of the camera
    time_vec : 1D array
        The time vector. None by default.

    Returns
    -------
    None.
    """
    
    # check folder/create 
    
    pulse_str = misc_tools.get_pulse_str(pulse_id)
    
    folder_name = camera_name + '_' + pulse_str
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    
        
    if not os.path.isfile(vid_path):
        raise FileNotFoundError('Could not locate the video file in the given path ({0})'.format(vid_path))
        
    video = cv2.VideoCapture(vid_path)
    #height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    #width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    
    counter = 1
    # Detect blobs.
    params = cv2.SimpleBlobDetector_Params()
        
    # Change thresholds
    params.minThreshold = 45
    params.maxThreshold = 255
        
    # Filter by Area.
    params.filterByArea = True
    params.minArea = 5
    params.maxArea = 300
        
    params.filterByColor = False
    params.blobColor = 40
        
    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.2
        
    # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0.2
        
    # Filter by Inertia
    params.filterByInertia = False
    params.minInertiaRatio = 0.25
        
    # Create a detector with the parameters
    # OLD: detector = cv2.SimpleBlobDetector(params)
    detector = cv2.SimpleBlobDetector_create(params)
    
    while True:
        ret, frame = video.read()
        
        if ret == False or not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect blobs.
        
        # Filter by brightness
        #bkg_brightness = int((gray[0][0] + gray[0][-1] + gray[-1][0] + gray[-1][-1]) / 4)
        bkg_brightness = np.mean(gray)
        min_bkg = int(20 + bkg_brightness)
        if min_bkg > 210:
            min_bkg = 210
        params.minThreshold = min_bkg
        print(params.minThreshold)
        params.maxThreshold = 255
 
        if counter == 1:
            width, height = gray.shape
            # Filter by area
            params.filterByArea = True
            resolution = int(width * height)
            params.minArea = int(resolution * 3.5e-5)
            params.maxArea = int(resolution * 2.16e-2)
            tmp_keypoints = []
        detector = cv2.SimpleBlobDetector_create(params)

        #treated_frame = gray
        median = cv2.medianBlur(gray, 5)
        treated_frame = cv2.Canny(median, min_bkg, 255)
        keypoints = detector.detect(median)
        im_with_keypoints = cv2.drawKeypoints(gray, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        if tmp_keypoints != keypoints:
            #print('Checking tmp and key: ', tmp_keypoints, keypoints)
            (start_points, end_points) = filter_points_with_distance_matrix(keypoints, tmp_keypoints, threshold = 20, 0.1, gray, tmp_frame)
            if start_points is None:
                pass
            else:
                im_with_keypoints = draw_arrow_in_frame(im_with_keypoints, start_points, end_points)
            
        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob

        if not time_vec is None:
            final_frame = misc_tools.synchronise_video_with_time(time_vec[counter - 1], im_with_keypoints, counter)
        else:
            final_frame = im_with_keypoints

	    # evaluate OS
        if sys.platform == 'linux':
            cv2.imwrite("{0}/{1}.png".format(folder_name, counter), final_frame)
        elif sys.platform == 'win32':
            cv2.imwrite(r"{0}\{1}.png".format(folder_name, counter), final_frame)
        else:
            raise OSError('Not applicable to current OS. Either linux or win32 expected.')
            
        counter = counter + 1        
        tmp_keypoints = keypoints
        frame_B = gray
        
        print('Frame {0}'.format(counter))
        
    video.release()
    cv2.destroyAllWindows()
    
    return 1
    
    
def recreate_video(pulse_id):
    """
    Creates a video with the processed images for each pulse.
    
    This seems to produce buggy results. At the moment it might be more 
    convenient to use rely on gifs.
    """
    
    pulse_str = misc_tools.get_pulse_str(pulse_id)
    
    image_folder = pulse_str
    video_name = '{0}_detect.mp4'.format(pulse_str)

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    
    video = cv2.VideoWriter(video_name, 0, 1, (width,height))
    
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))
    
    cv2.destroyAllWindows()
    video.release()
    
    return True
    

def treat_frame(current_frame, previous_frame):
    """
    Substracts two consecutive frames in colour space (:, :, 3).
    
    It also multiplies by 2 the resulting frame, considering that an increase 
    in contrast can be written as f' = f * alpha + beta, being beta additional 
    brightness.
    
    
    Returns
    -------
    None.

    """
    
    # TODO
    res = current_frame

    return res


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


def filter_points_with_distance_matrix(keypoints_A, keypoints_B, threshold = 10, check_brightness = 0, frame_A = None, frame_B = None):
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
    
    current_points = [None] * len(keypoints_A)
    past_points = [None] * len(keypoints_B)

    for i in range(0, len(keypoints_A)):
        current_points[i] = keypoint_to_xy(keypoints_A[i])
        
    for i in range(0, len(keypoints_B)):
        past_points[i] = keypoint_to_xy(keypoints_B[i])
    
 
    distance_vector = distance_matrix(current_points, past_points)
    
    keypositions = np.argwhere(distance_vector < threshold)
    if check_brightness != 0:
        brightness_ratios = misc_tools.compare_UFO_brightness_in_two_frames(frame_A, frame_B, keypoints_A, keypoints_B)        
        brightness_positions = np.argwhere(np.logical_and(brightness_ratios >= 1 - check_brightness, brightness_ratios <= 1 + check_brightness))
        
    for elem in keypositions:
        if check_brightness:
            if elem in brightness_positions:
                start_points.append(past_points[elem[1]])
                end_points.append(current_points[elem[0]])
        else:
            start_points.append(past_points[elem[1]])
            end_points.append(current_points[elem[0]])
        
    return start_points, end_points

    
def draw_arrow_in_frame(frame, start_points, end_points):
    """
    Draws arrows int othe given frame following the positions 

    Parameters
    ----------
    frame : cv2 image
        The frame in which the arrow will be painted
    start_points : list of starting positions
        tuples of pixel coordinates.
    end_points : list of final positions
        tuples of pixel coordinates

    Returns
    -------
    frame : cv2 image
        frame edited with the arrow
    """
    
    for p in range(0, len(start_points)):
        initial_point = start_points[p]
        final_point = end_points[p]
        cv2.arrowedLine(frame, initial_point, final_point, (0, 255, 0), 2, 5, 0, 0.5)

    return frame

