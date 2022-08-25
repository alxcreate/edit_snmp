import os
import sys
import datetime
import threading
import time

# from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from snmp import *
import socket


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Edit SNMP")
        # self.setFixedSize(QSize(400, 500))

        self.community_get = 'public'
        self.community_set = 'private'
        self.ip = '10.6.8.139'
        self.descr = ''
        self.object_id = ''
        self.uptime = ''
        self.contact = ''
        self.name = ''
        self.location = ''

        self.descr_oid = '1.3.6.1.2.1.1.1.0'
        self.object_id_oid = '1.3.6.1.2.1.1.2.0'
        self.uptime_oid = '1.3.6.1.2.1.1.3.0'
        self.contact_oid = '1.3.6.1.2.1.1.4.0'
        self.name_oid = '1.3.6.1.2.1.1.5.0'
        self.location_oid = '1.3.6.1.2.1.1.6.0'

        self.label_community_get = 'Community Get:'
        self.label_community_set = 'Community Set:'
        self.label_ip_title = 'IP:'
        self.label_descr_title = 'Description:'
        self.label_object_id_title = 'Object ID:'
        self.label_uptime_title = 'Uptime:'
        self.label_contact_title = 'Contact:'
        self.label_name_title = 'Name:'
        self.label_location_title = 'Location:'

        self.label_status_incorrect = 'Incorrect'
        self.label_status_unavailable = 'Unavailable'
        self.label_status_wait = 'Wait...'
        self.label_status_ok = 'Ok'
        self.label_status_error = 'Error'

        self.button_check = 'Check'
        self.button_get_all = 'Get All'
        self.button_set_all = 'Set All'
        self.button_get = 'Get'
        self.button_set = 'Set'

        # ELEMENTS
        self.label_community_get = QLabel(self.label_community_get)

        self.label_community_set = QLabel(self.label_community_set)

        self.line_community_get = QLineEdit()
        self.line_community_get.textEdited.connect(self.edit_community_get)
        self.line_community_get.setText(self.community_get)

        self.line_community_set = QLineEdit()
        self.line_community_set.textEdited.connect(self.edit_community_set)
        self.line_community_set.setText(self.community_set)
        ###################
        self.label_ip = QLabel(self.label_ip_title)

        self.line_ip = QLineEdit()
        self.line_ip.textEdited.connect(self.edit_ip)
        self.line_ip.setText(self.ip)

        self.button_get_all = QPushButton(self.button_get_all)
        self.button_get_all.clicked.connect(self.get_all)

        self.button_set_all = QPushButton(self.button_set_all)
        self.button_set_all.clicked.connect(self.set_all)

        self.button_ip_check = QPushButton(self.button_check)
        self.button_ip_check.clicked.connect(self.ip_check)
        ###################
        self.label_descr = QLabel(self.label_descr_title)

        self.line_descr = QLineEdit()
        self.line_descr.textEdited.connect(self.edit_descr)
        self.line_descr.setText(self.descr)

        self.button_descr_get = QPushButton(self.button_get)
        self.button_descr_get.clicked.connect(self.descr_get)
        ###################
        self.label_object_id = QLabel(self.label_object_id_title)

        self.line_object_id = QLineEdit()
        self.line_object_id.textEdited.connect(self.edit_object_id)
        self.line_object_id.setText(self.object_id)

        self.button_object_id_get = QPushButton(self.button_get)
        self.button_object_id_get.clicked.connect(self.object_id_get)
        ###################
        self.label_uptime = QLabel(self.label_uptime_title)

        self.line_uptime = QLineEdit()
        self.line_uptime.textEdited.connect(self.edit_uptime)
        self.line_uptime.setText(self.uptime)

        self.button_uptime_get = QPushButton(self.button_get)
        self.button_uptime_get.clicked.connect(self.uptime_get)
        ###################
        self.label_contact = QLabel(self.label_contact_title)

        self.line_contact = QLineEdit()
        self.line_contact.textEdited.connect(self.edit_contact)
        self.line_contact.setText(self.contact)

        self.button_contact_get = QPushButton(self.button_get)
        self.button_contact_get.clicked.connect(self.contact_get)

        self.button_contact_set = QPushButton(self.button_set)
        self.button_contact_set.clicked.connect(self.contact_set)
        ###################
        self.label_name = QLabel(self.label_name_title)

        self.line_name = QLineEdit()
        self.line_name.textEdited.connect(self.edit_name)
        self.line_name.setText(self.name)

        self.button_name_get = QPushButton(self.button_get)
        self.button_name_get.clicked.connect(self.name_get)

        self.button_name_set = QPushButton(self.button_set)
        self.button_name_set.clicked.connect(self.name_set)
        ###################
        self.label_location = QLabel(self.label_location_title)

        self.line_location = QLineEdit()
        self.line_location.textEdited.connect(self.edit_location)
        self.line_location.setText(self.location)

        self.button_location_get = QPushButton(self.button_get)
        self.button_location_get.clicked.connect(self.location_get)

        self.button_location_set = QPushButton(self.button_set)
        self.button_location_set.clicked.connect(self.location_set)

        # LAYOUT
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(18, 18, 18, 18)
        self.layout.setSpacing(5)

        self.layout_community = QGridLayout()
        self.layout_community.setColumnMinimumWidth(0, 90)
        self.layout_community.setColumnMinimumWidth(2, 90)
        self.layout_community.setContentsMargins(0, 0, 0, 10)
        self.layout.addLayout(self.layout_community)

        self.layout_community.addWidget(self.label_community_get, 0, 0)
        self.layout_community.addWidget(self.label_community_set, 0, 2)
        self.layout_community.addWidget(self.line_community_get, 0, 1)
        self.layout_community.addWidget(self.line_community_set, 0, 3)

        self.layout_body = QGridLayout()
        self.layout_body.setColumnMinimumWidth(0, 100)
        self.layout_body.setColumnMinimumWidth(1, 300)
        self.layout.addLayout(self.layout_body)

        self.layout_body.addWidget(self.label_ip, 1, 0)
        self.layout_body.addWidget(self.line_ip, 1, 1)
        self.layout_body.addWidget(self.button_get_all, 1, 2)
        self.layout_body.addWidget(self.button_set_all, 1, 3)
        self.layout_body.addWidget(self.button_ip_check, 1, 4)

        self.layout_body.addWidget(self.label_descr, 2, 0)
        self.layout_body.addWidget(self.line_descr, 2, 1)
        self.layout_body.addWidget(self.button_descr_get, 2, 2)

        self.layout_body.addWidget(self.label_object_id, 3, 0)
        self.layout_body.addWidget(self.line_object_id, 3, 1)
        self.layout_body.addWidget(self.button_object_id_get, 3, 2)

        self.layout_body.addWidget(self.label_uptime, 4, 0)
        self.layout_body.addWidget(self.line_uptime, 4, 1)
        self.layout_body.addWidget(self.button_uptime_get, 4, 2)

        self.layout_body.addWidget(self.label_contact, 5, 0)
        self.layout_body.addWidget(self.line_contact, 5, 1)
        self.layout_body.addWidget(self.button_contact_get, 5, 2)
        self.layout_body.addWidget(self.button_contact_set, 5, 3)

        self.layout_body.addWidget(self.label_name, 6, 0)
        self.layout_body.addWidget(self.line_name, 6, 1)
        self.layout_body.addWidget(self.button_name_get, 6, 2)
        self.layout_body.addWidget(self.button_name_set, 6, 3)

        self.layout_body.addWidget(self.label_location, 7, 0)
        self.layout_body.addWidget(self.line_location, 7, 1)
        self.layout_body.addWidget(self.button_location_get, 7, 2)
        self.layout_body.addWidget(self.button_location_set, 7, 3)

        # END
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def edit_community_get(self, community_get):
        self.community_get = community_get

    def edit_community_set(self, community_set):
        self.community_set = community_set

    def edit_ip(self, ip):
        self.ip = ip

    def edit_descr(self, descr):
        self.descr = descr

    def edit_object_id(self, object_id):
        self.object_id = object_id

    def edit_uptime(self, uptime):
        self.uptime = uptime

    def edit_contact(self, contact):
        self.contact = contact

    def edit_name(self, name):
        self.name = name

    def edit_location(self, location):
        self.location = location

    def get_all(self):
        # self.label_ip.setText(f'{self.label_ip_title} {self.label_status_wait}')
        self.descr_get()
        self.object_id_get()
        self.uptime_get()
        self.contact_get()
        self.name_get()
        self.location_get()

    def set_all(self):
        self.contact_set()
        self.name_set()
        self.location_set()

    def ip_check(self):
        self.label_ip.setText(f'{self.label_ip_title} {self.label_status_wait}')
        try:
            socket.inet_aton(self.ip)
            try:
                response = os.system("ping -c 1 -W 1 " + self.ip)
                if response == 0:
                    self.label_ip.setText(f'{self.label_ip_title} {self.label_status_ok}')
                else:
                    self.label_ip.setText(f'{self.label_ip_title} {self.label_status_unavailable}')
            except Exception:
                self.label_ip.setText(f'{self.label_ip_title} {self.label_status_error}')
        except socket.error:
            self.label_ip.setText(f'{self.label_ip_title} {self.label_status_incorrect}')

    def descr_get(self):
        self.label_descr.setText(f'{self.label_descr_title} {self.label_status_wait}')
        try:
            self.descr = snmp_get(self.ip, [self.descr_oid], CommunityData(self.community_get))
            for i in self.descr.values():
                self.line_descr.setText(str(i))
            self.label_descr.setText(f'{self.label_descr_title} {self.label_status_ok}')
        except Exception:
            self.line_descr.setText('')
            self.label_descr.setText(f'{self.label_descr_title} {self.label_status_error}')

    def object_id_get(self):
        self.label_object_id.setText(f'{self.label_object_id_title} {self.label_status_wait}')
        try:
            self.object_id = snmp_get(self.ip, [self.object_id_oid], CommunityData(self.community_get))
            for i in self.object_id.values():
                self.line_object_id.setText(str(i))
            self.label_object_id.setText(f'{self.label_object_id_title} {self.label_status_ok}')
        except Exception:
            self.line_object_id.setText('')
            self.label_object_id.setText(f'{self.label_object_id_title} {self.label_status_error}')

    def uptime_get(self):
        self.label_uptime.setText(f'{self.label_uptime_title} {self.label_status_wait}')
        try:
            self.uptime = snmp_get(self.ip, [self.uptime_oid], CommunityData(self.community_get))
            for i in self.uptime.values():
                self.line_uptime.setText(str(datetime.timedelta(seconds=(round(i / 100, 0)))))
            self.label_uptime.setText(f'{self.label_uptime_title} {self.label_status_ok}')
        except Exception:
            self.line_uptime.setText('')
            self.label_uptime.setText(f'{self.label_uptime_title} {self.label_status_error}')

    def contact_get(self):
        self.label_contact.setText(f'{self.label_contact_title} {self.label_status_wait}')
        try:
            self.contact = snmp_get(self.ip, [self.contact_oid], CommunityData(self.community_get))
            for i in self.contact.values():
                self.line_contact.setText(str(i))
            self.label_contact.setText(f'{self.label_contact_title} {self.label_status_ok}')
        except Exception:
            self.line_contact.setText('')
            self.label_contact.setText(f'{self.label_contact_title} {self.label_status_error}')

    def contact_set(self):
        self.label_contact.setText(f'{self.label_contact_title} {self.label_status_wait}')
        try:
            snmp_set(self.ip, {self.contact_oid: self.contact}, CommunityData(self.community_set))
            self.label_contact.setText(f'{self.label_contact_title} {self.label_status_ok}')
        except Exception:
            self.label_contact.setText(f'{self.label_contact_title} {self.label_status_error}')

    def name_get(self):
        self.label_name.setText(f'{self.label_name_title} {self.label_status_wait}')
        try:
            self.name = snmp_get(self.ip, [self.name_oid], CommunityData(self.community_get))
            for i in self.name.values():
                self.line_name.setText(str(i))
            self.label_name.setText(f'{self.label_name_title} {self.label_status_ok}')
        except Exception:
            self.line_name.setText('')
            self.label_name.setText(f'{self.label_name_title} {self.label_status_error}')

    def name_set(self):
        self.label_name.setText(f'{self.label_name_title} {self.label_status_wait}')
        try:
            snmp_set(self.ip, {self.name_oid: self.name}, CommunityData(self.community_set))
            self.label_name.setText(f'{self.label_name_title} {self.label_status_ok}')
        except Exception:
            self.label_name.setText(f'{self.label_name_title} {self.label_status_error}')

    def location_get(self):
        self.label_location.setText(f'{self.label_location_title} {self.label_status_wait}')
        try:
            self.location = snmp_get(self.ip, [self.location_oid], CommunityData(self.community_get))
            for i in self.location.values():
                self.line_location.setText(str(i))
            self.label_location.setText(f'{self.label_location_title} {self.label_status_ok}')
        except Exception:
            self.line_location.setText('')
            self.label_location.setText(f'{self.label_location_title} {self.label_status_error}')

    def location_set(self):
        self.label_location.setText(f'{self.label_location_title} {self.label_status_wait}')
        try:
            snmp_set(self.ip, {self.location_oid: self.location}, CommunityData(self.community_set))
            self.label_location.setText(f'{self.label_location_title} {self.label_status_ok}')
        except Exception:
            self.label_location.setText(f'{self.label_location_title} {self.label_status_error}')


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
