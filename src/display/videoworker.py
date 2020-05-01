import traceback
import sys
import cv2

from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QImage, QPixmap


class VideoWorkerSignals(QObject):

    change_pixmap = pyqtSignal(QImage)
    error = pyqtSignal(tuple)
    finished = pyqtSignal()


class VideoWorker(QRunnable):

    def __init__(self, *args, **kwargs):
        super(VideoWorker, self).__init__()

        self.args = args
        self.kwargs = kwargs
        self.signals = VideoWorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                if ret:
                    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    if sys.platform == 'linux':
                        rgb_image = cv2.rotate(rgb_image, cv2.ROTATE_180)
                    h, w, ch = rgb_image.shape
                    bytes_per_line = ch * w
                    qt_image = QImage(rgb_image.data, w, h,
                                      bytes_per_line,
                                      QImage.Format_RGB888)
                    pixmap = qt_image.scaled(640, 480,
                                             Qt.KeepAspectRatio)
                    self.signals.change_pixmap.emit(pixmap)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()
