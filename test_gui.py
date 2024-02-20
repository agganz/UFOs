# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 16:44:13 2023

@author: Alejandro Gonzalez Ganzabal


ChangeLog

    0.1 (AG): First version (GIT)
    0.2 (AG): Added pulse search; changed function arguments.
    0.2.1 (AG): Still on progress - noow it shows the frames
    0.2.2 (AG): almost functional
    0.2.3 (AG): working up to selecting keypoints
"""

import sys
import cv2
import os
import numpy as np
import pandas as pd
import re
import fast_camera_detection
from aux_tools import misc_tools

# QT5 stuff
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QTableWidget, QTableWidgetItem,
    QMessageBox,
    QLabel,
    QGridLayout,
    QFileDialog,
    QMainWindow,
    QFormLayout,
    QWidget,
    QLineEdit,
    QVBoxLayout,
    QCheckBox,
    QPushButton
)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("JUUT")
        
        self.main_layout = QGridLayout()

        # Create a form layout and add widgets

        self.conf_image_layout = QFormLayout()
        self.video_btn = QPushButton()
        self.video_btn.setCheckable(False)
        self.video_btn.setText('Select file...')
        
        self.video_filename = None
        self.video_btn.clicked.connect(self.get_video_filename)

        self.conf_image_layout.addRow("Enter video name:", self.video_btn)
        
        self.frame_number = QLineEdit()
        self.conf_image_layout.addRow("Frame number:", self.frame_number)

        self.median_filt = QCheckBox('Apply median filter')
        self.conf_image_layout.addWidget(self.median_filt)
        self.canny_al = QCheckBox('Apply Canny algorithm')
        self.conf_image_layout.addWidget(self.canny_al)
        self.LoG_btn = QCheckBox('Apply Laplacian of Gaussian filter')
        self.conf_image_layout.addWidget(self.LoG_btn)
        self.threshold_btn = QCheckBox('Apply threshold with min. brightness')
        self.conf_image_layout.addWidget(self.threshold_btn)

        self.min_bkg_image = QLineEdit()
        self.conf_image_layout.addRow("Minimum background for frame:", self.min_bkg_image)
        self.delta_time_box = QLineEdit()
        self.conf_image_layout.addRow("Video real frame rate:", self.delta_time_box)

        # detecting set up
        self.conf_detect_layout = QFormLayout()
        self.det_brightness = QLineEdit()
        self.det_inertia = QLineEdit()
        self.det_convexety = QLineEdit()
        self.det_size = QLineEdit()
        self.det_circularity = QLineEdit()
        self.conf_detect_layout.addRow("Detector brightness:", self.det_brightness)
        self.conf_detect_layout.addRow("Detector size:", self.det_size)
        self.conf_detect_layout.addRow("Detector inertia:", self.det_inertia)
        self.conf_detect_layout.addRow("Detector convexity:", self.det_convexety)
        self.conf_detect_layout.addRow("Detector circularity:", self.det_circularity)

        # Image
       # self.frame_1 = None
       #♠ self.frame_2 = None
        
        
        # Add a button box
        self.btnBox = QPushButton()
        self.btnBox.setCheckable(False)
        self.btnBox.setText('Get frame')
        self.btnBox.clicked.connect(self.get_image_when_clicked)


        # Add the detect box
        self.btndet = QPushButton()
        self.btndet.setCheckable(False)
        self.btndet.setText('Make detection')
        self.btndet.clicked.connect(self.make_detection)
        
        # Set the layout on the dialog
        self.main_layout.addLayout(self.conf_image_layout, 0, 0)
        self.main_layout.addWidget(self.btnBox, 1, 0)
        self.main_layout.addLayout(self.conf_detect_layout, 2, 0)
        self.main_layout.addWidget(self.btndet, 3, 0)

        self.auto_detect = QCheckBox('Auto detect?')
        self.main_layout.addWidget(self.auto_detect, 4, 0)

        self.setLayout(self.main_layout)        
        self.container = QWidget()
        self.container.setLayout(self.main_layout)
        self.setCentralWidget(self.container)
        
        
    def get_image_when_clicked(self):
        """
        Shows the image corresponding to the current frame and the next, including 
        all the filtering options.
        """
        
        video_name_str = self.video_filename
        try:
            frame_number_int = int(self.frame_number.text())
        except ValueError:
            self.show_error_message('Please enter a valid frame number. Switching to 1.')
            frame_number_int = 1
            self.frame_number.setText('1')

        if not os.path.isfile(video_name_str):
            raise FileNotFoundError('Could not locate the video file in the given path ({0})'.format(video_name_str))
        
        gray_1 = get_frame_from_video(video_name_str, frame_number_int)
        gray_2 = get_frame_from_video(video_name_str, 1 + frame_number_int)

        use_median = self.median_filt.isChecked()
        use_canny = self.canny_al.isChecked()
        use_LoG = self.LoG_btn.isChecked()
        use_threshold = self.threshold_btn.isChecked()
        
        try:
            min_bkg_im = int(self.min_bkg_image.text())
        except ValueError:
            min_bkg_im = int(np.mean(gray_1))
            
        self.frame_1_cv2 = fast_camera_detection.adjust_frame(gray_1, canny_al = use_canny, median_al = use_median, LoG = use_LoG,  min_bkg = min_bkg_im, thresholding = use_threshold, div_mask_limits = None)
        self.frame_2_cv2 = fast_camera_detection.adjust_frame(gray_2, canny_al = use_canny, median_al = use_median, LoG = use_LoG, min_bkg = min_bkg_im, thresholding = use_threshold, div_mask_limits = None)
        misc_tools.save_frame('.', 1, self.frame_1_cv2)
        misc_tools.save_frame('.', 2, self.frame_2_cv2)

        self.frame_1 = '1.png'
        self.frame_2 = '2.png'
    
        self.frame_1_layout = QVBoxLayout()
        self.frame_2_layout = QVBoxLayout()
        
        self.label_pix_1 = QLabel()
        self.label_pix_1.setText('Frame {0}'.format(frame_number_int))
        self.pixmap_1 = QPixmap(self.frame_1)
        self.label_pix_1.setPixmap(self.pixmap_1)
        self.frame_1_layout.addWidget(self.label_pix_1)
        
        self.label_pix_2 = QLabel()
        self.pixmap_2 = QPixmap(self.frame_2)
        self.label_pix_2.setPixmap(self.pixmap_2)
        self.frame_2_layout.addWidget(self.label_pix_2)

        self.main_layout.addLayout(self.frame_1_layout, 0, 1)
        self.main_layout.addLayout(self.frame_2_layout, 0, 2)
        
        # Go to next frame
        self.btn_nextframe = QPushButton()
        self.btn_nextframe.setCheckable(False)
        self.btn_nextframe.setText('Next frame')
        self.btn_nextframe.clicked.connect(self.go_next)
        
        self.main_layout.addWidget(self.btn_nextframe, 2, 2)

        # Previous frame
        self.btn_prevframe = QPushButton()
        self.btn_prevframe.setCheckable(False)
        self.btn_prevframe.setText('Previous frame')
        self.btn_prevframe.clicked.connect(self.go_prev)
        
        self.main_layout.addWidget(self.btn_prevframe, 2, 1)
        
        self.btn_keypoints = QPushButton()
        self.btn_keypoints.setCheckable(False)
        self.btn_keypoints.setText('Open keypoints dialog')
        self.btn_keypoints.clicked.connect(self.keypoints_dialog)
        
        self.main_layout.addWidget(self.btn_keypoints, 3, 2)

        if self.auto_detect.isChecked():
            self.make_detection()
        
        
    def go_next(self):
        """
        Moves the frame number up by one number.
        """
        
        self.frame_number.setText(str(int(self.frame_number.text()) + 1))
        self.get_image_when_clicked()
        

    def go_prev(self):
        """
        Moves the frame number down by one number.
        """

        self.frame_number.setText(str(int(self.frame_number.text()) - 1))
        self.get_image_when_clicked()
        
        
    def define_detector(self):
        """
        Defines the detector parameters for creating a blob detector.

        Returns
        -------
        detector : cv2.detector type
            The detector with the new parameters.
        """
        
        params = cv2.SimpleBlobDetector_Params()

        brightness_det = self.det_brightness.text()
        if brightness_det != '':
            minb, maxb = re.findall(r"[+]?(?:\d*\.*\d+)", brightness_det)
            params.minThreshold = int(minb)
            params.maxThreshold = int(maxb)
        else:
            self.show_error_message('At least the detector brightness must be specified. Default value will be set.')
            self.det_brightness.setText('40-255')
            brightness_det = self.det_brightness.text()
            minb, maxb = re.findall(r"[+]?(?:\d*\.*\d+)", brightness_det)
            params.minThreshold = int(minb)
            params.maxThreshold = int(maxb)
        size_det = self.det_size.text()

        if size_det != '':
            params.filterByArea = True
            min_size, max_size = re.findall(r"[+]?(?:\d*\.*\d+)", size_det)
            params.minArea = int(min_size)
            params.maxArea = int(max_size)
        else:
            params.filterByArea = False
            
        inertia_det = self.det_inertia.text()
        if inertia_det != '':
            params.filterByInertia = True
            min_inertia, max_inertia = re.findall(r"[+]?(?:\d*\.*\d+)", inertia_det)
            params.minInertiaRatio = float(min_inertia)
            params.maxInertiaRatio = float(max_inertia)
        else:
            params.filterByArea = False
        
        convexity_det = self.det_convexety.text()
        if convexity_det != '':
            params.filterByConvexity = True
            min_convexity, max_convexity = re.findall(r"[+]?(?:\d*\.*\d+)", inertia_det)
            params.minConvexity = float(min_convexity)
            params.maxConvexity = float(max_convexity)
        else:
            params.filterByConvexity = False
            
        circularity_det = self.det_circularity.text()
        if circularity_det != '':
            params.filterByCircularity = True
            min_circularity, max_circularity = re.findall(r"[+]?(?:\d*\.*\d+)", inertia_det)
            params.minCircularity = float(min_circularity)
            params.maxCircularity = float(max_circularity)
        else:
            params.filterByCircularity = False

        params.minRepeatability = 2
        
        detector = cv2.SimpleBlobDetector_create(params)
            
        return detector
    
    
    def make_detection(self):
        """
        Makes detection over the current frames.
        If possible, will try to connect the keypoints.
        """
        
        self.detector = self.define_detector()
        keypoints_A = self.detector.detect(self.frame_1_cv2)
        keypoints_B = self.detector.detect(self.frame_2_cv2)
        
        self.im_with_keypoints_A = cv2.drawKeypoints(self.frame_1_cv2, keypoints_A, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        self.im_with_keypoints_B = cv2.drawKeypoints(self.frame_1_cv2, keypoints_B, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        print(keypoints_A, keypoints_B)

        try:
            delta_time = int(self.delta_time_box.text())
        except ValueError:
            self.show_error_message('Could not read delta time. Setting it to 30.')
            self.delta_time_box.setText('30')
            delta_time = int(self.delta_time_box.text())

        if len(keypoints_A) != 0 and len(keypoints_B) != 0:
            (start_points, end_points) = fast_camera_detection.filter_points_with_distance_matrix(keypoints_A, keypoints_B, threshold = 100, check_brightness = 0, frame_A = self.frame_1_cv2, frame_B = self.frame_2_cv2)
            if start_points is None:
                pass
            else:
                self.im_with_keypoints_A, self.speed_dict = fast_camera_detection.draw_arrow_in_frame(self.im_with_keypoints_A, start_points, end_points, frame_number = None, time_vec = None, delta_time = delta_time)
            
        self.refresh_image_detection()
        
        
    def refresh_image_detection(self):
        """
        Refresh the current images with new inputs after the detection.
        """
        
        misc_tools.save_frame('.', 1, self.im_with_keypoints_A)
        misc_tools.save_frame('.', 2, self.im_with_keypoints_B)

        self.frame_1 = '1.png'
        self.frame_2 = '2.png'
        
        print('max', np.max(self.frame_1_cv2))
    
        self.frame_1_layout = QVBoxLayout()
        self.frame_2_layout = QVBoxLayout()
        
        self.label_pix_1 = QLabel()
        self.label_pix_1.setText('Frame {0}'.format(self.frame_number.text()))
        self.pixmap_1 = QPixmap(self.frame_1)
        self.label_pix_1.setPixmap(self.pixmap_1)
        self.frame_1_layout.addWidget(self.label_pix_1)
        
        self.label_pix_2 = QLabel()
        self.pixmap_2 = QPixmap(self.frame_2)
        self.label_pix_2.setPixmap(self.pixmap_2)
        self.frame_2_layout.addWidget(self.label_pix_2)

        self.main_layout.addLayout(self.frame_1_layout, 0, 1)
        self.main_layout.addLayout(self.frame_2_layout, 0, 2)
        
        
    def get_video_filename(self):
        """
        Opens the file browser and updates the video file path, updated in 
        self.video_filename.
        """
        
        path = QFileDialog.getOpenFileName()
        self.video_filename = path[0]


    def show_error_message(self, message):
        """
        Shows an error message instead of crashing (I hope?)
        """

        error_dialog = QMessageBox() 
        error_dialog.setIcon(QMessageBox.Information) 
  
        # setting message for Message Box 
        error_dialog.setText(message) 
        error_dialog.setStandardButtons(QMessageBox.Ok) 
        error_dialog.exec_() 


    def keypoints_dialog(self):
        """
        Creates a table with the present keypoints and their speed.
        """

        data_dict = self.speed_dict
        keypoints_main_dialog = QDialog()
        layout_dialog = QVBoxLayout()
        keypoints_main_dialog.setLayout(layout_dialog)
        table = QTableWidget()
        table.setRowCount(len(data_dict))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Keypoint", "Speed", "Action"])

        # define button
        btn_save_keypoint = QPushButton()
        btn_save_keypoint.setCheckable(False)
        btn_save_keypoint.setText('Save')

        for i, key in enumerate(data_dict):
            item_pos = QTableWidgetItem(str(key))
            item_vel = QTableWidgetItem(str(data_dict[key]))
            table.setItem(i, 0, item_pos)
            table.setItem(i, 1, item_vel)
            print(data_dict)
        #    btn_save_keypoint.clicked.connect(save_point(key, data_dict[key]))
            table.setCellWidget(i, 2, btn_save_keypoint)

        layout_dialog.addWidget(table)
        keypoints_main_dialog.exec_()


def cv2_to_QImage(cv2_frame):
    """
    Currently not used due to a bug in the cv2 installation?

    Parameters
    ----------
    cv2_frame : cv2.image array
        the cv2 frame

    Returns
    -------
    QImg : QImg type
        The QImage object to show
    """
    
    height, width = cv2_frame.shape
    bytesPerLine = 3 * width
    QImg = QImage(cv2_frame.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
    
    return QImg


def get_frame_from_video(path_to_video, frame_number):
    """
    Returns the chosen frame from a given video, given as a path.

    Parameters
    ----------
    path_to_video : str
        the video path.
    frame_number : int
        Number indicating the frame

    Returns
    -------
    frame : cv2.image
        The selected frame from the video.
    """
    
    video = cv2.VideoCapture(path_to_video)
    frame_counter = 1
    
    while True:
        ret, frame = video.read()
        
        if ret == False:
            break
        
       # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        if not ret:
            break
        
        if frame_counter == frame_number:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            break
    
        frame_counter = frame_counter + 1
    
    video.release()
  #  cv2.destroyAllWindows()
    
    return frame


def save_point(position, speed):
    column_names = ('Position', 'Velocity')
    final_ddbb = pd.DataFrame(columns = column_names)
    pd_speed = {'Position' : position, 'Speed' : speed}


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()