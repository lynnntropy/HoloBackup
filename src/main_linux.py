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


CONTROLS = {
    'btn1': {
        'geometry': [34, 109, 235, 26],
        'trigger': 'backup_all_without_system'
    },
    'btn2': {
        'geometry': [34, 138, 235, 26],
        'trigger': 'backup_all_with_system'
    },
    'btn3': {
        'geometry': [34, 167, 235, 26],
        'trigger': 'backup_app_data_and_device_data'
    },
    'btn4': {
        'geometry': [34, 196, 235, 26],
        'trigger': 'backup_apps'
    },
    'btn5': {
        'geometry': [34, 225, 235, 26],
        'trigger': 'backup_storage'
    },
    'restore': {
        'geometry': [34, 270, 235, 26],
        'trigger': 'get_backup_location'
    },
    'sms': {
        'geometry': [34, 315, 235, 26],
        'trigger': 'install_sms_app'
    },
    'browse': {
        'geometry': [216, 372, 69, 26],
        'trigger': 'open_browse_window'
    },
    'wirelessAdb': {
        'geometry': [34, 407, 235, 26],
        'trigger': 'connect_wireless_adb'
    },
    'btc': {
        'geometry': [34, 474, 235, 26],
        'trigger': 'donate_btc'
    }
}


def password_required(wrapped):
    def wrapper(self, *args):
        if self.password_popup():
            self.progress_popup()

            wrapped(self, *args)

    return wrapper


class Window(QtGui.QWidget):
    su_command = ''

    def __init__(self):
        super(Window, self).__init__()

        Window.su_command = Window.get_su_gui_command()

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
                                           popup_msg, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.Yes)

        return reply == QtGui.QMessageBox.Yes

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

    def run_command(self, command):
        if not self.use_system_adb_binary:
            command = '{0} \'./{1}\''.format(Window.su_command, command)

        os.system(command)

    @password_required
    def backup_all_without_system(self, event):
        self.run_command('adb backup -apk -shared -all -nosystem -f "{0}"'.format(Path))

    @password_required
    def backup_all_with_system(self, event):
        self.run_command('adb backup -apk -shared -all -system -f "{0}"'.format(Path))

    @password_required
    def backup_app_data_and_device_data(self, event):
        self.run_command('adb backup -all -f "{0}"'.format(Path))

    @password_required
    def backup_apps(self, event):
        self.run_command('adb backup -apk -noshared -nosystem -f "{0}"'.format(Path))

    @password_required
    def backup_storage(self, event):
        self.run_command('adb backup -noapk -shared -nosystem -f "{0}"'.format(Path))

    @password_required
    def _get_backup_location(self, backup_location):
        self.run_command("adb restore {0}".format(backup_location))

    def get_backup_location(self, event):
        backup_location = QtGui.QFileDialog.getOpenFileName(self, 'Open backup file', os.getcwd())

        self._get_backup_location(backup_location)

    def install_sms_app(self, event):
        self.sms_popup()

        self.run_command("adb install smsBackupPlus/sms_backup_plus.apk")
        self.run_command("adb shell am start -n com.zegoggles.smssync/com.zegoggles.smssync.SmsSync")

    def open_browse_window(self, event):
        # print "Browse window placeholder"
        directory = QtGui.QFileDialog.getExistingDirectory(self, 'Select backup directory')

        Path = directory + "/backup.ab"
        self.path_label.setText(directory)

    def adb_binary_change(self, event):
        if not self.use_system_adb_binary:
            self.use_system_adb_binary = True
            direction = 'checked'
        else:
            self.use_system_adb_binary = False
            direction = 'unchecked'

        self.system_adb.setPixmap(QtGui.QPixmap('img/adb_{0}.png'.format(direction)))

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

    def wrap_event(self, label, direction):
        def wrapped(event):
            getattr(self, label).setPixmap(
                QtGui.QPixmap('img/{0}_{1}.png'.format(label, direction)))

        return wrapped

    def create_button(self, label, geometry, method):
        button = QtGui.QLabel(self)
        button.setPixmap(QtGui.QPixmap('img/{0}_up.png'.format(label)))
        button.setGeometry(*geometry)
        button.enterEvent = self.wrap_event(label, 'down')
        button.leaveEvent = self.wrap_event(label, 'up')
        button.mouseReleaseEvent = getattr(self, method)

        setattr(self, label, button)

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

        self.path_label = QtGui.QLabel(self)
        self.path_label.setGeometry(22, 381, 189, 14)
        self.path_label.setText(os.getcwd() + '/Backups/')

        self.system_adb = QtGui.QLabel(self)
        self.system_adb.setPixmap(QtGui.QPixmap('img/adb_unchecked.png'))
        self.system_adb.setGeometry(10, 450, 272, 29)
        # self.system_adb.enterEvent = self.browse_enter
        # self.system_adb.leaveEvent = self.browse_leave
        self.system_adb.mouseReleaseEvent = self.adb_binary_change

        for label, settings in CONTROLS.iteritems():
            self.create_button(label, settings['geometry'], settings['trigger'])


def main():
    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
