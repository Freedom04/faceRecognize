# faceRecognize

在Ubuntu上使用Qt和Python编写一个界面，可以使用PyQt5库。PyQt5是一个Python绑定Qt库的模块，可以方便地使用Python编写Qt应用程序。

以下是一个简单的示例代码，可以打开视频文件并播放：

```python
import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QAction, QFileDialog
import cv2


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def run(self):
        cap = cv2.VideoCapture(self.filename)
        while True:
            ret, frame = cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                p = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)
                self.change_pixmap_signal.emit(p)
            else:
                break
        cap.release()


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("视频播放器")
        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.video_label)

        open_action = QAction("打开", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        self.menuBar().addAction(open_action)

        self.thread = None

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "打开视频文件", "", "视频文件 (*.mp4 *.avi)")
        if filename:
            self.stop_video()
            self.thread = VideoThread(filename)
            self.thread.change_pixmap_signal.connect(self.set_image)
            self.thread.start()

    def set_image(self, image):
        self.video_label.setPixmap(QPixmap.fromImage(image))

    def stop_video(self):
        if self.thread is not None:
            self.thread.terminate()
            self.thread.wait()
            self.thread = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
```

在代码中，使用`QMainWindow`作为主窗口，并在窗口中添加一个`QLabel`控件用于显示视频。使用`QAction`添加一个打开文件的菜单项，可以选择视频文件进行播放。使用`VideoThread`类作为视频播放的线程，使用`cv2.VideoCapture`打开视频文件，读取视频帧并转换为`QImage`格式，通过`change_pixmap_signal`信号发送给主线程。在主线程中，使用`setPixmap`方法将`QImage`显示在`QLabel`控件中。在打开新的视频文件时，需要先停止原来的视频播放线程。

需要安装PyQt5和OpenCV库才能运行该程序，可以使用以下命令进行安装：

```
sudo apt-get install python3-pyqt5
sudo apt-get install python3-opencv
```

运行程序：

```
python3 video_player.py
```

注意：该程序只能播放本地视频文件，无法播放网络视频流。
