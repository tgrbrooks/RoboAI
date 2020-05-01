import time

# pyqt imports
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QListWidget,
                             QGridLayout, QWidget, QTabWidget, QScrollArea,
                             QVBoxLayout, QSizePolicy, QComboBox, QLabel,
                             QLineEdit, QCheckBox)
from PyQt5.QtCore import QThreadPool, QTimer, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from display.videoworker import VideoWorker
from display.audiofigure import AudioFigure


class Label(QWidget):

    def __init__(self, text, col, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        label = QLabel(text)
        label.setStyleSheet(
            'font-size: 28pt; font-family: Courier; background-color: %s'
            % (col)
        )
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class ControlPanel(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Pi Control Panel'
        # Default dimensions
        self.left = 10
        self.top = 60
        self.width = 960
        self.height = 600
        self.threadpool = QThreadPool()
        self.counter = 0
        print('multithreading with maximum %d threads'
              % (self.threadpool.maxThreadCount()))
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        tabs = QTabWidget()

        default_font = 'font-size: 14pt; font-family: Courier;'
        big_font = 'font-size: 28pt; font-family: Courier;'

        #----------------------------------------------------------------------
        #                       MAIN TAB - ALL INFO
        #----------------------------------------------------------------------

        main_layout = QGridLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(20)

        # Video display
        main_layout.addWidget(Label('Video', 'red'), 0, 0, 4, 6)

        # Audio signal display
        main_layout.addWidget(Label('Audio', 'blue'), 0, 6, 2, 3)
        #audio_figure = AudioFigure(self, width=3, height=2)
        #main_layout.addWidget(audio_figure, 0, 6, 2, 3)

        # Accelerometer display
        main_layout.addWidget(Label('Accelerometer', 'green'), 2, 6, 2, 3)

        # Movement controls
        move_left_button = QPushButton('Left', self)
        move_left_button.setStyleSheet(default_font)
        main_layout.addWidget(move_left_button, 5, 6, 1, 1)

        move_forward_button = QPushButton('Forward', self)
        move_forward_button.setStyleSheet(default_font)
        main_layout.addWidget(move_forward_button, 4, 7, 1, 1)

        move_back_button = QPushButton('Back', self)
        move_back_button.setStyleSheet(default_font)
        main_layout.addWidget(move_back_button, 5, 7, 1, 1)

        move_right_button = QPushButton('Right', self)
        move_right_button.setStyleSheet(default_font)
        main_layout.addWidget(move_right_button, 5, 8, 1, 1)
 
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        tabs.addTab(main_widget, 'Main')

        #----------------------------------------------------------------------
        #                               VISION TAB
        #----------------------------------------------------------------------

        vision_layout = QGridLayout()
        vision_layout.setContentsMargins(0, 0, 0, 0)
        vision_layout.setSpacing(20)

        self.video = QLabel(self)
        self.video.resize(640, 480)
        video_worker = VideoWorker()
        video_worker.signals.change_pixmap.connect(self.set_image)
        video_worker.signals.finished.connect(self.thread_complete)
        self.threadpool.start(video_worker)
        vision_layout.addWidget(self.video, 0, 0)

        vision_widget = QWidget()
        vision_widget.setLayout(vision_layout)
        tabs.addTab(vision_widget, 'Vision')

        #----------------------------------------------------------------------
        #                               AUDIO TAB
        #----------------------------------------------------------------------

        audio_layout = QGridLayout()
        audio_layout.setContentsMargins(0, 0, 0, 0)
        audio_layout.setSpacing(20)

        audio_figure = AudioFigure(self)
        audio_layout.addWidget(audio_figure, 0, 0)

        audio_widget = QWidget()
        audio_widget.setLayout(audio_layout)
        tabs.addTab(audio_widget, 'Audio')

        #----------------------------------------------------------------------
        #                               MOVEMENT TAB
        #----------------------------------------------------------------------

        movement_layout = QGridLayout()
        movement_layout.setContentsMargins(0, 0, 0, 0)
        movement_layout.setSpacing(20)

        movement_widget = QWidget()
        movement_widget.setLayout(movement_layout)
        tabs.addTab(movement_widget, 'Movement')

        # Finish up by setting central widget and showing
        self.setCentralWidget(tabs)
        self.show()

    @pyqtSlot(QImage)
    def set_image(self, image):
        self.video.setPixmap(QPixmap.fromImage(image))

    def thread_complete(self):
        print("THREAD COMPLETE!")
