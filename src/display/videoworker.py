import traceback
import sys

from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot


class VideoWorkerSignals(QObject):

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class VideoWorker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(VideoWorker, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = VideoWorkerSignals()

        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
