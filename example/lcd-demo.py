import lcddriver
from time import *

lcd = lcddriver.lcd()
lcd.lcd_clear()

lcd.lcd_display_string("Cornell Physics ", 1)
lcd.lcd_display_string("and Engineering ", 2)
