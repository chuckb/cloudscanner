class ScanDestination(object):
	def __init__(self, name=""):
		self.name = name

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		self._name = value

class EmailScanDestination(ScanDestination):
	def __init__(self, name = "", address = ""):
		super(EmailScanDestination, self).__init__(name)
		self.address = address

	@property
	def address(self):
		return self._address

	@address.setter
	def address(self, value):
		self._address = value
