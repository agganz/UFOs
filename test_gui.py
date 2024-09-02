# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 16:44:13 2023

@author: Alejandro Gonzalez Ganzabal


ChangeLog

    0.1 (AG): First version (GIT)
    0.2 (AG): Added pulse search; changed function arguments.
    0.2.1 (AG): Still on progress - noow it shows the frames
    0.2.2 (AG): almost functional.
    0.2.3 (AG): working up to selecting keypoints. This might take a while.
    0.2.4 (AG): LOOOTS of fixes.
    0.2.5 (AG): several crashes fixed, and image info is now
        available. Also fixed the issue with the tables.
    0.3 (AG): now contrast and brightness can be enhanced.
    0.3.1 (AG): fixed the issue with the duplicated labels.
    0.3.2 (AG): added stad deviation.
    0.3.3 (AG): added buttom to restart speed measures.
    0.4 (AG): added scale factor for time. 
        Added several shortcut and the possibility to save the images.
"""

import sys
import cv2
import os
import numpy as np
import re
import fast_camera_detection
from aux_tools import misc_tools
from aux_tools import simple_image_editor

# QT5 stuff
from PyQt5.QtGui import QPixmap, QImage, QKeySequence
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
    QShortcut,
    QLineEdit,
    QVBoxLayout,
    QCheckBox,
    QPushButton
)


class MainWindow(QMainWindow):
    """
    Will define the whole GUI except some table data and the error messages.
    Those are handled separately but in the same class. Don't see the point of 
    creating dedicated classes for just that.
    """

    def __init__(self):
        super().__init__()

        self.velocities_selected = []
        self.velocity = 0.0
        self.error_velocity = 0.0
        self.save_counter = 0

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

        self.time_scale_factor = QLineEdit()
        self.conf_image_layout.addRow("Time scale factor (m/pixel):", self.time_scale_factor)
        self.time_scale_factor.setText('1.0')


        self.contrast_and_brightness = QLineEdit()
        self.conf_image_layout.addRow('Enhance image as contrast-brightness:', self.contrast_and_brightness)
        self.contrast_and_brightness.setText('1-0')

        self.btn_keypoints = QPushButton()
        self.btn_keypoints.setCheckable(False)
        self.btn_keypoints.setText('Open keypoints dialog')
        self.btn_keypoints.clicked.connect(self.keypoints_dialog)
        
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
        
        
        self.set_shortcuts()


    def set_shortcuts(self):
        """
        Sets the shortcuts for the buttons.
        """
        
        self.shortcut_next = QShortcut(QKeySequence('Ctrl+D'), self)
        self.shortcut_next.activated.connect(self.go_next)
        self.shortcut_prev = QShortcut(QKeySequence('Ctrl+A'), self)
        self.shortcut_prev.activated.connect(self.go_prev)

        self.shortcut_save_left = QShortcut(QKeySequence('Ctrl+L'), self)
        self.shortcut_save_left.activated.connect(self.save_left_image)
        self.shortcut_save_right = QShortcut(QKeySequence('Ctrl+R'), self)
        self.shortcut_save_right.activated.connect(self.save_right_image)


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
        
        try:
            gray_1 = get_frame_from_video(video_name_str, frame_number_int)
            gray_2 = get_frame_from_video(video_name_str, 1 + frame_number_int)
        except IndexError:
            self.show_error_message('The video does not have enough frames. Getting second to last frame')
            max_frames = get_max_frames_from_video(video_name_str)
            frame_number_int = max_frames - 1
            self.frame_number.setText(str(frame_number_int))
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
            

        text_enhance = self.contrast_and_brightness.text()
        extra_contrast, extra_brightness = re.findall(r"[+]?(?:\d*\.*\d+)", text_enhance)
        extra_contrast = float(extra_contrast)
        extra_brightness = int(extra_brightness)
        
        gray_1 = simple_image_editor.increase_contrast_brightness_gray(gray_1, extra_contrast, extra_brightness)
        gray_2 = simple_image_editor.increase_contrast_brightness_gray(gray_2, extra_contrast, extra_brightness)
        self.frame_1_cv2 = fast_camera_detection.adjust_frame(gray_1, canny_al = use_canny, median_al = use_median, LoG = use_LoG, min_bkg = min_bkg_im, thresholding = use_threshold, div_mask_limits = None)
        self.frame_2_cv2 = fast_camera_detection.adjust_frame(gray_2, canny_al = use_canny, median_al = use_median, LoG = use_LoG, min_bkg = min_bkg_im, thresholding = use_threshold, div_mask_limits = None)
        
        misc_tools.save_frame('.', 1, self.frame_1_cv2)
        misc_tools.save_frame('.', 2, self.frame_2_cv2)

        self.mean_frame_1 = np.mean(self.frame_1_cv2)
        self.mean_frame_2 = np.mean(self.frame_2_cv2)
        self.std_frame_1 = np.std(self.frame_1_cv2)
        self.std_frame_2 = np.std(self.frame_2_cv2)

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
        

        msg_1 = 'Mean: {0}. Std. dev: {1}'.format(round(self.mean_frame_1, 2), round(self.std_frame_1, 2))
        self.im_info_1 = QLabel(msg_1, self)
        self.im_info_1.setText(msg_1)
        if not 'added_1' in self.__dict__.keys():
            self.main_layout.addWidget(self.im_info_1, 1, 1)
            self.added_1 = True

        msg_2 = 'Mean: {0}. Std. dev: {1}'.format(round(self.mean_frame_2, 2), round(self.std_frame_2, 2))
        self.im_info_2 = QLabel(msg_2, self) 
        self.im_info_2.setText(msg_2)
        if not 'added_2' in self.__dict__.keys():
            self.main_layout.addWidget(self.im_info_2, 1, 2)
            self.added_2 = True
            
        # Save the images for the detection
        self.btn_save_left_frame = QPushButton()
        self.btn_save_left_frame.setCheckable(False)
        self.btn_save_left_frame.setText('Save frame')
        self.btn_save_left_frame.clicked.connect(self.save_left_image)

        self.btn_save_right_frame = QPushButton()
        self.btn_save_right_frame.setCheckable(False)
        self.btn_save_right_frame.setText('Save frame')
        self.btn_save_right_frame.clicked.connect(self.save_right_image)

        self.main_layout.addWidget(self.btn_save_left_frame, 2, 1)
        self.main_layout.addWidget(self.btn_save_right_frame, 2, 2)

        # Go to next frame
        self.btn_nextframe = QPushButton()
        self.btn_nextframe.setCheckable(False)
        self.btn_nextframe.setText('Next frame')
        self.btn_nextframe.clicked.connect(self.go_next)
        self.main_layout.addWidget(self.btn_nextframe, 3, 2)

        # Previous frame
        self.btn_prevframe = QPushButton()
        self.btn_prevframe.setCheckable(False)
        self.btn_prevframe.setText('Previous frame')
        self.btn_prevframe.clicked.connect(self.go_prev)
        self.main_layout.addWidget(self.btn_prevframe, 3, 1)
        

        self.btn_keypoints = QPushButton()
        self.btn_keypoints.setCheckable(False)
        self.btn_keypoints.setText('Open keypoints dialog')
        self.btn_keypoints.clicked.connect(self.keypoints_dialog)
        
        self.btn_speed_to_zero = QPushButton()
        self.btn_speed_to_zero.setCheckable(False)
        self.btn_speed_to_zero.setText('Set speed to zero')
        self.btn_speed_to_zero.clicked.connect(self.set_speed_to_zero)

        self.vel_display = QLineEdit()
        self.vel_display.setText('Mean speed: ' + str(self.velocity))
        # TODO quick fix to add label
        self.vel_display.setReadOnly(True)
        self.main_layout.addWidget(self.vel_display, 4, 1)
        
        self.err_display = QLineEdit()
        self.err_display.setText('Speed deviation: ' + str(self.error_velocity))
        self.err_display.setReadOnly(True)
        self.main_layout.addWidget(self.err_display, 4, 2)

        self.main_layout.addWidget(self.btn_speed_to_zero, 3, 3)
        self.main_layout.addWidget(self.btn_keypoints, 2, 3)

        if self.auto_detect.isChecked():
            self.make_detection()
        

    def set_speed_to_zero(self):
        """
        Sets the speed to zero.
        """
        
        self.velocity = 0.0
        self.error_velocity = 0.0
        self.vel_display.setText('Mean speed: ' + str(self.velocity))
        self.err_display.setText('Speed deviation: ' + str(self.error_velocity))


    def estimate_delta_time(self):
        """
        Estimates the value for the delta time using functions from jet2video.
        """

        try:
            import jet2video
        except ModuleNotFoundError:
            self.show_error_message('Needs to be on a Heimdall machine to execute this. Also check the Pythonpath. You might want to run start_py_juvil.sh.')
            return None
        
        camera, pulse = misc_tools.get_camera_pulse(self.video_filename)

        if camera is None or pulse is None:
            self.show_error_message('Could not find a proper delta time with the video filename.')
            return None
        else:
            est_delta_time = jet2video.get_framerate(camera, pulse)
            self.delta_time_box.setText(str(est_delta_time))
            return est_delta_time
        

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
        self.im_with_keypoints_B = cv2.drawKeypoints(self.frame_2_cv2, keypoints_B, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        try:
            delta_time = float(self.delta_time_box.text())
        except ValueError:
            self.show_error_message('Could not read delta time. Will try to estimate..')
            try:
                est_delta_time = self.estimate_delta_time()
            except:
                est_delta_time = 30
            if est_delta_time is None:
                est_delta_time = 30

            self.delta_time_box.setText(str(est_delta_time))
            delta_time = float(self.delta_time_box.text())

        try:
            scale_factor = float(self.time_scale_factor.text())
        except ValueError:
            self.show_error_message('Could not read scale factor. Will set to 1.0')
            scale_factor = 1.0

        delta_time = delta_time * scale_factor # scale factor in m/pixel

        if len(keypoints_A) != 0 and len(keypoints_B) != 0:
            (start_points, end_points) = fast_camera_detection.filter_points_with_distance_matrix(keypoints_B, keypoints_A, threshold = 100, check_brightness = 0, frame_A = self.frame_2_cv2, frame_B = self.frame_1_cv2)
            if start_points is None:
                pass
            else:
                self.im_with_keypoints_B, self.speed_dict = fast_camera_detection.draw_arrow_in_frame(self.im_with_keypoints_B, start_points, end_points, frame_number = None, time_vec = None, delta_time = delta_time)
            
        self.refresh_image_detection()
        
        
    def refresh_image_detection(self):
        """
        Refresh the current images with new inputs after the detection.
        """
        
        misc_tools.save_frame('.', 1, self.im_with_keypoints_A)
        misc_tools.save_frame('.', 2, self.im_with_keypoints_B)

        self.frame_1 = '1.png'
        self.frame_2 = '2.png'
            
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
        video_basename = os.path.basename(path[0])
        self.video_btn.setText('Current file: {0}'.format(video_basename))


    def show_error_message(self, message):
        """
        Shows an error message instead of crashing (I hope?)
        TODO: try to force it out of the class broadcasting lambda functiions.
        This is working well tho

        Parameters:
        ----------
        message : str
            The message to be displayed.
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

        try:
            data_dict = self.speed_dict
        except AttributeError:
            self.show_error_message('There are no keypoints available.')
            data_dict = dict()

        keypoints_main_dialog = QDialog()
        keypoints_main_dialog.setWindowTitle('JUUT - Keypoints')
        layout_dialog = QVBoxLayout()
        keypoints_main_dialog.setLayout(layout_dialog)

        self.table = QTableWidget()
        self.table.setRowCount(len(data_dict))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Keypoint", "Speed (pix/s)"])

        for i, key in enumerate(data_dict):
            item_pos = QTableWidgetItem(str(key))
            item_vel = QTableWidgetItem(str(data_dict[key]))
            self.table.setItem(i, 0, item_pos)
            self.table.setItem(i, 1, item_vel)
            
        self.table.cellClicked.connect(self.cellClick)

        layout_dialog.addWidget(self.table)
        keypoints_main_dialog.exec_()


    def cellClick(self, row, col):
        """
        Get's the row and column number of the clicked cell.
        Will also save the clicked data into a pandas dataframe.

        Technically it's got more inputs, but those are gathered 
        from the cellclicked signal. 
        """

        self.row = row
        self.col = col
        self.save_point()


    def save_point(self):
        """
        Once a cell is selected, it will save both the position and
        the velocity into a pandas dataframe.
        """
        
        position = self.table.item(self.row, 0).text()
        pos_tuple = re.findall('\d+', position)
        position = (int(pos_tuple[0]), int(pos_tuple[1]))
        velocity = float(self.table.item(self.row, 1).text())
        self.velocities_selected.append(velocity)
        self.velocity = np.mean(self.velocities_selected)
        self.error_velocity = np.std(self.velocities_selected)
        self.vel_display.setText(str(self.velocity))
        self.err_display.setText(str(self.error_velocity))


    def save_left_image(self):
        """
        Saves the left image.
        """
        
        self.save_counter = self.save_counter + 1
        file_name = 's_{0}'.format(self.save_counter)
        misc_tools.save_frame('.', file_name, self.frame_1_cv2)


    def save_right_image(self):
        """
        Saves the right image.
        """
        
        self.save_counter = self.save_counter + 1
        file_name = 's_{0}'.format(self.save_counter)
        misc_tools.save_frame('.', file_name, self.frame_2_cv2)


def cv2_to_QImage(cv2_frame):
    """
    Currently not used due to a bug in the cv2 installation?
    Might be moved to aux code for the GUI, as this here is useless.

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


def get_max_frames_from_video(path_to_video):
    """
    Returns the total number of frames in the video.

    Parameters
    ----------
    path_to_video : str
        The path to the video.

    outputs
    -------
    frame_counter : int
        The total number of frames.
    """

    video = cv2.VideoCapture(path_to_video)
    frame_counter = 0
    
    # this is probably slower than the built-in cv2.CAP_PROP_FRAME_COUNT but seems way more reliable
    while True:
        ret, _ = video.read()
        
        if not ret:
            break
    
        frame_counter = frame_counter + 1
    
    video.release()
    return frame_counter


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
        
        if not ret:
            video.release()
            #  cv2.destroyAllWindows() # I have no idea why this works sometimes but hell if I care - it's out

            raise IndexError
        
        if frame_counter == frame_number:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            video.release()
             #  cv2.destroyAllWindows()
            return frame
    
        frame_counter = frame_counter + 1

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
