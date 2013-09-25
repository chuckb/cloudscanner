#!/usr/bin/python

# Import libraries
import RPIO as GPIO
from MyCharLCD import MyCharLCD
from ScanDestination import *
from ScanSize import *
from MailUtil import *
import subprocess
import logging
import time

# Setup constants
WHITE_BUTTON = 11
BLUE_BUTTON = 9
BLACK_BUTTON = 10
GREEN_BUTTON = 7
# TODO: These mail constants should be persisted
GMAIL_USER = "<put your gmail address here>"
GMAIL_PASSWORD = "<put your gmail password here>"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
BACKLIGHT_TIMEOUT = 30
LOG_FILE = "/tmp/scan.log"
# Hard-code destinations
# TODO: Put this in a persistent YAML file
destinations = []
destinations.append(EmailScanDestination("<mail name to display on Pi>", "<mail destination address goes here>"))
# destinations.append(...) add as many as you need

destination = 0
# Hard-code sizes
# TODO: Persist this stuff too?  Maybe not...
sizes = []
sizes.append(ScanSize("Letter", 210, 280))
sizes.append(ScanSize("Legal", 210, 356))
size = 0
logging.basicConfig(level=logging.DEBUG, filename=LOG_FILE)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

lcd = MyCharLCD(pin_rs=25, pin_rw=None, pin_e=24, pins_data=[23, 17, 27, 22],
              numbering_mode=GPIO.BCM,
              cols=16, rows=2, pin_backlight=4)

mailutil = MailUtil(GMAIL_USER, GMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT)

