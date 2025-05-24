import sys

import pandas as pd
from PySide6.QtCore import QThread, Signal, Qt, QTimer, QCoreApplication, QObject, QEvent, Slot
from PySide6.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem,
                               QFileDialog, QMessageBox)

from config_set import config_instance
from ui_general_excel import Ui_MainWindow


class Worker(QObject):
    """通用工作线程类，用于在后台执行耗时操作"""

    finished = Signal(object)  # 操作完成信号，携带结果
    error = Signal(tuple)  # 错误信号，携带异常类型和异常信息
    progress = Signal(int)  # 进度信号，携带进度值(0-100)

    def __init__(self, func, *args, **kwargs):
        """
        初始化工作线程

        参数:
            func: 要在后台执行的函数
            *args: 传递给函数的位置参数
            **kwargs: 传递给函数的关键字参数
        """
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        # 检查函数是否支持进度回调
        if 'progress_callback' not in self.func.__code__.co_varnames:
            self.kwargs.pop('progress_callback', None)
        else:
            self.kwargs['progress_callback'] = self.progress_callback

    @Slot()
    def run(self):
        """执行工作函数，处理结果和异常"""
        try:
            result = self.func(*self.args, **self.kwargs)
        except Exception as e:
            # 发送错误信号
            self.error.emit((type(e), str(e)))
        else:
            # 发送完成信号和结果
            self.finished.emit(result)

    def progress_callback(self, value):
        """进度回调函数，用于发送进度信号"""
        self.progress.emit(value)


'''
if hasattr(self, 'thread') and self.thread.isRunning():
            return
            
self.thread = QThread()
self.worker = Worker(long_running_task, 10)  # 执行10秒的任务

self.worker.progress.connect(self.update_progress)
self.worker.finished.connect(self.task_finished)
self.worker.error.connect(self.task_error)

# 线程管理
self.thread.started.connect(self.worker.run)
self.worker.finished.connect(self.thread.quit)
self.worker.finished.connect(self.worker.deleteLater)
self.thread.finished.connect(self.thread.deleteLater)

self.thread.start()
'''


class ExcelLoaderThread(QThread):
    """Excel文件加载线程"""
    preview_ready = Signal(pd.DataFrame)  # 预览数据就绪信号
    full_data_ready = Signal(pd.DataFrame)  # 完整数据就绪信号
    error = Signal(str)  # 错误信号

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        """线程执行的主要任务"""
        try:
            # 读取前20行作为预览数据
            preview_df = pd.read_excel(self.file_path, nrows=20)
            self.preview_ready.emit(preview_df)

            # 读取完整数据
            full_df = pd.read_excel(self.file_path)
            self.full_data_ready.emit(full_df)
        except Exception as e:
            self.error.emit(str(e))


