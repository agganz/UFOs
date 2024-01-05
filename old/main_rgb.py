# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 16:10:53 2023

@author: Doctorando1
"""

import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
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


def get_video(pulse_id):
    """

    Parameters
    ----------
    pulse_id : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    
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

    
def examine_video_for_UFOs(pulse_id = 99910):
    """
    Parameters
    ----------
    pulse_id : TYPE
        DESCRIPTION.

    Returns
    -------
    None.
    """
    
    # check folder/create 
    
    pulse_str = get_pulse_str(pulse_id)
    
    if not os.path.isdir(pulse_str):
        os.mkdir(pulse_str)
    
    
    vid_path = '0099910.wmv'
    if os.path.isfile(vid_path):
        print('isfile')
        
    video = cv2.VideoCapture(vid_path)
    #height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    #width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    
    counter = 0
    
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
        params.maxArea = 1500
        
        params.filterByColor = False
        params.blobColor = 40
        
        # Filter by Circularity
        params.filterByCircularity = True
        params.minCircularity = 0.2
        
        # Filter by Convexity
        params.filterByConvexity = False
        params.minConvexity = 0.2
        
        # Filter by Inertia
        params.filterByInertia = True
        params.minInertiaRatio = 0.25
        
        # Create a detector with the parameters
        # OLD: detector = cv2.SimpleBlobDetector(params)
        detector = cv2.SimpleBlobDetector_create(params)
        
        if counter == 0:
            treated_frame = frame
        else:
            treated_frame = treat_frame(frame, tmp_frame)
            
        # Detect blobs.
        keypoints = detector.detect(treated_frame)
        if len(keypoints) == 0:
            pass
         
        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (255,255,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        cv2.imwrite(r"{0}\frame_{1}.png".format(pulse_str, counter), im_with_keypoints)
            
        if counter == 256:
            cv2.imwrite(r"{0}\noborrar_{1}.png".format(pulse_str, counter), frame)

        counter = counter + 1        
        tmp_frame = frame
        
    video.release()
    cv2.destroyAllWindows()
    

def synchronise_video_with_time(time_vec, frame, frame_number):
    '''
    Writes into a video frame the current physical time and the frame number.
    
    
    
    Returns
    -------
    None.

    '''
      
    # font 
    font = cv2.FONT_HERSHEY_SIMPLEX 
      
    # org 
    org = (50, 50) 
      
    # fontScale 
    fontScale = 1
       
    # Blue color in BGR 
    color = (255, 255, 0) 
      
    # Line thickness of 2 px 
    thickness = 2
       
    # Using cv2.putText() method 
    frame = cv2.putText(frame, 'OpenCV', org, font,  
                       fontScale, color, thickness, cv2.LINE_AA) 
    
    return frame
        
    
    
def recreate_video(pulse_id):
    """
    """
    
    pulse_str = get_pulse_str(pulse_id)
    
    image_folder = pulse_str
    video_name = '{0}_detect.wmv'.format(pulse_str)

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    
    video = cv2.VideoWriter(video_name, 0, 1, (width,height))
    
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))
    
    cv2.destroyAllWindows()
    video.release()
    
    return True
    
    
def delete_all_outputs():
    
    files = glob.glob('output_*')
    for f in files:
        os.remove(f)
    

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
    
    treated_frame = cv2.subtract(current_frame, previous_frame)
    
    return treated_frame * 2 + 20