# Set up buttons as an input, pulled down, connected to 3V3 on button press  
GPIO.setup(WHITE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.setup(BLUE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.setup(BLACK_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.setup(GREEN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  

# Define menus and interrupt handlers
def main_scan_green_callback(channel, value):
	if not lcd.backlight_is_on():
		lcd.backlight_on()
		lcd.set_backlight_timer(BACKLIGHT_TIMEOUT)
	else:
		lcd.clear()
		lcd.backlight_on()
		lcd.kill_backlight_timer()
		lcd.write_string('Scanning...')
		# TODO: scanning and pdfing should be busted up into python function
		# for more granular control
		try:
			# Scan doc to tmp directory
			# Then email it to current destination
			with open(LOG_FILE, 'w') as f:
				rc = subprocess.call(['./scan2pdf', '99', 'document', 
					str(sizes[size].x), str(sizes[size].y)], stdout=f, stderr=f)
			lcd.clear()
			lcd.write_string('Sending...')
			mailutil.mail_with_attachment(destinations[destination].address, 
				'Cloudscan Document', '', '/tmp/document.pdf')
		except:
			lcd.clear()
			lcd.write_string('Failed!')
			logging.exception("Failure scanning or sending document:")
			time.sleep(5)
		main_menu()

def dest_ok_green_callback(channel, value):
	if not lcd.backlight_is_on():
		lcd.backlight_on()
		lcd.set_backlight_timer(BACKLIGHT_TIMEOUT)
	else:
		main_menu()

def size_ok_green_callback(channel, value):
	if not lcd.backlight_is_on():
		lcd.backlight_on()
		lcd.set_backlight_timer(BACKLIGHT_TIMEOUT)
	else:
		main_menu()

def main_dest_white_callback(channel, value):
	dest_menu()

def dest_prev_white_callback(channel, value):
	dest_prev()

def size_prev_white_callback(channel, value):
	size_prev()

def main_size_blue_callback(channel, value):
	size_menu()

def dest_next_blue_callback(channel, value):
	dest_next()

def size_next_blue_callback(channel, value):
	size_next()

def main_menu():
	lcd.clear()
	lcd.write_string('Ready\n\rScn Dst Sze')
	lcd.backlight_on()
	lcd.set_backlight_timer(BACKLIGHT_TIMEOUT)
	try:
		GPIO.del_interrupt_callback(GREEN_BUTTON)
	except:
		pass
	finally:
		GPIO.add_interrupt_callback(GREEN_BUTTON, main_scan_green_callback, 'rising', debounce_timeout_ms=300)
	try:
		GPIO.del_interrupt_callback(WHITE_BUTTON)
	except:
		pass
	finally:
		GPIO.add_interrupt_callback(WHITE_BUTTON, main_dest_white_callback, 'rising', debounce_timeout_ms=300)
	try:
		GPIO.del_interrupt_callback(BLUE_BUTTON)
	except:
		pass
	finally:
		GPIO.add_interrupt_callback(BLUE_BUTTON, main_size_blue_callback, 'rising', debounce_timeout_ms=300)
	try:
		GPIO.del_interrupt_callback(BLACK_BUTTON)
	except:
		pass

def dest_menu():
	lcd.clear()
	lcd.write_string(destinations[destination].name)
	lcd.write_string("\n\rOK Prv Nxt")
	lcd.backlight_on()
	lcd.set_backlight_timer(BACKLIGHT_TIMEOUT)
	try:
		GPIO.del_interrupt_callback(GREEN_BUTTON)
	except:
		pass
	finally:
		GPIO.add_interrupt_callback(GREEN_BUTTON, dest_ok_green_callback, 'rising', debounce_timeout_ms=300)
	try:
		GPIO.del_interrupt_callback(WHITE_BUTTON)
	except:
		pass
	finally:
		GPIO.add_interrupt_callback(WHITE_BUTTON, dest_prev_white_callback, 'rising', debounce_timeout_ms=300)
	try:
		GPIO.del_interrupt_callback(BLUE_BUTTON)
	except:
		pass
	finally:
		GPIO.add_interrupt_callback(BLUE_BUTTON, dest_next_blue_callback, 'rising', debounce_timeout_ms=300)
	try:
		GPIO.del_interrupt_callback(BLACK_BUTTON)
	except:
		pass
	
def dest_prev():
	global destination
	destination = destination - 1
	if destination < 0:
		destination = len(destinations) - 1 
	dest_menu()

def dest_next():
	global destination
	destination = destination + 1
	if destination >= len(destinations):
		destination = 0 
	dest_menu()

def size_menu():
	lcd.clear()
	lcd.write_string(sizes[size].name)
	lcd.write_string("\n\rOK Prv Nxt")
	lcd.backlight_on()
	lcd.set_backlight_timer(BACKLIGHT_TIMEOUT)
	try:
		GPIO.del_interrupt_callback(GREEN_BUTTON)
	except:
		pass
	finally:
		GPIO.add_interrupt_callback(GREEN_BUTTON, size_ok_green_callback, 'rising', debounce_timeout_ms=300)
	try:
		GPIO.del_interrupt_callback(WHITE_BUTTON)
	except:
		pass
	finally:
		GPIO.add_interrupt_callback(WHITE_BUTTON, size_prev_white_callback, 'rising', debounce_timeout_ms=300)
	try:
		GPIO.del_interrupt_callback(BLUE_BUTTON)
	except:
		pass
	finally:
		GPIO.add_interrupt_callback(BLUE_BUTTON, size_next_blue_callback, 'rising', debounce_timeout_ms=300)
	try:
		GPIO.del_interrupt_callback(BLACK_BUTTON)
	except:
		pass

def size_prev():
	global size 
	size = size - 1
	if size < 0:
		size = len(sizes) - 1 
	size_menu()

def size_next():
	global size
	size = size + 1
	if size >= len(sizes):
		size = 0 
	size_menu()

# Kick off main menu processing and then wait for buttons to be pushed
try:
	main_menu()
	GPIO.wait_for_interrupts()
except:
	pass

# After an exception (which is usually a ctrl-c interrupt), clean up and end
lcd.clear()
lcd.backlight_off()
GPIO.cleanup()
