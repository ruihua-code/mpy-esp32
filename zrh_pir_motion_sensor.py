import machine


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
    # led灯
    led_pin = machine.Pin(21, machine.Pin.OUT, machine.Pin.PULL_UP)
    if state:
        print("运动检测回调：检测到运动")
        led_pin.value(1)
    else:
        print("运动检测回调：运动结束")
        led_pin.value(0)


zrhPirMotionSensor = ZrhPirMotionSensor(23)
zrhPirMotionSensor.listen(_on_motion)

while 1:
    pass
