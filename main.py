import os
import sys
import time

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from snmp import *
import socket


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		self.setWindowTitle("Edit SNMP")
		self.setFixedSize(QSize(400, 500))

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

		self.label_status_ip_incorrect = 'Incorrect address'
		self.label_status_ip_unavailable = 'Unavailable address'
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

		self.button_ip_check = QPushButton(self.button_check)
		self.button_ip_check.clicked.connect(self.ip_check)

		self.button_get_all = QPushButton(self.button_get_all)
		self.button_get_all.clicked.connect(self.get_all)

		self.button_set_all = QPushButton(self.button_set_all)
		self.button_set_all.clicked.connect(self.set_all)
		###################
		self.label_descr = QLabel(self.label_descr_title)

		self.line_descr = QLineEdit()
		self.line_descr.textEdited.connect(self.edit_descr)
		self.line_descr.setText(self.descr)

		self.button_descr_get = QPushButton(self.button_get)
		self.button_descr_get.clicked.connect(self.descr_get)

		self.button_descr_set = QPushButton(self.button_set)
		self.button_descr_set.clicked.connect(self.descr_set)
		###################
		self.label_object_id = QLabel(self.label_object_id_title)

		self.line_object_id = QLineEdit()
		self.line_object_id.textEdited.connect(self.edit_object_id)
		self.line_object_id.setText(self.object_id)

		self.button_object_id_get = QPushButton(self.button_get)
		self.button_object_id_get.clicked.connect(self.object_id_get)

		self.button_object_id_set = QPushButton(self.button_set)
		self.button_object_id_set.clicked.connect(self.object_id_set)
		###################
		self.label_uptime = QLabel(self.label_uptime_title)

		self.line_uptime = QLineEdit()
		self.line_uptime.textEdited.connect(self.edit_uptime)
		self.line_uptime.setText(self.uptime)

		self.button_uptime_get = QPushButton(self.button_get)
		self.button_uptime_get.clicked.connect(self.uptime_get)

		self.button_uptime_set = QPushButton(self.button_set)
		self.button_uptime_set.clicked.connect(self.uptime_set)
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
		self.layout_community.setContentsMargins(0, 0, 0, 10)
		self.layout.addLayout(self.layout_community)
		self.layout_community.addWidget(self.label_community_get, 0, 0)
		self.layout_community.addWidget(self.label_community_set, 0, 1)
		self.layout_community.addWidget(self.line_community_get, 1, 0)
		self.layout_community.addWidget(self.line_community_set, 1, 1)

		self.layout_ip = QHBoxLayout()
		self.layout.addWidget(self.label_ip)
		self.layout.addLayout(self.layout_ip)
		self.layout_ip.addWidget(self.line_ip)
		self.layout_ip.addWidget(self.button_ip_check)
		self.layout_ip.addWidget(self.button_get_all)
		self.layout_ip.addWidget(self.button_set_all)

		self.layout_descr = QHBoxLayout()
		self.layout.addWidget(self.label_descr)
		self.layout.addLayout(self.layout_descr)
		self.layout_descr.addWidget(self.line_descr)
		self.layout_descr.addWidget(self.button_descr_get)
		self.layout_descr.addWidget(self.button_descr_set)

		self.layout_object_id = QHBoxLayout()
		self.layout.addWidget(self.label_object_id)
		self.layout.addLayout(self.layout_object_id)
		self.layout_object_id.addWidget(self.line_object_id)
		self.layout_object_id.addWidget(self.button_object_id_get)
		self.layout_object_id.addWidget(self.button_object_id_set)

		self.layout_uptime = QHBoxLayout()
		self.layout.addWidget(self.label_uptime)
		self.layout.addLayout(self.layout_uptime)
		self.layout_uptime.addWidget(self.line_uptime)
		self.layout_uptime.addWidget(self.button_uptime_get)
		self.layout_uptime.addWidget(self.button_uptime_set)

		self.layout_contact = QHBoxLayout()
		self.layout.addWidget(self.label_contact)
		self.layout.addLayout(self.layout_contact)
		self.layout_contact.addWidget(self.line_contact)
		self.layout_contact.addWidget(self.button_contact_get)
		self.layout_contact.addWidget(self.button_contact_set)

		self.layout_name = QHBoxLayout()
		self.layout.addWidget(self.label_name)
		self.layout.addLayout(self.layout_name)
		self.layout_name.addWidget(self.line_name)
		self.layout_name.addWidget(self.button_name_get)
		self.layout_name.addWidget(self.button_name_set)

		self.layout_location = QHBoxLayout()
		self.layout.addWidget(self.label_location)
		self.layout.addLayout(self.layout_location)
		self.layout_location.addWidget(self.line_location)
		self.layout_location.addWidget(self.button_location_get)
		self.layout_location.addWidget(self.button_location_set)

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

	def ip_check(self):
		self.label_ip.setText(f'{self.label_ip_title} {self.label_status_wait}')
		try:
			socket.inet_aton(self.ip)
			try:
				response = os.system("ping -c 1 " + self.ip)
				if response == 0:
					self.label_ip.setText(f'{self.label_ip_title} {self.label_status_ok}')
				else:
					self.label_ip.setText(f'{self.label_ip_title} {self.label_status_ip_unavailable}')
			except Exception:
				self.label_ip.setText(f'{self.label_ip_title} {self.label_status_error}')
		except socket.error:
			self.label_ip.setText(f'{self.label_ip_title} {self.label_status_ip_incorrect}')

	def get_all(self):
		self.descr_get()
		self.object_id_get()
		self.uptime_get()
		self.contact_get()
		self.name_get()
		self.location_get()

	def set_all(self):
		self.descr_set()
		self.object_id_set()
		self.uptime_set()
		self.contact_set()
		self.name_set()
		self.location_set()

	def descr_get(self):
		self.label_descr.setText(f'{self.label_descr_title} {self.label_status_wait}')
		try:
			self.descr = snmp_get(self.ip, [self.descr_oid], hlapi.CommunityData(self.community_get))
			for i in self.descr.values():
				self.line_descr.setText(str(i))
			self.label_descr.setText(f'{self.label_descr_title} {self.label_status_ok}')
		except Exception:
			self.line_descr.setText('')
			self.label_descr.setText(f'{self.label_descr_title} {self.label_status_error}')

	def descr_set(self):
		self.label_descr.setText(f'{self.label_descr_title} {self.label_status_wait}')
		try:
			snmp_set(self.ip, {self.descr_oid: self.descr}, hlapi.CommunityData(self.community_set))
			self.label_descr.setText(f'{self.label_descr_title} {self.label_status_ok}')
		except Exception:
			self.label_descr.setText(f'{self.label_descr_title} {self.label_status_error}')

	def object_id_get(self):
		self.label_object_id.setText(f'{self.label_object_id_title} {self.label_status_wait}')
		try:
			self.object_id = snmp_get(self.ip, [self.object_id_oid], hlapi.CommunityData(self.community_get))
			for i in self.object_id.values():
				self.line_object_id.setText(str(i))
			self.label_object_id.setText(f'{self.label_object_id_title} {self.label_status_ok}')
		except Exception:
			self.line_object_id.setText('')
			self.label_object_id.setText(f'{self.label_object_id_title} {self.label_status_error}')

	def object_id_set(self):
		self.label_object_id.setText(f'{self.label_object_id_title} {self.label_status_wait}')
		try:
			snmp_set(self.ip, {self.object_id_oid: self.object_id}, hlapi.CommunityData(self.community_set))
			self.label_object_id.setText(f'{self.label_object_id_title} {self.label_status_ok}')
		except Exception:
			self.label_object_id.setText(f'{self.label_object_id_title} {self.label_status_error}')

	def uptime_get(self):
		self.label_uptime.setText(f'{self.label_uptime_title} {self.label_status_wait}')
		try:
			self.uptime = snmp_get(self.ip, [self.uptime_oid], hlapi.CommunityData(self.community_get))
			for i in self.uptime.values():
				# self.line_uptime.setText(str(i/100))
				self.line_uptime.setText(time.strftime("%Y %H:%M:%S", time.gmtime(i/100)))
			self.label_uptime.setText(f'{self.label_uptime_title} {self.label_status_ok}')
		except Exception:
			self.line_uptime.setText('')
			self.label_uptime.setText(f'{self.label_uptime_title} {self.label_status_error}')

	def uptime_set(self):
		self.label_uptime.setText(f'{self.label_uptime_title} {self.label_status_wait}')
		try:
			snmp_set(self.ip, {self.uptime_oid: self.uptime}, hlapi.CommunityData(self.community_set))
			self.label_uptime.setText(f'{self.label_uptime_title} {self.label_status_ok}')
		except Exception:
			self.label_uptime.setText(f'{self.label_uptime_title} {self.label_status_error}')

	def contact_get(self):
		self.label_contact.setText(f'{self.label_contact_title} {self.label_status_wait}')
		try:
			self.contact = snmp_get(self.ip, [self.contact_oid], hlapi.CommunityData(self.community_get))
			for i in self.contact.values():
				self.line_contact.setText(str(i))
			self.label_contact.setText(f'{self.label_contact_title} {self.label_status_ok}')
		except Exception:
			self.line_contact.setText('')
			self.label_contact.setText(f'{self.label_contact_title} {self.label_status_error}')

	def contact_set(self):
		self.label_contact.setText(f'{self.label_contact_title} {self.label_status_wait}')
		try:
			snmp_set(self.ip, {self.contact_oid: str(self.contact)}, hlapi.CommunityData(self.community_set))
			self.label_contact.setText(f'{self.label_contact_title} {self.label_status_ok}')
		except Exception:
			self.label_contact.setText(f'{self.label_contact_title} {self.label_status_error}')

	def name_get(self):
		self.label_name.setText(f'{self.label_name_title} {self.label_status_wait}')
		try:
			self.name = snmp_get(self.ip, [self.name_oid], hlapi.CommunityData(self.community_get))
			for i in self.name.values():
				self.line_name.setText(str(i))
			self.label_name.setText(f'{self.label_name_title} {self.label_status_ok}')
		except Exception:
			self.line_name.setText('')
			self.label_name.setText(f'{self.label_name_title} {self.label_status_error}')

	def name_set(self):
		self.label_name.setText(f'{self.label_name_title} {self.label_status_wait}')
		try:
			snmp_set(self.ip, {self.name_oid: self.name}, hlapi.CommunityData(self.community_set))
			self.label_name.setText(f'{self.label_name_title} {self.label_status_ok}')
		except Exception:
			self.label_name.setText(f'{self.label_name_title} {self.label_status_error}')

	def location_get(self):
		self.label_location.setText(f'{self.label_location_title} {self.label_status_wait}')
		try:
			self.location = snmp_get(self.ip, [self.location_oid], hlapi.CommunityData(self.community_get))
			for i in self.location.values():
				self.line_location.setText(str(i))
			self.label_location.setText(f'{self.label_location_title} {self.label_status_ok}')
		except Exception:
			self.line_location.setText('')
			self.label_location.setText(f'{self.label_location_title} {self.label_status_error}')

	def location_set(self):
		self.label_location.setText(f'{self.label_location_title} {self.label_status_wait}')
		try:
			snmp_set(self.ip, {self.location_oid: self.location}, hlapi.CommunityData(self.community_set))
			self.label_location.setText(f'{self.label_location_title} {self.label_status_ok}')
		except Exception:
			self.label_location.setText(f'{self.label_location_title} {self.label_status_error}')


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
