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



以下是一个示例代码，可以实现在Ubuntu上使用Qt和Python编写一个界面，能够打开视频并播放，并在界面上方显示选择的目录，下方显示当前目录下的文件：

```python
import os
import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QAction, QFileDialog, QTreeView, QSplitter
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

        # 显示选择的目录
        self.dir_label = QLabel(self)
        self.dir_label.setText("选择目录：")

        # 显示当前目录下的文件
        self.tree_view = QTreeView(self)
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setRootIsDecorated(False)

        # 使用QSplitter分割窗口
        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(self.dir_label)
        splitter1.addWidget(self.tree_view)

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(self.video_label)
        splitter2.addWidget(splitter1)

        self.setCentralWidget(splitter2)

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

        # 显示选择的目录和当前目录下的文件
        dir_path, _ = os.path.split(filename)
        self.dir_label.setText(f"选择目录：{dir_path}")
        self.show_files(dir_path)

    def set_image(self, image):
        self.video_label.setPixmap(QPixmap.fromImage(image))

    def stop_video(self):
        if self.thread is not None:
            self.thread.terminate()
            self.thread.wait()
            self.thread = None

    def show_files(self, path):
        self.tree_view.setModel(None)
        model = QStandardItemModel()
        self.tree_view.setModel(model)
        for filename in os.listdir(path):
            item = QStandardItem(filename)
            item.setEditable(False)
            item.setSelectable(True)
            item.setCheckable(False)
            item.setDragEnabled(False)
            item.setDropEnabled(False)
            model.appendRow(item)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
```

在代码中，使用`QSplitter`将窗口分成两部分，上方显示选择的目录，下方显示当前目录下的文件和视频播放器。在打开视频文件时，获取视频文件所在的目录，然后调用`show_files()`方法显示该目录下的文件。在`show_files()`方法中，使用`QStandardItemModel`创建一个数据模型，然后遍历目录下的文件，为每个文件创建一个`QStandardItem`对象，并添加到数据模型中。最后，将数据模型设置为`QTreeView`控件的模型。

需要安装PyQt5和OpenCV库才能运行该程序，可以使用以下命令进行安装：

```
sudo apt-get install python3-pyqt5
sudo apt-get install python3-opencv
```

运行程序：

```
python3 video_player.py
```

选择视频文件后，界面上方会显示该视频所在的目录，下方会显示该目录下的文件列表，同时播放器开始播放该视频。



以下是一个基本的界面，可以选择视频文件并播放：

```python
import os
import sys
import vlc
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QTreeView, QFileSystemModel, QSizePolicy

class Player(QMainWindow):
    def __init__(self, parent=None):
        super(Player, self).__init__(parent)
        self.setWindowTitle("Video Player")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(100, 100, 800, 600)
        self.media_player = None
        self.video_path = None
        self.init_ui()

    def init_ui(self):
        # 添加菜单栏
        open_action = self.create_action("&Open", self.open_file, "Ctrl+O", "Open video file")
        exit_action = self.create_action("&Exit", self.exit_app, "Ctrl+Q", "Exit application")
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # 添加视频播放区域
        self.media_player = vlc.MediaPlayer()
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.media_player.set_xwindow(self.centralWidget().winId())
        elif sys.platform == "win32": # for Windows
            self.media_player.set_hwnd(self.centralWidget().winId())
        elif sys.platform == "darwin": # for MacOS
            self.media_player.set_nsobject(int(self.centralWidget().winId()))

        # 添加文件浏览器
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath('')
        self.file_tree = QTreeView()
        self.file_tree.setModel(self.file_model)
        self.file_tree.setRootIndex(self.file_model.index(os.path.expanduser('~')))
        self.file_tree.clicked.connect(self.file_clicked)

        # 添加主窗口布局
        self.setCentralWidget(self.file_tree)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def create_action(self, text, slot=None, shortcut=None, tooltip=None, icon=None):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tooltip is not None:
            action.setToolTip(tooltip)
            action.setStatusTip(tooltip)
        if slot is not None:
            action.triggered.connect(slot)
        return action

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video", os.path.expanduser('~'))
        if file_path != '':
            self.video_path = file_path
            self.media_player.set_media(vlc.Media(self.video_path))
            self.media_player.play()

    def file_clicked(self, index):
        path = self.file_model.filePath(index)
        if os.path.isfile(path):
            self.video_path = path
            self.media_player.set_media(vlc.Media(self.video_path))
            self.media_player.play()

    def exit_app(self):
        self.media_player.stop()
        sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = Player()
    player.show()
    sys.exit(app.exec_())
```

这个界面使用了VLC播放器作为视频播放的后端，并使用PyQt5实现了一个简单的文件浏览器。在初始化UI时，我们设置了主窗口的大小为800x600，并将文件浏览器放在了主窗口的中心。在菜单栏中，我们添加了一个“Open”按钮，点击它可以选择要播放的视频文件。在文件浏览器中，当用户双击一个视频文件时，它将被播放。
