from PIL.ImageQt import ImageQt 
from PIL import Image
from PyQt5.QtGui import QPixmap
import cv2

from PyQt5 import QtCore, QtGui, QtWidgets
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image as ros_img
import time


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, -250, 1920, 1080))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
    
        self.bridge = CvBridge()
        rospy.init_node("Rosimg to GUI")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.sub=rospy.Subscriber("/video_frame1/image",ros_img,self.convertROStoCV)
        self.frame_count=0
        self.timethen=time.time()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        print("Initialized")
    
    def convertROStoCV(self,msg):
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        self.convertCvImage2QtImage(frame)

    def convertCvImage2QtImage(self,frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        PIL_image = Image.fromarray(rgb_image).convert('RGB')
        self.embed_image=QPixmap.fromImage(ImageQt(PIL_image))
        self.label.setPixmap(self.embed_image)
        self.count_frames()
    
    def count_frames(self):
        self.frame_count+=1
        self.timenow=time.time()
        if(self.timenow-self.timethen<10.5 and self.timenow-self.timethen>10):
            self.current_frame=self.frame_count/10
            print("Current frame rate: " + str(self.current_frame))
            self.frame_count=0
            self.timethen=time.time()




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())