import machine
import time
from zrh_led import ZrhLedBoard


zrhLedBoard = ZrhLedBoard()


class ZrhPirMotionSensor:
    '''运动传感器'''

    def __init__(self, pin: int) -> None:
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.callback = None

    def listen(self, callback):
        self.callback = callback
        self.pin.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING,
                     handler=self._motion_callback)

    def _motion_callback(self, pin):
        if pin.value():
            # 检测到运动！
            self.callback(1)
        else:
            # 运动结束
            self.callback(0)


'''使用示例'''


def _on_motion(state):
    if state:
        print("find")
        zrhLedBoard.on_led((150, 150, 50))
    else:
        print("stop")
        zrhLedBoard.off_led()


def on_start():
    zrhPirMotionSensor = ZrhPirMotionSensor(15)
    zrhPirMotionSensor.listen(_on_motion)
