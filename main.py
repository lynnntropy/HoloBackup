import sys
import os
from PyQt4 import QtGui, QtCore

Path = os.getcwd() + "\\Backups\\" + "backup.ab"

PackageToBackup = ""

class SingleAppWindow(QtGui.QWidget):
	def __init__(self):
		super(SingleAppWindow, self).__init__()
		self.initUI()
	
	def center(self):
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
		
	def initUI(self):
		self.resize(500, 500)
		self.center()
		
		applist = QtGui.QListWidget(self)
		applist.resize(500, 500)
		applist.move(0, 0)
		applist.show()
		
class Window(QtGui.QWidget):
	def __init__(self):
		super(Window, self).__init__()
		self.initUI()
		
	def handleNewWindow(self):
		window = QtGui.QMainWindow(self)
		window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		window.setWindowTitle(self.tr('Backup Single App'))
		window.resize(500, 500)
		window.show()
		
		window.list = QtGui.QListWidget(self)
		window.list.resize(100, 100)
		window.list.move(1, 1)
		window.list.show()

	def showDialog(self):
		text, ok = QtGui.QInputDialog.getText(self, 'Backup single app', "You should be seeing a list of installed packages in the second window. Enter which one you want to backup.")
		PackageToBackup = (str(text))
	
	def showDisclaimer(self):
		popup_msg = "ADB Backup is an undocumented, hacky and untested part of the Android SDK. There are various phones and tablets it simply does not work on, and even then it's very likely that at least some part of it will cause an error or simply produce an empty backup file. Some functions also may require superuser permissions on your device.\n\nAs a result of this, I strongly recommend that you check if the application actually works for you before relying on it as your only backup solution."
		reply = QtGui.QMessageBox.question(self, 'Disclaimer', popup_msg, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
		
		if reply == QtGui.QMessageBox.Ok:
			pass
		else:
			exit(0)

	def password_popup(self):
		popup_msg = "This program only works properly if you've set a 'Desktop backup password' in Developer Options. Have you done that?"
		reply = QtGui.QMessageBox.question(self, 'Warning!',
			popup_msg, QtGui.QMessageBox.Yes)
			
	def progress_popup(self):
		popup_msg = "Ready to start the operation. You'll need to monitor the rest of the process on your device. Be careful not to close the main window until it's done!"
		reply = QtGui.QMessageBox.question(self, 'Ready!',
			popup_msg, QtGui.QMessageBox.Ok)
			
	def backup_all_without_system(self):
		self.password_popup()
		self.progress_popup()
		os.system("adb backup -apk -shared -all -nosystem -f \"" + Path + "\"")
		
	def backup_all_with_system(self):
		self.password_popup()
		self.progress_popup()
		os.system("adb backup -apk -shared -all -system -f \"" + Path + "\"")
		
	def backup_app_data_and_device_data(self):
		self.password_popup()
		self.progress_popup()
		os.system("adb backup -all -f \"" + Path + "\"")
		
	def backup_apps(self):
		self.password_popup()
		self.progress_popup()
		os.system("adb backup -apk -noshared -nosystem -f \"" + Path + "\"")
		
	def backup_storage(self):
		self.password_popup()
		self.progress_popup()
		os.system("adb backup -noapk -shared -nosystem -f \"" + Path + "\"")
		
	def backup_single_app(self):
		os.system("singleappbackup.bat")
		#print "Single app placeholder"
		
		#app2 = QtGui.QApplication(sys.argv)
		#w = SingleAppWindow()
		#sys.exit(app2.exec_())
		
		#self.handleNewWindow()
		
		self.showDialog()
		
		self.password_popup()
		self.progress_popup()
		print "PackageToBackup = " + PackageToBackup
		print "Path = " + Path
		os.system("adb backup " + PackageToBackup + " \"" + Path + "\"")
		
	def restore(self):
		backup_location = QtGui.QFileDialog.getOpenFileName(self, 'Open backup file', os.getcwd())
		self.password_popup()
		self.progress_popup()
		os.system("adb restore " + str(backup_location))
		
	def openBrowseWindow(self):
		# print "Browse window placeholder"
		#dialog = QtGui.QFileDialog(self, 'Select: Shared Music Directory', os.getcwd())
		#dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
		
		directory = QtGui.QFileDialog.getExistingDirectory(self, 'Select backup directory')
		win_directory = QtCore.QDir.toNativeSeparators(directory)
		
		Path = win_directory + "\\backup.ab"
		self.location_path.setText(win_directory)
		
	def initUI(self):
		self.showDisclaimer()

		self.resize(300, 500)
		self.center()
		self.setFixedSize(300, 500)
		
		self.setWindowTitle("Simple ADB Backup")
		
		self.header = QtGui.QLabel(self)
		self.header.setPixmap(QtGui.QPixmap('header.png'))
		self.header.setGeometry(0, 0, 300, 70)
		self.show()
		
		self.arrow_left = QtGui.QLabel(self)
		self.arrow_left.setPixmap(QtGui.QPixmap('arrow_left.png'))
		self.arrow_left.setGeometry(257, 127, 20, 20)
		self.arrow_left.show()

		self.arrow_right = QtGui.QLabel(self)
		self.arrow_right.setPixmap(QtGui.QPixmap('arrow_right.png'))
		self.arrow_right.setGeometry(23, 127, 20, 20)
		self.arrow_right.show()

		warning1 = QtGui.QLabel(self)
		warning1.setGeometry(45, 70, 300, 14)
		warning1.setText("<font color='red'>Backups only work on devices running 4.0+.<font>")
		warning1.show()
		
		warning2 = QtGui.QLabel(self)
		warning2.setGeometry(30, 84, 300, 14)
		warning2.setText("<font color='red'>Backups can only be restored to the same device.<font>")
		warning2.show()
		
		warning3 = QtGui.QLabel(self)
		warning3.setGeometry(60, 98, 300, 14)
		warning3.setText("<font color='red'>Make sure USB Debugging is enabled.<font>")
		warning3.show()
		
		btn_1 = QtGui.QPushButton('Backup all without system apps', self)
		btn_1.resize(200, 25)
		btn_1.move(50, 124)
		btn_1.clicked.connect(self.backup_all_without_system)
		btn_1.show()
		
		btn_2 = QtGui.QPushButton('Backup all with system apps (unsafe)', self)
		btn_2.resize(200, 25)
		btn_2.move(50, 150)
		btn_2.clicked.connect(self.backup_all_with_system)
		btn_2.show()
		
		btn_3 = QtGui.QPushButton('Backup app data and device data', self)
		btn_3.resize(200, 25)
		btn_3.move(50, 176)
		btn_3.clicked.connect(self.backup_app_data_and_device_data)
		btn_3.show()
		
		btn_4 = QtGui.QPushButton('Backup apps', self)
		btn_4.resize(200, 25)
		btn_4.move(50, 202)
		btn_4.clicked.connect(self.backup_apps)
		btn_4.show()
		
		btn_5 = QtGui.QPushButton('Backup storage / SD card', self)
		btn_5.resize(200, 25)
		btn_5.move(50, 228)
		btn_5.clicked.connect(self.backup_storage)
		btn_5.show()
		
		btn_6 = QtGui.QPushButton('Backup a single app', self)
		btn_6.resize(200, 25)
		btn_6.move(50, 254)
		btn_6.clicked.connect(self.backup_single_app)
		btn_6.show()
		
		btn_restore = QtGui.QPushButton("Restore...", self)
		btn_restore.resize(200, 25)
		btn_restore.move(50, 290)
		btn_restore.clicked.connect(self.restore)
		btn_restore.show()
		
		location_header = QtGui.QLabel(self)
		location_header.setGeometry(80, 324, 300, 14)
		location_header.setText("Backups will be stored here:")
		location_header.show()
				
		self.location_path = QtGui.QLineEdit(self)
		self.location_path.move(50, 344)
		self.location_path.resize(144, 20)
		self.location_path.show()
		self.location_path.setText(os.getcwd() + "\\Backups\\")
		
		btn_browse = QtGui.QPushButton("Browse...", self)
		btn_browse.resize(55, 22)
		btn_browse.move(195, 343)
		btn_browse.clicked.connect(self.openBrowseWindow)
		btn_browse.show()
		
		location_footer = QtGui.QLabel(self)
		location_footer.setGeometry(95, 370, 300, 14)
		location_footer.setText("(You can change this.)")
		location_footer.show()
		
		
		
		
	def center(self):
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
		
def main():
	app = QtGui.QApplication(sys.argv)
	w = Window()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()
