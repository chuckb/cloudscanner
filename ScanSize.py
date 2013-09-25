class ScanSize(object):
	# Sizes are in millimeters
	# 1 inch = 25.4 millimeters
	def __init__(self, name="", x=0, y=0):
		self.name = name
		self.x = x
		self.y = y

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		self._name = value

	@property
	def x(self):
		return self._x

	@x.setter
	def x(self, value):
		self._x = value

	@property
	def y(self):
		return self._y

	@y.setter
	def y(self, value):
		self._y = value
