import neopixel
import machine
import time


class ZrhLedBoard:
    def __init__(self) -> None:
        self.led_num = 10
        # 初始化NeoPixel
        self.np = neopixel.NeoPixel(machine.Pin(18), self.led_num)
        self.default_color = (100, 100, 10)

    def on_led(self, color):
        print("color:", color)
        if color:
            self.np.fill(color)
        else:
            self.np.fill(self.color)
        self.np.write()

    def off_led(self):
        self.np.fill((0, 0, 0))
        self.np.write()
