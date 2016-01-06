import sys
import os
import webbrowser
from PyQt4 import QtGui, QtCore
from ui_files import main_gui

Path = os.getcwd() + "/Backups/" + "backup.ab"
Path = QtCore.QDir.toNativeSeparators(Path)

class Window(QtGui.QDialog, main_gui.Ui_mainWindow):
	def __init__(self):
		super(Window, self).__init__()		
		self.setupUi(self)
		self.initUI()
		
		self.bakAllNoSys.clicked.connect(self.backup_all_without_system)
		self.bakAll.clicked.connect(self.backup_all_with_system)
		self.bakAppDevData.clicked.connect(self.backup_app_data_and_device_data)
		self.bakApp.clicked.connect(self.backup_apps)
		self.bakStorSd.clicked.connect(self.backup_storage)
		self.restoreBtn.clicked.connect(self.getBackupLocation)
		self.smsBakRestore.clicked.connect(self.installSmsApp)
		self.bakBrowseBtn.clicked.connect(self.openBrowseWindow)
		self.wirelessAdb.clicked.connect(self.connectWirelessADB)
		self.systemAdb.toggled.connect(self.adbBinaryChange)
		
	def center(self):
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def showDialog(self):
		text, ok = QtGui.QInputDialog.getText(self, 'Backup single app', "You should be seeing a list of installed packages in the second window. Enter which one you want to backup.")
		if ok:
			self.PackageToBackup = str(text)

	def showDisclaimer(self):
		popup_msg = "ADB Backup is an undocumented, hacky and untested part of the Android SDK. There are various phones and tablets it has trouble with, and on certain devices, it's fairly likely it'll produce an empty backup file for no reason. Some functions might not work properly without root access to your device.\n\nAs a result of this, I strongly recommend that you check if the application actually works for you before relying on it as your only backup solution."
		reply = QtGui.QMessageBox.question(self, 'Disclaimer', popup_msg, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
		
		if not reply == QtGui.QMessageBox.Ok:			
			exit(0)
	
	def password_popup(self):
		popup_msg = "This program only works properly if you've set a 'Desktop backup password' in Developer Options. Have you done that?"
		reply = QtGui.QMessageBox.question(self, 'Warning!',
			popup_msg, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
			
		if reply is not QtGui.QMessageBox.Yes:
		    return
			
	def progress_popup(self):
		popup_msg = "Ready to start the operation. You'll need to monitor the rest of the process on your device. Be careful not to close the main window until it's done!"
		reply = QtGui.QMessageBox.question(self, 'Ready!',
			popup_msg, QtGui.QMessageBox.Ok)

	def root_popup(self):
		popup_msg = "Backups can only be performed when the application is run as superuser/root. Please do that now."
		reply = QtGui.QMessageBox.question(self, 'Warning!',
			popup_msg, QtGui.QMessageBox.Ok)
		exit(0)

	def sms_popup(self):
		popup_msg = "SMS Backup+, a great open-source application by Jan Berkel, will now be installed and launched on your device.\n\nYou can use this to back up and restore your SMS messages and call log entries using a custom label in your Gmail."
		reply = QtGui.QMessageBox.question(self, 'SMS Backup / Restore',
			popup_msg, QtGui.QMessageBox.Ok)

	def backup_all_without_system(self, event):
	
	    if self.password_popup():
	    	self.progress_popup()
	    else:
    		return
	        
		if not self.useSystemAdbBinary:
			os.system(str("gksudo \"./adb backup -apk -shared -all -nosystem -f \"" + Path + "\"\""))
		else:
			os.system(str("adb backup -apk -shared -all -nosystem -f \"" + Path + "\""))
		
	def backup_all_with_system(self, event):
		if self.password_popup():
			self.progress_popup()
		else:
			return
		
		if not self.useSystemAdbBinary:
			os.system(str("gksudo \"./adb backup -apk -shared -all -system -f \"" + Path + "\"\""))
		else:
			os.system(str("adb backup -apk -shared -all -system -f \"" + Path + "\""))
		
	def backup_app_data_and_device_data(self, event):
		if self.password_popup():
			self.progress_popup()
		else:
			return

		if not self.useSystemAdbBinary:
			os.system(str("gksudo \"./adb backup -all -f \"" + Path + "\"\""))
		else:
			os.system(str("adb backup -all -f \"" + Path + "\""))
		
	def backup_apps(self, event):
		if self.password_popup():
			self.progress_popup()
		else:
			return

		if not self.useSystemAdbBinary:
			os.system(str("gksudo \"./adb backup -apk -noshared -nosystem -f \"" + Path + "\"\""))
		else:
			os.system(str("adb backup -apk -noshared -nosystem -f \"" + Path + "\""))
		
	def backup_storage(self, event):
		if self.password_popup():
			self.progress_popup()
		else:
			return

		if not self.useSystemAdbBinary:
			os.system(str("gksudo \"./adb backup -noapk -shared -nosystem -f \"" + Path + "\"\""))
		else:
			os.system(str("adb backup -noapk -shared -nosystem -f \"" + Path + "\""))

	def getBackupLocation(self, event):
		backup_location = QtGui.QFileDialog.getOpenFileName(self, 'Open backup file', os.getcwd())
		if self.password_popup():
			self.progress_popup()
		else:
			return

		if not self.useSystemAdbBinary:
			os.system(str("gksudo \"./adb restore " + str(backup_location) + "\""))
		else:
			os.system(str("adb restore " + str(backup_location)))


	def installSmsApp(self, event):
		self.sms_popup()
		if not self.useSystemAdbBinary:
			os.system(str("gksudo \"./adb install smsBackupPlus/sms_backup_plus.apk\""))
			os.system(str("gksudo \"./adb shell am start -n com.zegoggles.smssync/com.zegoggles.smssync.SmsSync\""))
		else:
			os.system(str("adb install smsBackupPlus/sms_backup_plus.apk"))
			os.system(str("adb shell am start -n com.zegoggles.smssync/com.zegoggles.smssync.SmsSync"))
		
	def openBrowseWindow(self, event):
		# print "Browse window placeholder"
		#dialog = QtGui.QFileDialog(self, 'Select: Shared Music Directory', os.getcwd())
		#dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
		
		directory = QtGui.QFileDialog.getExistingDirectory(self, 'Select backup directory')
		
		Path = QtCore.QDir.toNativeSeparators(directory + "/backup.ab")
		self.pathLabel.setText(directory)

	def adbBinaryChange(self, event):
		pass

	def donateBtc(self, event):
		webbrowser.open('donate.html')

	def connectWirelessADB(self, event):
		text, ok = QtGui.QInputDialog.getText(self, 'Connect to Wireless ADB', "If your device is set up for wireless ADB, connect to it here. Just type the location of the device in 'host:port' format.")
		if ok:
			os.system(str("./adb connect " + str(text)))

	def initUI(self):
		self.showDisclaimer()

		# backup_location = QtGui.QFileDialog.getOpenFileName(self, 'Open backup file', os.getcwd())

		self.useSystemAdbBinary = False

		self.resize(300, 520)
		self.center()
		self.setFixedSize(300, 520)		
		self.setWindowTitle("Holo Backup")		
		self.bakLocation.setText(Path)


def main():
	app = QtGui.QApplication(sys.argv)
	w = Window()
	w.show()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()
