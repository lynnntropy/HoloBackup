#!/usr/bin/env python

import sys
import os
import webbrowser
from PyQt4 import QtGui, QtCore

Path = os.getcwd() + "/Backups/" + "backup.ab"

"""
Help text for adb backup extracted from adb help:

adb backup [-f <file>] [-apk|-noapk] [-obb|-noobb] [-shared|-noshared] [-all] [-system|-nosystem] [<packages...>]
- write an archive of the device's data to <file>.

If no -f option is supplied then the data is written to "backup.ab" in the current directory.

(-apk|-noapk enable/disable backup of the .apks themselves in the archive; the default is noapk.)

(-obb|-noobb enable/disable backup of any installed apk expansion (aka .obb) files associated with each application;
    the default is noobb.)

(-shared|-noshared enable/disable backup of the device's shared storage / SD card contents; the default is noshared.)

(-all means to back up all installed applications)

(-system|-nosystem toggles whether -all automatically includes system applications;
    the default is to include system apps)

(<packages...> is the list of applications to be backed up.
    If the -all or -shared flags are passed, then the package list is optional.
    Applications explicitly given on the command line will be included even if -nosystem would ordinarily cause them to
    be omitted.)
"""


class Window(QtGui.QWidget):
    su_command = ''

    def __init__(self):
        super(Window, self).__init__()

        Window.su_command = Window.get_su_gui_command()

        self.package_to_backup = self.use_system_adb_binary = self.background = self.btn1 = self.btn2 = self.btn3 = \
            self.btn4 = self.btn5 = self.restore = self.sms = self.browse = self.path_label = self.wireless_adb = \
            self.btc = self.system_adb = None

        self.init_ui()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_dialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Backup single app',
                                              "You should be seeing a list of installed packages in the second window. "
                                              "Enter which one you want to backup.")
        if ok:
            self.package_to_backup = str(text)

    def show_disclaimer(self):
        popup_msg = "ADB Backup is an undocumented, hacky and untested part of the Android SDK. " \
                    "There are various phones and tablets it has trouble with, and on certain devices, " \
                    "it's fairly likely it'll produce an empty backup file for no reason. " \
                    "Some functions might not work properly without root access to your device.\n\n" \
                    "As a result of this, I strongly recommend that you check if the application actually works " \
                    "for you before relying on it as your only backup solution."
        reply = QtGui.QMessageBox.question(self, 'Disclaimer', popup_msg, QtGui.QMessageBox.Ok,
                                           QtGui.QMessageBox.Cancel)

        if reply == QtGui.QMessageBox.Ok:
            pass
        else:
            exit(0)

    def password_popup(self):
        popup_msg = "This program only works properly if you've set a 'Desktop backup password' in Developer Options." \
                    " Have you done that?"
        reply = QtGui.QMessageBox.question(self, 'Warning!',
                                           popup_msg, QtGui.QMessageBox.Yes)

    def progress_popup(self):
        popup_msg = "Ready to start the operation. You'll need to monitor the rest of the process on your device. " \
                    "Be careful not to close the main window until it's done!"
        reply = QtGui.QMessageBox.question(self, 'Ready!',
                                           popup_msg, QtGui.QMessageBox.Ok)

    def root_popup(self):
        popup_msg = "Backups can only be performed when the application is run as superuser/root. Please do that now."
        reply = QtGui.QMessageBox.question(self, 'Warning!',
                                           popup_msg, QtGui.QMessageBox.Ok)
        exit(0)

    def sms_popup(self):
        popup_msg = "SMS Backup+, a great open-source application by Jan Berkel, will now be installed and " \
                    "launched on your device.\n\nYou can use this to back up and restore your SMS messages and " \
                    "call log entries using a custom label in your GMail."
        reply = QtGui.QMessageBox.question(self, 'SMS Backup / Restore',
                                           popup_msg, QtGui.QMessageBox.Ok)

    def btn1_enter(self, event):
        self.btn1.setPixmap(QtGui.QPixmap('img/btn1_down.png'))

    def btn1_leave(self, event):
        self.btn1.setPixmap(QtGui.QPixmap('img/btn1_up.png'))

    def btn2_enter(self, event):
        self.btn2.setPixmap(QtGui.QPixmap('img/btn2_down.png'))

    def btn2_leave(self, event):
        self.btn2.setPixmap(QtGui.QPixmap('img/btn2_up.png'))

    def btn3_enter(self, event):
        self.btn3.setPixmap(QtGui.QPixmap('img/btn3_down.png'))

    def btn3_leave(self, event):
        self.btn3.setPixmap(QtGui.QPixmap('img/btn3_up.png'))

    def btn4_enter(self, event):
        self.btn4.setPixmap(QtGui.QPixmap('img/btn4_down.png'))

    def btn4_leave(self, event):
        self.btn4.setPixmap(QtGui.QPixmap('img/btn4_up.png'))

    def btn5_enter(self, event):
        self.btn5.setPixmap(QtGui.QPixmap('img/btn5_down.png'))

    def btn5_leave(self, event):
        self.btn5.setPixmap(QtGui.QPixmap('img/btn5_up.png'))

    def restore_enter(self, event):
        self.restore.setPixmap(QtGui.QPixmap('img/restore_down.png'))

    def restore_leave(self, event):
        self.restore.setPixmap(QtGui.QPixmap('img/restore_up.png'))

    def browse_enter(self, event):
        self.browse.setPixmap(QtGui.QPixmap('img/browse_down.png'))

    def browse_leave(self, event):
        self.browse.setPixmap(QtGui.QPixmap('img/browse_up.png'))

    def sms_enter(self, event):
        self.sms.setPixmap(QtGui.QPixmap('img/sms_down.png'))

    def sms_leave(self, event):
        self.sms.setPixmap(QtGui.QPixmap('img/sms_up.png'))

    def btc_enter(self, event):
        self.btc.setPixmap(QtGui.QPixmap('img/btc_down.png'))

    def btc_leave(self, event):
        self.btc.setPixmap(QtGui.QPixmap('img/btc_up.png'))

    def wireless_adb_enter(self, event):
        self.wireless_adb.setPixmap(QtGui.QPixmap('img/wirelessAdb_down.png'))

    def wireless_adb_leave(self, event):
        self.wireless_adb.setPixmap(QtGui.QPixmap('img/wirelessAdb_up.png'))

    def backup_all_without_system(self, event):
        self.password_popup()
        self.progress_popup()

        if not self.use_system_adb_binary:
            os.system(Window.su_command + ' "./adb backup -apk -shared -all -nosystem -f "' + Path + '""')
        else:
            os.system('adb backup -apk -shared -all -nosystem -f "' + Path + '"')

    def backup_all_with_system(self, event):
        self.password_popup()
        self.progress_popup()

        if not self.use_system_adb_binary:
            os.system(Window.su_command + ' "./adb backup -apk -shared -all -system -f "' + Path + '""')
        else:
            os.system('adb backup -apk -shared -all -system -f "' + Path + '"')

    def backup_app_data_and_device_data(self, event):
        self.password_popup()
        self.progress_popup()

        if not self.use_system_adb_binary:
            os.system(Window.su_command + ' "./adb backup -all -f "' + Path + '""')
        else:
            os.system('adb backup -all -f "' + Path + '"')

    def backup_apps(self, event):
        self.password_popup()
        self.progress_popup()

        if not self.use_system_adb_binary:
            os.system(Window.su_command + ' "./adb backup -apk -noshared -nosystem -f "' + Path + '""')
        else:
            os.system('adb backup -apk -noshared -nosystem -f "' + Path + '"')

    def backup_storage(self, event):
        self.password_popup()
        self.progress_popup()

        if not self.use_system_adb_binary:
            os.system(Window.su_command + ' "./adb backup -noapk -shared -nosystem -f "' + Path + '""')
        else:
            os.system('adb backup -noapk -shared -nosystem -f "' + Path + '"')

    def get_backup_location(self, event):
        backup_location = QtGui.QFileDialog.getOpenFileName(self, 'Open backup file', os.getcwd())
        self.password_popup()
        self.progress_popup()

        if not self.use_system_adb_binary:
            os.system(Window.su_command + ' "./adb restore ' + str(backup_location) + '"')
        else:
            os.system("adb restore " + str(backup_location))

    def install_sms_app(self, event):
        self.sms_popup()
        if not self.use_system_adb_binary:
            os.system(Window.su_command + ' "./adb install smsBackupPlus/sms_backup_plus.apk"')
            os.system(Window.su_command + ' "./adb shell am start -n '
                                          'com.zegoggles.smssync/com.zegoggles.smssync.SmsSync"')
        else:
            os.system("adb install smsBackupPlus/sms_backup_plus.apk")
            os.system("adb shell am start -n com.zegoggles.smssync/com.zegoggles.smssync.SmsSync")

    def open_browse_window(self, event):
        # print "Browse window placeholder"
        #dialog = QtGui.QFileDialog(self, 'Select: Shared Music Directory', os.getcwd())
        #dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)

        directory = QtGui.QFileDialog.getExistingDirectory(self, 'Select backup directory')

        Path = directory + "/backup.ab"
        self.path_label.setText(directory)

    def adb_binary_change(self, event):
        if not self.use_system_adb_binary:
            self.use_system_adb_binary = True
            self.system_adb.setPixmap(QtGui.QPixmap('img/adb_checked.png'))
        else:
            self.use_system_adb_binary = False
            self.system_adb.setPixmap(QtGui.QPixmap('img/adb_unchecked.png'))

    @staticmethod
    def donate_btc(event):
        webbrowser.open(os.getcwd() + os.sep + 'donate.html')

    def connect_wireless_adb(self, event):
        text, ok = QtGui.QInputDialog.getText(self, 'Connect to Wireless ADB',
                                              "If your device is set up for wireless ADB, connect to it here. "
                                              "Just type the location of the device in 'host:port' format.")
        if ok:
            os.system("./adb connect " + str(text))

    @staticmethod
    def get_su_gui_command():
        """
        Ensure that the proper graphical front end for su is used when running in different desktop environments.
        That is: kdesu for KDE, gksudo for GNOME, XFCE, etc
        """
        if 'KDE_FULL_SESSION' in os.environ and os.environ['KDE_FULL_SESSION']:
            return '$(kde4-config --path libexec)kdesu -c'
        else:
            return 'gksudo'

    def init_ui(self):
        self.show_disclaimer()

        # backup_location = QtGui.QFileDialog.getOpenFileName(self, 'Open backup file', os.getcwd())

        self.use_system_adb_binary = False

        self.resize(300, 500)
        self.center()
        self.setFixedSize(300, 500)

        self.setWindowTitle("Holo Backup")

        self.background = QtGui.QLabel(self)
        self.background.setPixmap(QtGui.QPixmap('mockup.png'))
        self.background.setGeometry(0, 0, 300, 500)
        # self.show()

        self.btn1 = QtGui.QLabel(self)
        self.btn1.setPixmap(QtGui.QPixmap('img/btn1_up.png'))
        self.btn1.setGeometry(34, 109, 235, 26)
        self.btn1.enterEvent = self.btn1_enter
        self.btn1.leaveEvent = self.btn1_leave
        self.btn1.mouseReleaseEvent = self.backup_all_without_system

        self.btn2 = QtGui.QLabel(self)
        self.btn2.setPixmap(QtGui.QPixmap('img/btn2_up.png'))
        self.btn2.setGeometry(34, 138, 235, 26)
        self.btn2.enterEvent = self.btn2_enter
        self.btn2.leaveEvent = self.btn2_leave
        self.btn2.mouseReleaseEvent = self.backup_all_with_system

        self.btn3 = QtGui.QLabel(self)
        self.btn3.setPixmap(QtGui.QPixmap('img/btn3_up.png'))
        self.btn3.setGeometry(34, 167, 235, 26)
        self.btn3.enterEvent = self.btn3_enter
        self.btn3.leaveEvent = self.btn3_leave
        self.btn3.mouseReleaseEvent = self.backup_app_data_and_device_data

        self.btn4 = QtGui.QLabel(self)
        self.btn4.setPixmap(QtGui.QPixmap('img/btn4_up.png'))
        self.btn4.setGeometry(34, 196, 235, 26)
        self.btn4.enterEvent = self.btn4_enter
        self.btn4.leaveEvent = self.btn4_leave
        self.btn4.mouseReleaseEvent = self.backup_apps

        self.btn5 = QtGui.QLabel(self)
        self.btn5.setPixmap(QtGui.QPixmap('img/btn5_up.png'))
        self.btn5.setGeometry(34, 225, 235, 26)
        self.btn5.enterEvent = self.btn5_enter
        self.btn5.leaveEvent = self.btn5_leave
        self.btn5.mouseReleaseEvent = self.backup_storage

        self.restore = QtGui.QLabel(self)
        self.restore.setPixmap(QtGui.QPixmap('img/restore_up.png'))
        self.restore.setGeometry(34, 270, 235, 26)
        self.restore.enterEvent = self.restore_enter
        self.restore.leaveEvent = self.restore_leave
        self.restore.mouseReleaseEvent = self.get_backup_location

        self.sms = QtGui.QLabel(self)
        self.sms.setPixmap(QtGui.QPixmap('img/sms_up.png'))
        self.sms.setGeometry(34, 315, 235, 26)
        self.sms.enterEvent = self.sms_enter
        self.sms.leaveEvent = self.sms_leave
        self.sms.mouseReleaseEvent = self.install_sms_app

        self.browse = QtGui.QLabel(self)
        self.browse.setPixmap(QtGui.QPixmap('img/browse_up.png'))
        self.browse.setGeometry(216, 372, 69, 26)
        self.browse.enterEvent = self.browse_enter
        self.browse.leaveEvent = self.browse_leave
        self.browse.mouseReleaseEvent = self.open_browse_window

        self.path_label = QtGui.QLabel(self)
        self.path_label.setGeometry(22, 381, 189, 14)
        self.path_label.setText(os.getcwd() + '/Backups/')

        self.wireless_adb = QtGui.QLabel(self)
        self.wireless_adb.setPixmap(QtGui.QPixmap('img/wirelessAdb_up.png'))
        self.wireless_adb.setGeometry(34, 407, 235, 26)
        self.wireless_adb.enterEvent = self.wireless_adb_enter
        self.wireless_adb.leaveEvent = self.wireless_adb_leave
        self.wireless_adb.mouseReleaseEvent = self.connect_wireless_adb

        self.btc = QtGui.QLabel(self)
        self.btc.setPixmap(QtGui.QPixmap('img/btc_up.png'))
        self.btc.setGeometry(34, 474, 235, 26)
        self.btc.enterEvent = self.btc_enter
        self.btc.leaveEvent = self.btc_leave
        self.btc.mouseReleaseEvent = self.donate_btc
        self.btc.show()

        self.system_adb = QtGui.QLabel(self)
        self.system_adb.setPixmap(QtGui.QPixmap('img/adb_unchecked.png'))
        self.system_adb.setGeometry(10, 450, 272, 29)
        # self.system_adb.enterEvent = self.browse_enter
        # self.system_adb.leaveEvent = self.browse_leave
        self.system_adb.mouseReleaseEvent = self.adb_binary_change


def main():
    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
