import RPIO
from RPLCD import CharLCD
from ResettableTimer import ResettableTimer

class MyCharLCD(CharLCD):
	def __init__(self, pin_rs=15, pin_rw=18, pin_e=16, pins_data=[21, 22, 23, 24],
                       numbering_mode=RPIO.BOARD,
                       cols=20, rows=4, dotsize=8, pin_backlight=None):  
		super(MyCharLCD, self).__init__(pin_rs, pin_rw, pin_e,
			pins_data, numbering_mode, cols, rows, dotsize)
		self.pin_backlight = pin_backlight
		RPIO.setup(pin_backlight, RPIO.OUT)

	def backlight_on(self):
		if self.pin_backlight is not None:
			RPIO.output(self.pin_backlight, 1)

	def backlight_off(self):
		if self.pin_backlight is not None:
			RPIO.output(self.pin_backlight, 0)

	def backlight_is_on(self):
		if self.pin_backlight is not None:
			return RPIO.input(self.pin_backlight)
		return 0

	def set_backlight_timer(self, off_in_seconds):
		try:
			self.backlight_timer.max_time = off_in_seconds
			self.backlight_timer.reset()
		except AttributeError:
			self.backlight_timer = ResettableTimer(off_in_seconds, self.backlight_off, 1)
			self.backlight_timer.start()

	def kill_backlight_timer(self):
		self.backlight_timer.deactivate()
