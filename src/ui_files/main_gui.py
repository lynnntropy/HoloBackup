# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_gui.ui'
#
# Created: Sun Feb  3 07:52:52 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName(_fromUtf8("mainWindow"))
        mainWindow.resize(300, 520)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mainWindow.sizePolicy().hasHeightForWidth())
        mainWindow.setSizePolicy(sizePolicy)
        mainWindow.setMinimumSize(QtCore.QSize(300, 520))
        mainWindow.setMaximumSize(QtCore.QSize(300, 520))
        self.label = QtGui.QLabel(mainWindow)
        self.label.setGeometry(QtCore.QRect(10, 0, 151, 41))
        self.label.setFrameShadow(QtGui.QFrame.Plain)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(mainWindow)
        self.label_2.setGeometry(QtCore.QRect(10, 35, 291, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(mainWindow)
        self.label_3.setGeometry(QtCore.QRect(50, 80, 201, 41))
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(mainWindow)
        self.label_4.setGeometry(QtCore.QRect(20, 60, 261, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.bakAllNoSys = QtGui.QPushButton(mainWindow)
        self.bakAllNoSys.setGeometry(QtCore.QRect(25, 130, 251, 27))
        self.bakAllNoSys.setObjectName(_fromUtf8("bakAllNoSys"))
        self.bakAll = QtGui.QPushButton(mainWindow)
        self.bakAll.setGeometry(QtCore.QRect(25, 165, 251, 27))
        self.bakAll.setObjectName(_fromUtf8("bakAll"))
        self.bakAppDevData = QtGui.QPushButton(mainWindow)
        self.bakAppDevData.setGeometry(QtCore.QRect(25, 200, 251, 27))
        self.bakAppDevData.setObjectName(_fromUtf8("bakAppDevData"))
        self.bakStorSd = QtGui.QPushButton(mainWindow)
        self.bakStorSd.setGeometry(QtCore.QRect(25, 270, 251, 27))
        self.bakStorSd.setObjectName(_fromUtf8("bakStorSd"))
        self.bakApp = QtGui.QPushButton(mainWindow)
        self.bakApp.setGeometry(QtCore.QRect(25, 235, 251, 27))
        self.bakApp.setObjectName(_fromUtf8("bakApp"))
        self.line = QtGui.QFrame(mainWindow)
        self.line.setGeometry(QtCore.QRect(25, 305, 251, 5))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.restoreBtn = QtGui.QPushButton(mainWindow)
        self.restoreBtn.setGeometry(QtCore.QRect(25, 315, 251, 27))
        self.restoreBtn.setObjectName(_fromUtf8("restoreBtn"))
        self.smsBakRestore = QtGui.QPushButton(mainWindow)
        self.smsBakRestore.setGeometry(QtCore.QRect(25, 360, 251, 27))
        self.smsBakRestore.setObjectName(_fromUtf8("smsBakRestore"))
        self.line_2 = QtGui.QFrame(mainWindow)
        self.line_2.setGeometry(QtCore.QRect(25, 350, 251, 5))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.bakLocation = QtGui.QLineEdit(mainWindow)
        self.bakLocation.setGeometry(QtCore.QRect(25, 395, 151, 27))
        self.bakLocation.setObjectName(_fromUtf8("bakLocation"))
        self.bakBrowseBtn = QtGui.QPushButton(mainWindow)
        self.bakBrowseBtn.setGeometry(QtCore.QRect(180, 395, 98, 27))
        self.bakBrowseBtn.setObjectName(_fromUtf8("bakBrowseBtn"))
        self.donateLbl = QtGui.QLabel(mainWindow)
        self.donateLbl.setGeometry(QtCore.QRect(30, 492, 241, 17))
        self.donateLbl.setOpenExternalLinks(True)
        self.donateLbl.setObjectName(_fromUtf8("donateLbl"))
        self.wirelessAdb = QtGui.QPushButton(mainWindow)
        self.wirelessAdb.setGeometry(QtCore.QRect(25, 430, 251, 27))
        self.wirelessAdb.setObjectName(_fromUtf8("wirelessAdb"))
        self.systemAdb = QtGui.QCheckBox(mainWindow)
        self.systemAdb.setGeometry(QtCore.QRect(25, 465, 251, 22))
        self.systemAdb.setObjectName(_fromUtf8("systemAdb"))

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(_translate("mainWindow", "Holo Backup v2.0", None))
        self.label.setText(_translate("mainWindow", "<html><head/><body><p><span style=\" font-size:18pt; color:#006a9f;\">Holo Backup</span></p></body></html>", None))
        self.label_2.setText(_translate("mainWindow", "Backups only work on devices running 4.0+", None))
        self.label_3.setText(_translate("mainWindow", "<html><head/><body><p align=\"center\">Backups can only be restored to the same device</p></body></html>", None))
        self.label_4.setText(_translate("mainWindow", "Make sure USB Debugging is enabled!", None))
        self.bakAllNoSys.setText(_translate("mainWindow", "Backup all without system apps", None))
        self.bakAll.setText(_translate("mainWindow", "Backup all with system apps (unsafe)", None))
        self.bakAppDevData.setText(_translate("mainWindow", "Backup app data and device data", None))
        self.bakStorSd.setText(_translate("mainWindow", "Backup storage / SD card", None))
        self.bakApp.setText(_translate("mainWindow", "Backup apps", None))
        self.restoreBtn.setText(_translate("mainWindow", "Restore...", None))
        self.smsBakRestore.setText(_translate("mainWindow", "SMS Backup / Restore", None))
        self.bakLocation.setPlaceholderText(_translate("mainWindow", "Backup location", None))
        self.bakBrowseBtn.setText(_translate("mainWindow", "Browse", None))
        self.donateLbl.setText(_translate("mainWindow", "<html><head/><body><p><a href=\"donate.html\"><span style=\" text-decoration: underline; color:#0000ff;\">Feeling generous? Send me bitcoins!</span></a></p></body></html>", None))
        self.wirelessAdb.setText(_translate("mainWindow", "Connect to wireless ADB", None))
        self.systemAdb.setText(_translate("mainWindow", "Use system ADB binary? (No root)", None))

