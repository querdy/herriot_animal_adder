import inspect
import sys
import time
import traceback

from PyQt6.QtCore import pyqtSignal, pyqtSlot, QRunnable, QObject, QMutexLocker, QMutex


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(str)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.mutex = QMutex()
        self.is_stop = False
        if 'progress_callback' in inspect.getfullargspec(self.fn).args:
            self.kwargs["progress_callback"] = self.signals.progress
        if 'worker_object' in inspect.getfullargspec(self.fn).args:
            self.kwargs["worker_object"] = self

    @pyqtSlot()
    def run(self):
        try:
            with QMutexLocker(self.mutex):
                self.is_stop = False
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()

    # @pyqtSlot()
    def stop(self):
        with QMutexLocker(self.mutex):
            self.is_stop = True
