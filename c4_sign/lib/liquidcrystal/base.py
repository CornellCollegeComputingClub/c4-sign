from abc import ABC, abstractmethod

# i'm just copying the interface from the arduino library
# see: https://www.arduino.cc/en/Reference/LiquidCrystal
# and:
# https://github.com/johnrickman/LiquidCrystal_I2C/tree/master
# TODO: more pythonic! but that can happen way later.


class LiquidCrystalBase(ABC):
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    @abstractmethod
    def begin(self, cols, rows):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def home(self):
        pass

    @abstractmethod
    def setCursor(self, col, row):
        pass

    @abstractmethod
    def noDisplay(self):
        pass

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def noBlink(self):
        pass

    @abstractmethod
    def blink(self):
        pass

    @abstractmethod
    def noCursor(self):
        pass

    @abstractmethod
    def cursor(self):
        pass

    @abstractmethod
    def scrollDisplayLeft(self):
        pass

    @abstractmethod
    def scrollDisplayRight(self):
        pass

    @abstractmethod
    def leftToRight(self):
        pass

    @abstractmethod
    def rightToLeft(self):
        pass

    @abstractmethod
    def autoscroll(self):
        pass

    @abstractmethod
    def noAutoscroll(self):
        pass

    @abstractmethod
    def createChar(self, location, charmap):
        pass
