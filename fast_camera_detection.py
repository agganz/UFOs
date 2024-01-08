# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 17:43:20 2023

@author: Alejandro Gonzalez Ganzabal

ChangeLog:
    V.- 0.1 (AG): First version
    V.- 0.1.1 (AG): Added reliance on aux_tools. Removed get_video.
"""

import numpy as np
import cv2
from scipy.spatial import distance_matrix
import os
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

    
def examine_video_for_UFOs(vid_path, pulse_id, camera_name):
    """
    Parameters
    ----------
    vid_path : str
        The path to the video.
    pulse_id : int
        The pulse number identifier.
    camera_name : str
        The name of the camera

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
    params.minThreshold = 10
    params.maxThreshold = 255
        
    # Filter by Area.
    params.filterByArea = True
    params.minArea = 3
    params.maxArea = 300
        
    params.filterByColor = False
    params.blobColor = 40
        
    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.3
        
    # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0.2
        
    # Filter by Inertia
    params.filterByInertia = True
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
        
        if counter == 1:
            tmp_keypoints = []

        treated_frame = gray
        
        keypoints = detector.detect(treated_frame)
        im_with_keypoints = cv2.drawKeypoints(gray, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        if tmp_keypoints != keypoints:
            print('Checking tmp and key: ', tmp_keypoints, keypoints)
            (start_points, end_points) = filter_points_with_distance_matrix(keypoints, tmp_keypoints, threshold = 20)
            if start_points is None:
                pass
            else:
                im_with_keypoints = draw_arrow_in_frame(im_with_keypoints, start_points, end_points)
            
        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob

        cv2.imwrite(r"{0}\{1}.png".format(folder_name, counter), im_with_keypoints)
            
        counter = counter + 1        
        tmp_keypoints = keypoints
        
        print('Frame {0}'.format(counter))
        
    video.release()
    cv2.destroyAllWindows()
    
    return 1
    

def synchronise_video_with_time(time_vec, frame, frame_number):
    """
    Writes into a video frame the current physical time and the frame number.


    Parameters
    ----------
    time_vec : 1D array
        DESCRIPTION.
    frame : cv2 image
        The frame to be edited
    frame_number : int
        The frame of the number.

    Returns
    -------
    frame : TYPE
        DESCRIPTION.

    """
      
    # font 
    font = cv2.FONT_HERSHEY_SIMPLEX 
    time_frame = time_vec[frame_number]
      
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
        
    
    
def recreate_video(pulse_id):
    """
    Creates a video with the processed images for each pulse.
    
    
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
        print('No consecutive points.')
        return (None, None)
    
    current_points = [None] * len(keypoints_A)
    past_points = [None] * len(keypoints_B)

    for i in range(0, len(keypoints_A)):
        current_points[i] = keypoint_to_xy(keypoints_A[i])
        
    for i in range(0, len(keypoints_B)):
        past_points[i] = keypoint_to_xy(keypoints_B[i])
            
    distance_vector = distance_matrix(current_points, past_points)
    keypositions = np.argwhere(distance_vector < threshold)

    for elem in keypositions:
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

