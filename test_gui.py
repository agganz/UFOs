import sys
import cv2
import os
import fast_camera_detection
from aux_tools import misc_tools

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (

    QApplication,

    QDialog,
    
    QLabel,
    
    QGridLayout,
    
    QFileDialog,

    QDialogButtonBox,
    
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
        self.video_btn.setCheckable(True)
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
        
        self.min_bkg_image = QLineEdit()
        self.conf_image_layout.addRow("Minimum background for the Canny algorithm::", self.min_bkg_image)


        # Image
        self.frame_1 = None
        self.frame_2 = None
        
        
        # Add a button box
        self.btnBox = QPushButton()
        self.btnBox.setCheckable(True)
        self.btnBox.setText('Get frame')
        self.btnBox.clicked.connect(self.get_image_when_clicked)


        
        self.frame_1_layout = QVBoxLayout()
        self.frame_2_layout = QVBoxLayout()
        
        self.label_pix_1 = QLabel()
        #self.pixmap_1 = QPixmap(self.frame_1)
        #self.label_pix_1.setPixmap(self.pixmap_1)
       # self.frame_1_layout.addWidget(self.label_pix_1)
        
        self.label_pix_2 = QLabel()
        #self.pixmap_2 = QPixmap(self.frame_2)
        #self.label_pix_2.setPixmap(self.pixmap_2)
        #self.frame_2_layout.addWidget(self.label_pix_2)

        # Set the layout on the dialog
        self.main_layout.addLayout(self.conf_image_layout, 0, 0)
        self.main_layout.addWidget(self.btnBox, 1, 0)
        self.main_layout.addLayout(self.frame_1_layout, 0, 1)
        self.main_layout.addLayout(self.frame_2_layout, 0, 2)


        self.setLayout(self.main_layout)        
        self.container = QWidget()
        self.container.setLayout(self.main_layout)
        self.setCentralWidget(self.container)
        
        
    def get_image_when_clicked(self):
        """
        


        """
        
        video_name_str = self.video_filename
        frame_number_int = int(self.frame_number.text())
    
        if not os.path.isfile(video_name_str):
            raise FileNotFoundError('Could not locate the video file in the given path ({0})'.format(video_name_str))
        
        gray_1 = get_frame_from_video(video_name_str, frame_number_int)
        gray_2 = get_frame_from_video(video_name_str, 1 + frame_number_int)

        use_median = self.median_filt.isChecked()
        use_canny = self.canny_al.isChecked()
        min_bkg_im = int(self.min_bkg_image.text())
        print('todo ok')
        frame_1_cv2 = fast_camera_detection.adjust_frame(gray_1, canny_al = use_canny, median_al = use_median, min_bkg = min_bkg_im, div_mask_limits = None)
        print('todo ok 2')
        frame_2_cv2 = fast_camera_detection.adjust_frame(gray_2, canny_al = use_canny, median_al = use_median, min_bkg = min_bkg_im, div_mask_limits = None)


        self.frame_1 = cv2_to_QImage(frame_1_cv2)
    
    
    def get_video_filename(self):
        """
        Opens the file browser and updates the video file path, updated in 
        self.video_filename.
        """
        
        path = QFileDialog.getOpenFileName()
        self.video_filename = path[0]
                
        
def cv2_to_QImage(cv2_frame):
    height, width = cv2_frame.shape
    bytesPerLine = 3 * width
    print('todo ok 3')
    QImg = QImage(cv2_frame.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
    print('todo ok 4')
    return QImg


def get_frame_from_video(path_to_video, frame_number):
    """
    

    Parameters
    ----------
    path_to_video : TYPE
        DESCRIPTION.
    frame_number : TYPE
        DESCRIPTION.

    Returns
    -------
    frame : TYPE
        DESCRIPTION.
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


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()