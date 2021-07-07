import sys
from PyQt5.QtWidgets import QWidget, QComboBox, QApplication, QLabel, QPushButton, QRadioButton, QButtonGroup
from PyQt5.QtCore import QSettings, Qt
import match_devices as md


class ComboxDemo(QWidget):
    def __init__(self):
        super().__init__()

        self.info = []

        # 设置标题
        self.setWindowTitle('推流设置')
        # 设置初始界面大小
        self.resize(1000, 400)

        # 实例化QComBox对象
        self.lb1 = QLabel('请选择视频设备：',self)
        self.lb1.move(100, 40)
        self.cb = QComboBox(self)
        self.cb.move(100, 70)

        self.lb2 = QLabel('请选择音频设备：',self)
        self.lb2.move(100, 120)
        self.cb1 = QComboBox(self)
        self.cb1.move(100, 150)

        self.lb3 = QLabel('请选择主屏内容：',self)
        self.lb3.move(100, 200)
        self.bg = QButtonGroup(self)
        self.rb1 = QRadioButton('屏幕录制',self)
        self.rb1.move(100, 230)
        self.rb2 = QRadioButton('白板',self)
        self.rb2.move(300, 230)
        self.rb1.setChecked(True)  # 默认选中屏幕录制


        data = md.match_devices()
        self.info.append(data[0][0])  # 默认视频设备
        self.info.append(data[1][0])  # 默认音频设备
        self.info.append("1")  # 默认屏幕录制

        # 添加条目
        self.cb.addItems(data[0])
        self.cb1.addItems(data[1])
        self.bg.addButton(self.rb1, 1)
        self.bg.addButton(self.rb2, 2)

        # 添加响应
        self.bg.buttonClicked.connect(self.clicked)
        self.bt2 = QPushButton('确定',self)
        self.bt2.move(100, 280)
        self.bt2.clicked.connect(self.submit)

        # 信号
        self.cb.currentIndexChanged[str].connect(self.modify_video_device) # 条目发生改变，发射信号，传递条目内容
        self.cb1.currentIndexChanged[str].connect(self.modify_audio_device)

        # 窗口置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def print_value(self, i):
        print(i)
    
    def modify_video_device(self, i):
        self.info[0] = i

    def modify_audio_device(self, i):
        self.info[1] = i

    def clicked(self):
        if self.bg.checkedId() == 1:
            self.info[2] = '1'
        elif self.bg.checkedId() == 2:
            self.info[2] = '2'

    def submit(self):
        settings = QSettings("config.ini", QSettings.IniFormat)
        settings.setIniCodec('utf-8')  # 修改编码方式！！！！
        settings.setValue("video", self.info[0])
        settings.setValue("audio", self.info[1])
        settings.setValue("sub_screen", self.info[2])

        # if self.bt2.isEnabled():
        #     self.bt2.setEnabled(False)
        #     self.bt2.setText('已推流')
        
        # print("video:{}\taudio:{}\tsub screen:{}".format(self.info[0], self.info[1], "屏幕录制" if self.info[2] == "1" else "白板"))

        app = QApplication.instance()
        app.quit()  # 提交后关闭
    
    
def main():
    app = QApplication(sys.argv)
    comboxDemo = ComboxDemo()
    comboxDemo.show()
    app.exec_()  # 不能退出整个程序，但需要这行代码维持运行


if __name__ == '__main__':
    app = QApplication(sys.argv)
    comboxDemo = ComboxDemo()
    comboxDemo.show()
    app.exec_()
    sys.exit(app.exec_())