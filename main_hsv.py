# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 17:43:20 2023

@author: Alejandro Gonzalez Ganzabal

ChangeLog:
    V.- 0.1 (AG): First version
    V.- 0.1.1 (AG): changes done to match UFO_detection
    V.- 0.1.2 (AG): added support for linux and windows paths
"""

import numpy as np
import cv2
import os
from aux_tools import misc_tools
import sys


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
    
    while True:
        ret, frame = video.read()
        
        if ret == False:
            break
        
       # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        if not ret:
            break
        
      #  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        
        # Detect blobs.
        params = cv2.SimpleBlobDetector_Params()
        
        # Change thresholds
        params.minThreshold = 20
        params.maxThreshold = 255
        
        # Filter by Area.
        params.filterByArea = True
        params.minArea = 5
        params.maxArea = 2000
        
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
        
        if counter == 1:
            treated_frame = frame
        else:
            treated_frame = treat_frame(frame, tmp_frame)
            
        # Detect blobs.
        keypoints = detector.detect(treated_frame)
         
        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (255,255,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
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
        tmp_frame = frame
        
        print('Frame {0}'.format(counter))
        
    video.release()
    cv2.destroyAllWindows()
    
    return 1
    
    
def recreate_video(pulse_id):
    """
    Creates a video with the processed images for each pulse.
    
    
    """
    
    pulse_str = get_pulse_str(pulse_id)
    
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
    
    hsv = cv2.cvtColor(current_frame, cv2.COLOR_BGR2HSV)
    
    # upper boundary RED color range values; Hue (160 - 180)
    
    lower1 = np.array([0, 40, 1])
    upper1 = np.array([10, 255, 255])

    lower2 = np.array([140,40,1])
    upper2 = np.array([179,255,255])
     
    lower_mask = cv2.inRange(hsv, lower1, upper1)
    upper_mask = cv2.inRange(hsv, lower2, upper2)
     
    full_mask = lower_mask + upper_mask
#    res = cv2.bitwise_and(current_frame, current_frame, mask = mask)
    
    mask_inv = cv2.bitwise_not(full_mask)
    #Filter the regions containing colours other than red from the grayscale image(background)
    res = cv2.bitwise_and(current_frame, current_frame, mask = mask_inv)
    #convert the one channelled grayscale background to a three channelled image
    #background = np.stack((background,)*3, axis=-1)
    #add the foreground and the background
    #added_img = cv.add(res, background)

    return res


def select_divertor_colour_paletter():
    pass
