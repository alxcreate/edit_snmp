import os
import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from snmp import *
import socket


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		self.setWindowTitle("Edit SNMP")
		self.setFixedSize(QSize(420, 300))

		self.ip = ''
		self.hostname = ''
		self.location = ''
		self.desc = ''
		self.ip_status = 'IP:'
		self.hostname_status = 'Hostname:'
		self.location_status = 'Location:'
		self.desc_status = 'Description:'
		self.hostname_oid = '1.3.6.1.2.1.1.5.0'
		self.location_oid = '1.3.6.1.2.1.1.6.0'
		self.desc_oid = '1.3.6.1.4.1.11.2.3.9.4.2.1.1.3.10.0'
		self.community_get = 'public'
		self.community_set = 'PrintsVB'

		# LAYOUTS
		self.layout = QVBoxLayout()
		self.layout.setContentsMargins(18, 18, 18, 18)
		self.layout.setSpacing(5)
		self.layout_ip = QHBoxLayout()
		self.layout_hostname = QHBoxLayout()
		self.layout_location = QHBoxLayout()
		self.layout_desc = QHBoxLayout()

		# ACTIVE ELEMENTS
		self.label_ip = QLabel(self.ip_status)
		self.line_ip = QLineEdit()
		self.line_ip.textEdited.connect(self.edit_ip)
		self.line_ip.setText(self.ip)
		self.button_ip_check = QPushButton('Check')
		self.button_ip_check.clicked.connect(self.ip_check)

		self.button_get_all = QPushButton('Get All')
		self.button_get_all.clicked.connect(self.get_all)
		self.button_set_all = QPushButton('Set All')
		self.button_set_all.clicked.connect(self.set_all)

		self.label_hostname = QLabel(self.hostname_status)
		self.line_hostname = QLineEdit()
		self.line_hostname.textEdited.connect(self.edit_hostname)
		self.line_hostname.setText(self.hostname)
		self.button_hostname_get = QPushButton('Get')
		self.button_hostname_get.clicked.connect(self.hostname_get)
		self.button_hostname_set = QPushButton('Set')
		self.button_hostname_set.clicked.connect(self.hostname_set)

		self.label_location = QLabel(self.location_status)
		self.line_location = QLineEdit()
		self.line_location.textEdited.connect(self.edit_location)
		self.line_location.setText(self.location)
		self.button_location_get = QPushButton('Get')
		self.button_location_get.clicked.connect(self.location_get)
		self.button_location_set = QPushButton('Set')
		self.button_location_set.clicked.connect(self.location_set)

		self.label_desc = QLabel(self.desc_status)
		self.line_desc = QLineEdit()
		self.line_desc.textEdited.connect(self.edit_desc)
		self.line_desc.setText(self.desc)
		self.button_desc_get = QPushButton('Get')
		self.button_desc_get.clicked.connect(self.desc_get)
		self.button_desc_set = QPushButton('Set')
		self.button_desc_set.clicked.connect(self.desc_set)

		# LAYOUT
		self.layout.addWidget(self.label_ip)
		self.layout.addLayout(self.layout_ip)

		self.layout_ip.addWidget(self.line_ip)
		self.layout_ip.addWidget(self.button_ip_check)
		self.layout_ip.addWidget(self.button_get_all)
		self.layout_ip.addWidget(self.button_set_all)

		self.layout.addWidget(self.label_hostname)
		self.layout.addLayout(self.layout_hostname)

		self.layout_hostname.addWidget(self.line_hostname)
		self.layout_hostname.addWidget(self.button_hostname_get)
		self.layout_hostname.addWidget(self.button_hostname_set)

		self.layout.addWidget(self.label_location)
		self.layout.addLayout(self.layout_location)

		self.layout_location.addWidget(self.line_location)
		self.layout_location.addWidget(self.button_location_get)
		self.layout_location.addWidget(self.button_location_set)

		self.layout.addWidget(self.label_desc)
		self.layout.addLayout(self.layout_desc)

		self.layout_desc.addWidget(self.line_desc)
		self.layout_desc.addWidget(self.button_desc_get)
		self.layout_desc.addWidget(self.button_desc_set)

		# END
		widget = QWidget()
		widget.setLayout(self.layout)
		self.setCentralWidget(widget)

	def edit_ip(self, ip):
		self.ip = ip
		print(self.ip)

	def edit_hostname(self, hostname):
		self.hostname = hostname
		print(self.hostname)

	def edit_location(self, location):
		self.location = location
		print(self.location)

	def edit_desc(self, desc):
		self.desc = desc
		print(self.desc)

	def ip_check(self):
		self.ip_status = 'IP: Processing...'
		self.label_ip.setText(self.ip_status)
		try:
			socket.inet_aton(self.ip)
			try:
				response = os.system("ping -c 1 " + self.ip)
				if response == 0:
					self.ip_status = 'IP: Ok'
					self.label_ip.setText(self.ip_status)
				else:
					self.ip_status = 'IP: Unavailable address'
					self.label_ip.setText(self.ip_status)
			except Exception:
				self.ip_status = 'IP: Error'
				self.label_ip.setText(self.ip_status)
		except socket.error:
			self.ip_status = 'IP: Incorrect address'
			self.label_ip.setText(self.ip_status)

	def get_all(self):
		self.hostname_get()
		self.location_get()
		self.desc_get()

	def set_all(self):
		self.hostname_set()
		self.location_set()
		self.desc_set()

	def line_hostname(self):
		print()

	def hostname_get(self):
		self.hostname_status = 'Hostname: Processing...'
		self.label_hostname.setText(self.hostname_status)
		try:
			self.hostname = snmp_get(self.ip, [self.hostname_oid], hlapi.CommunityData(self.community_get))
			for i in self.hostname.values():
				self.line_hostname.setText(i)
			self.hostname_status = 'Hostname: Ok'
			self.label_hostname.setText(self.hostname_status)
		except Exception:
			self.hostname_status = 'Hostname: Error'
			self.label_hostname.setText(self.hostname_status)
			self.line_hostname.setText('')

	def hostname_set(self):
		self.hostname_status = 'Hostname: Processing...'
		self.label_hostname.setText(self.hostname_status)
		try:
			snmp_set(self.ip, {self.hostname_oid: self.hostname}, hlapi.CommunityData(self.community_set))
			self.hostname_status = 'Hostname: Ok'
			self.label_hostname.setText(self.hostname_status)
		except Exception:
			self.hostname_status = 'Hostname: Error'
			self.label_hostname.setText(self.hostname_status)

	def line_location(self):
		print()

	def location_get(self):
		self.location_status = 'Location: Processing...'
		self.label_location.setText(self.location_status)
		try:
			self.location = snmp_get(self.ip, [self.location_oid], hlapi.CommunityData(self.community_get))
			for i in self.location.values():
				self.line_location.setText(i)
			self.location_status = 'Location: Ok'
			self.label_location.setText(self.location_status)
		except Exception:
			self.location_status = 'Location: Error'
			self.label_location.setText(self.location_status)
			self.line_location.setText('')

	def location_set(self):
		self.location_status = 'Location: Processing...'
		self.label_location.setText(self.location_status)
		try:
			snmp_set(self.ip, {self.location_oid: self.location}, hlapi.CommunityData(self.community_set))
			self.location_status = 'Location: Ok'
			self.label_location.setText(self.location_status)
		except Exception:
			self.location_status = 'Location: Error'
			self.label_location.setText(self.location_status)

	def line_desc(self):
		print()

	def desc_get(self):
		self.desc_status = 'Description: Processing...'
		self.label_desc.setText(self.desc_status)
		try:
			self.desc = snmp_get(self.ip, [self.desc_oid], hlapi.CommunityData(self.community_get))
			for i in self.desc.values():
				self.line_desc.setText(i)
			self.desc_status = 'Description: Ok'
			self.label_desc.setText(self.desc_status)
		except Exception:
			self.desc_status = 'Description: Error'
			self.label_desc.setText(self.desc_status)
			self.line_desc.setText('')

	def desc_set(self):
		self.desc_status = 'Description: Processing...'
		self.label_desc.setText(self.desc_status)
		try:
			snmp_set(self.ip, {self.desc_oid: self.desc}, hlapi.CommunityData(self.community_set))
			self.desc_status = 'Description: Ok'
			self.label_desc.setText(self.desc_status)
		except Exception:
			self.desc_status = 'Description: Error'
			self.label_desc.setText(self.desc_status)

	def state(self):
		print()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()