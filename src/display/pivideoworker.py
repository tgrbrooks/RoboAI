import traceback
import sys
import cv2
import time

from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QImage, QPixmap

from picamera.array import PiRGBArray
from picamera import PiCamera


class PiVideoWorkerSignals(QObject):

    change_pixmap = pyqtSignal(QImage)
    error = pyqtSignal(tuple)
    finished = pyqtSignal()


class PiVideoWorker(QRunnable):

    def __init__(self, *args, **kwargs):
        super(PiVideoWorker, self).__init__()

        self.args = args
        self.kwargs = kwargs
        self.signals = PiVideoWorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            camera = PiCamera()
            # Gotta be careful with this, too much data can cause a segfault
            # Reduce framerate, resolution or go to grayscale to prevent
            camera.resolution = (320, 240)
            camera.framerate = 16
            rawCapture = PiRGBArray(camera, size=(320, 240))

            time.sleep(0.1)
            for frame in camera.capture_continuous(rawCapture,
                                                   format="bgr",
                                                   use_video_port=True):
                image = frame.array
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                rgb_image = cv2.rotate(rgb_image, cv2.ROTATE_180)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h,
                                  bytes_per_line,
                                  QImage.Format_RGB888)
                pixmap = qt_image.scaled(640, 480,
                                         Qt.KeepAspectRatio)
                self.signals.change_pixmap.emit(pixmap)
                rawCapture.truncate(0)
                rawCapture.seek(0)
        except Exception:
            print('exception')
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()
