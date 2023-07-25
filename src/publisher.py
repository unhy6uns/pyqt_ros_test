#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

import rospy
import rospkg
from std_msgs.msg import String

rospack = rospkg.RosPack()
PACKAGE_PATH = rospack.get_path('pyqt_test')

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType(PACKAGE_PATH + "/src/publisher.ui")[0]



class PublisherNode:
    def __init__(self):
        self.pub = rospy.Publisher('/message', String, queue_size = 2)
        rospy.init_node('publisher_node')

        # r = rospy.Rate(10) # 10hz
        # while not rospy.is_shutdown():
        #     self.pub.publish("hello world")
        #     r.sleep()

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.publisher = PublisherNode()

        #버튼에 기능을 연결하는 코드
        self.publishButton.clicked.connect(self.buttonFunction)

    #btn이 눌리면 작동할 함수
    def buttonFunction(self) :
        msg = String()
        msg.data = self.lineEdit.text()
        print("btn Clicked")
        self.publisher.pub.publish(msg)

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
