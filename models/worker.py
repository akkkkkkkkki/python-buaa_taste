import sys
import traceback

from PySide6.QtCore import QObject, QRunnable, Signal, Slot


class WorkerSignals(QObject):
    """
    定义正在运行的工作线程可用的信号。

    支持的信号包括：

    finished
        无数据

    error
        元组（异常类型，异常值，traceback.format_exc()）

    result
        处理返回的对象，任何类型的数据

    progress
        int 指示 % 进度

    """
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)


class Worker(QRunnable):
    """
    工作线程

    从 QRunnable 继承，用于处理工作线程的设置、信号和结束。

    :param callback: 在此工作线程上运行的函数回调。提供的 args 和 kwargs 将传递给 runner。
    :type callback: function
    :param args: 要传递给回调函数的参数
    :param kwargs: 要传递给回调函数的关键字参数

    """

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # 存储构造函数参数（用于后续处理）
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        """
        使用传递的args和kwargs初始化运行函数。
        """

        # 在这里检索args/kwargs；然后使用它们触发处理
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # 返回处理的结果
        finally:
            self.signals.finished.emit()  # 完成
