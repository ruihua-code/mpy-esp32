import neopixel
import machine
import time


class ZrhLedBoard:
    def __init__(self) -> None:
        self.led_num = 10
        # 初始化NeoPixel
        self.np = neopixel.NeoPixel(machine.Pin(22), self.led_num)
        self.default_color = (10, 10, 0)

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


zrhLedBoard = ZrhLedBoard()
zrhLedBoard.on_led((20, 10, 0))


while 1:
    time.sleep(0.5)
    print("running...")
