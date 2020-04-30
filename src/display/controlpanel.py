import time

# pyqt imports
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QListWidget,
                             QGridLayout, QWidget, QTabWidget, QScrollArea,
                             QVBoxLayout, QSizePolicy, QComboBox, QLabel,
                             QLineEdit, QCheckBox)
from PyQt5.QtCore import QThreadPool, QTimer

from display.videoworker import VideoWorker


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

        self.label = QLabel('Start')
        main_layout.addWidget(self.label, 4, 0)
        button = QPushButton('DANGER!')
        button.clicked.connect(self.oh_no)
        main_layout.addWidget(button, 4, 1)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        tabs.addTab(main_widget, 'Main')

        #----------------------------------------------------------------------
        #                               VISION TAB
        #----------------------------------------------------------------------

        vision_layout = QGridLayout()
        vision_layout.setContentsMargins(0,0,0,0)
        vision_layout.setSpacing(20)

        vision_widget = QWidget()
        vision_widget.setLayout(vision_layout)
        tabs.addTab(vision_widget, 'Vision')

        #----------------------------------------------------------------------
        #                               AUDIO TAB
        #----------------------------------------------------------------------

        audio_layout = QGridLayout()
        audio_layout.setContentsMargins(0,0,0,0)
        audio_layout.setSpacing(20)

        audio_widget = QWidget()
        audio_widget.setLayout(audio_layout)
        tabs.addTab(audio_widget, 'Audio')

        #----------------------------------------------------------------------
        #                               MOVEMENT TAB
        #----------------------------------------------------------------------

        movement_layout = QGridLayout()
        movement_layout.setContentsMargins(0,0,0,0)
        movement_layout.setSpacing(20)

        movement_widget = QWidget()
        movement_widget.setLayout(movement_layout)
        tabs.addTab(movement_widget, 'Movement')

        # Finish up by setting central widget and showing
        self.setCentralWidget(tabs)
        self.show()

    def progress_fn(self, n):
        print('%d done' % n)

    def execute_this_fn(self, progress_callback):
        for n in range(0, 5):
            time.sleep(1)
            progress_callback.emit(n*100/4)

        return "Done."

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def oh_no(self):
        # Pass the function to execute
        worker = VideoWorker(self.execute_this_fn)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker) 

    def recurring_timer(self):
        self.counter +=1
        self.label.setText("Counter: %d" % self.counter)