class EnterKeyFilter(QObject):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return:
            # 获取当前文本内容
            text = obj.toPlainText()
            # 调用回调函数处理文本
            self.callback(text)
            return True  # 拦截事件，不插入换行
        return super().eventFilter(obj, event)


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.thread = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)

        # 初始化变量
        self.excel_thread = None
        self.df = None
        self.loading_timer = None
        self.batch_size = 500  # 每批处理行数
        self.current_row = 0
        self.is_preview = True  # 是否处于预览状态

        # **新增：设置状态栏样式表（全局修改颜色）**
        self.statusBar().setStyleSheet("""
                           QStatusBar {
                               color: red;        /* 红色字体 */
                               font-weight: bold; /* 加粗 */
                           }
                       """)
        # 加载上次的文件
        last_path = config_instance.get('last_opened_file', None)
        if last_path:
            self.open_file(last_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            if event.mimeData().urls()[0].toLocalFile().lower().endswith(('.xlsx', '.xls')):
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.open_file(file_path)
            event.acceptProposedAction()
        else:
            event.ignore()

    def open_file(self, file_path=None):
        """打开Excel文件，支持拖放和手动选择"""
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "选择Excel文件", "", "Excel Files (*.xlsx *.xls)"
            )

        if file_path:
            # 清空表格
            self.ui.tableWidget.setRowCount(0)
            self.ui.tableWidget.setColumnCount(0)

            # 显示加载中状态
            self.statusBar().showMessage("正在加载文件...", 0)

            # 创建并启动Excel加载线程
            self.excel_thread = ExcelLoaderThread(file_path)
            self.excel_thread.preview_ready.connect(self._show_preview)
            self.excel_thread.full_data_ready.connect(self._on_full_data_ready)
            self.excel_thread.error.connect(lambda msg: self._show_error(f"读取失败: {msg}"))
            self.excel_thread.start()

    def _show_preview(self, preview_df):
        """显示数据预览"""
        self.df = preview_df
        self.is_preview = True

        # 在状态栏显示预览提示
        self.statusBar().showMessage("数据预览中（前20行），正在加载完整数据...", 0)

        # 设置表格结构并加载预览数据
        table = self.ui.tableWidget
        table.setRowCount(preview_df.shape[0])
        table.setColumnCount(preview_df.shape[1])
        table.setHorizontalHeaderLabels(list(preview_df.columns))

        self._load_data_batch(preview_df)
        table.resizeColumnsToContents()

    def _on_full_data_ready(self, full_df):
        """完整数据就绪后的处理"""
        self.df = full_df
        self.current_row = 20  # 从第20行开始加载
        self.is_preview = False

        # 更新状态栏消息
        total_rows = full_df.shape[0]
        self.statusBar().showMessage(f"正在加载完整数据（共{total_rows}行）", 0)

        # 更新表格行数为完整数据行数
        self.ui.tableWidget.setRowCount(full_df.shape[0])

        # 使用定时器分批次加载剩余数据
        self.loading_timer = QTimer()
        self.loading_timer.timeout.connect(self._load_next_batch)
        self.loading_timer.start(10)  # 每10ms处理一批

    def _load_data_batch(self, df, start_row=0, end_row=None):
        """加载指定范围的数据到表格"""
        if end_row is None:
            end_row = df.shape[0]

        table = self.ui.tableWidget

        for row in range(start_row, end_row):
            for col in range(df.shape[1]):
                value = df.iloc[row, col]
                item = QTableWidgetItem(str(value) if pd.notna(value) else "")

                if isinstance(value, (int, float)):
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                elif isinstance(value, pd.Timestamp):
                    item.setText(value.strftime("%Y-%m-%d %H:%M:%S"))

                table.setItem(row, col, item)

                # **关键优化：每处理50行释放一次事件循环（避免长时间阻塞UI）**
                if (row - start_row) % 50 == 0:
                    QCoreApplication.processEvents()  # 主动释放控制权，刷新UI

    def _load_next_batch(self):
        """分批次加载剩余数据"""
        if self.current_row >= self.df.shape[0]:
            self.loading_timer.stop()
            self.ui.tableWidget.resizeColumnsToContents()

            # 更新状态栏为加载完成
            total_rows = self.df.shape[0]
            self.statusBar().showMessage(f"数据加载完成（共{total_rows}行）", 5000)

            # 保存文件路径
            config_instance.update({
                'last_opened_file': self.excel_thread.file_path
            })
            config_instance.save()
            self.excel_thread = None
            return

        end_row = min(self.current_row + self.batch_size, self.df.shape[0])
        self._load_data_batch(self.df, self.current_row, end_row)

        # 更新状态栏显示加载进度
        progress = f"{self.current_row}/{self.df.shape[0]}"
        self.statusBar().showMessage(f"正在加载: {progress}", 0)
        self.current_row = end_row

    def _show_error(self, message):
        """显示错误消息并清理资源"""
        self.statusBar().clearMessage()
        QMessageBox.critical(self, "错误", message)
        if self.excel_thread:
            self.excel_thread = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())
