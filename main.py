import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import pushHelper as ph
import threading


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('教师端')
        self.resize(1355, 820)
        self.show()

        self.webview = QWebEngineView()
        self.webview.load(QUrl("http://localhost:8888"))

        # 使用QToolBar创建导航栏，并使用QAction创建按钮
        # 添加导航栏
        navigation_bar = QToolBar('Navigation')
        # 设定图标的大小
        navigation_bar.setIconSize(QSize(16, 16))
        # 添加导航栏到窗口中
        self.addToolBar(navigation_bar)
        self.setCentralWidget(self.webview)

        # QAction类提供了抽象的用户界面action，这些action可以被放置在窗口部件中
        # 添加前进、后退、停止加载和刷新的按钮
        back_button = QAction(QIcon('static/images/arrow-left-gray.png'), 'Back', self)
        next_button = QAction(QIcon('static/images/arrow-right.png'), 'Forward', self)
        stop_button = QAction(QIcon('static/images/close.png'), 'stop', self)
        reload_button = QAction(QIcon('static/images/retry-gray.png'), 'reload', self)

        # 绑定事件
        back_button.triggered.connect(self.webview.back)
        next_button.triggered.connect(self.webview.forward)
        stop_button.triggered.connect(self.webview.stop)
        reload_button.triggered.connect(self.webview.reload)

        # 将按钮添加到导航栏上
        navigation_bar.addAction(back_button)
        navigation_bar.addAction(next_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)

        # 添加URL地址栏
        self.urlbar = QLineEdit()
        # 让地址栏能响应回车按键信号
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)

        # 让浏览器相应url地址的变化
        self.webview.urlChanged.connect(self.renew_urlbar)

        self.fkbtn = QPushButton('打开白板',self)
        self.btn = QPushButton('开始推流',self)
        self.btn.clicked.connect(self.push)

        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.fkbtn)
        navigation_bar.addWidget(self.btn)
    
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.webview.setUrl(q)

    # 响应输入的地址
    def renew_urlbar(self, q):
        # 将当前网页的链接更新到地址栏
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def push(self):
        self.thread1 = myThread(1, "thread1", 1)
        self.thread2 = myThread(2, "thread2", 2)
        text = self.btn.text()
        if text == "开始推流":
            self.thread1.start()
            self.thread2.start()
        elif text == "暂停推流":
            self.thread1.join()
            self.thread2.join()
        self.btn.setText("暂停推流" if text == "开始推流" else "开始推流")

class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        if self.threadID == 1:
            ph.push(0)
        elif self.threadID == 2:
            ph.pushDesktop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 创建主窗口
    browser = MainWindow()
    browser.show()
    # 运行应用，并监听事件
    sys.exit(app.exec_())