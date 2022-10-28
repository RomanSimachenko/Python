from PyQt5 import QtCore, QtGui, QtWidgets
from python import rename_folders, set_folders_name, resize_image
import sys
import os
#try:
#    from PIL import ImageGrab
#    screen = ImageGrab.grab()
#    screen_w, screen_h = screen.size
#except:
import pyautogui
resolution = pyautogui.size()
screen_w, screen_h = resolution[0], resolution[1]
if screen_w > 1920:
    screen_w = 1920
if screen_h > 1080:
    screen_h = 1080
if screen_w < 800:
    screen_w = 800
if screen_h < 600:
    screen_h = 600
window_w, window_h = screen_w // 2 + 170, screen_h // 2 + 100
# resize background image
resize_image(window_w, window_h)

# set LinePath width and height relative to our screen
LinePath_w, LinePath_h = (window_w * 80) // 100, window_h // 10
# set RenameFolders width and height relative to our screen
RenameFolders_w, RenameFolders_h = (
    window_w * 50) // 100, (window_h * 15) // 100
# set SetFoldersName width and height relative to our screen
SetFoldersName_w, SetFoldersName_h = (
    window_w * 50) // 100, (window_h * 15) // 100

# set LinePath x and y(the upper left coordinate of rectangle) relative to our screen
LinePath_x, LinePath_y = (window_w - LinePath_w) // 2, (window_h * 15) // 100
# set RenameFolders x and y(the upper left coordinate of rectangle) relative to our screen
RenameFolders_x, RenameFolders_y = (
    window_w - RenameFolders_w) // 2, (window_h * 35) // 100
# set SetFoldersName x and y(the upper left coordinate of rectangle) relative to our screen
SetFoldersName_x, SetFoldersName_y = (
    window_w - SetFoldersName_w) // 2, (window_h * 55) // 100


# create class for MainWindow
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # main window setting
        # set object name
        MainWindow.setObjectName("MainWindow")
        # set rectangle with and height
        MainWindow.resize(window_w, window_h)
        MainWindow.setStyleSheet("""
                background: white;
            """)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        # set styles
        self.centralwidget.setStyleSheet("""
                background: url("../data/background.jpg") no-repeat center;
            """)
        # set obj name
        self.centralwidget.setObjectName("centralwidget")

        # Line for path setting
        self.PathLine = QtWidgets.QLineEdit(self.centralwidget)
        # set rectangle start, end x and y
        self.PathLine.setGeometry(QtCore.QRect(
            LinePath_x, LinePath_y, LinePath_w, LinePath_h))
        # set styles
        self.PathLine.setStyleSheet("""
                font: Times New Roman;
                color: white;
                font-size: 26px;
                border: 2px solid rgb(0, 153, 255);
            """)
        # set obj name
        self.PathLine.setObjectName("PathLine")

        # Button for rename folders
        self.RenameFolders = QtWidgets.QPushButton(
            self.centralwidget)
        # set rectangle start, end x and y
        self.RenameFolders.setGeometry(
            QtCore.QRect(RenameFolders_x, RenameFolders_y, RenameFolders_w, RenameFolders_h))
        # set styles
        #self.RenameFolders.setStyleSheet("""
         #       font: bold Times New Roman;
          #      color: white;
           #     font-size: 32px;
            #    border: 2px solid rgb(255, 51, 133);
             #""")
        # set obj name
        self.RenameFolders.setObjectName("RenameFolders")
        MainWindow.setCentralWidget(self.centralwidget)

        # Button for return folder's names
        self.SetFoldersName = QtWidgets.QPushButton(
            self.centralwidget)
        # set rectangle start, end x and y
        self.SetFoldersName.setGeometry(
            QtCore.QRect(SetFoldersName_x, SetFoldersName_y, SetFoldersName_w, SetFoldersName_h))
        # set styles
        self.SetFoldersName.setStyleSheet("""
                font: bold Times New Roman;
                color: white;
                font-size: 32px;
                border: 2px solid rgb(255, 51, 133);
            """)
        # set obj name
        self.SetFoldersName.setObjectName("SetFoldersName")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # set buttons text and main window title

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("RenameFolders", "RenameFolders"))
        self.RenameFolders.setText(_translate("MainWindow", "Rename Folders"))
        self.SetFoldersName.setText(
            _translate("MainWindow", "Set Folders Name"))


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # set window icon
        self.setWindowIcon(QtGui.QIcon('../data/icon.ico'))

        # set up settings
        self.setupUi(self)
        # if clicked run func 'rename_folders'
        self.RenameFolders.clicked.connect(self.rename_folders)
        # if clicked run func 'set_folders_name'
        self.SetFoldersName.clicked.connect(self.set_folders_name)

    def rename_folders(self, file_path):
        # turn off button 'RenameFolders'
        self.RenameFolders.setEnabled(False)
        # del spaces in our path line
        if self.PathLine.text().strip() != '':
            # call our func to rename folders from other script
            if rename_folders(file_path=self.PathLine.text()):
                # turn on button
                self.RenameFolders.setEnabled(True)
        else:
            self.RenameFolders.setEnabled(True)

    def set_folders_name(self, file_path):
        # turn off button 'RenameFolders'
        self.RenameFolders.setEnabled(False)
        # del spaces in our path line
        if self.PathLine.text().strip() != '':
            # call our func to rename set back names from other script
            if set_folders_name(file_path=self.PathLine.text()):
                # turn on button
                self.RenameFolders.setEnabled(True)
        else:
            self.RenameFolders.setEnabled(True)


# start main app
def start_app():
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()
