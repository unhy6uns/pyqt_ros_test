#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

import rospy
import rospkg
from std_msgs.msg import String

rospack = rospkg.RosPack()
PACKAGE_PATH = rospack.get_path('pyqt_test')

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType(PACKAGE_PATH + "/src/subscriber.ui")[0]

#사용자 정의 시그널 사용을 위한 클래스 정의
class CustomSignal(QObject):
    msg_received = pyqtSignal(int, str) #반드시 클래스 변수로 선언할 것

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #버튼에 기능을 연결하는 코드
        #self.publishButton.clicked.connect(self.buttonFunction)

        rospy.init_node('subscriber')
        rospy.Subscriber('/message', String, self.callback)

        self.customsignal = CustomSignal()
        self.customsignal.msg_received.connect(self.funcEmit)

        self.cnt = 0

    def callback(self, msg):
        #self.msg_dsp.clear()
        #self.msg_dsp.append(msg.data)
        self.cnt = self.cnt + 1
        #self.count.display(self.cnt)
        self.customsignal.msg_received.emit(self.cnt, msg.data)


    @pyqtSlot(int, str)
    def funcEmit(self, i, msg):
        self.msg_dsp.setPlainText(msg)
        self.count.display(i)

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
