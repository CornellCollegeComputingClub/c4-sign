# from c4_sign.lib.liquidcrystal.base import LiquidCrystalBase
from base import LiquidCrystalBase


class SimulatedLCD(LiquidCrystalBase):
    pass


if __name__ == "__main__":
    s = SimulatedLCD(2, 16)
