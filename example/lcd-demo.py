import lcddriver
from time import *

lcd = lcddriver.lcd()
lcd.clear()

lcd.display_string("Cornell Physics ", 1)
lcd.display_string("and Engineering ", 2)
