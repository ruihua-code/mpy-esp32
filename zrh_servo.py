from machine import Pin, PWM
import time


class ZrhServo:
    def __init__(self, pin: int) -> None:
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)
        self.angle = 0

    def write_angle(self, angle):
        '''-90到90度的舵机方法,最大旋转角度是90度'''
        self.pwm.duty(int(((angle + 90)*2/180+0.5)/20*1023))
        self.angle = angle


'''使用示例'''


zrhServo = ZrhServo(12)
zrhServo.write_angle(45)

time.sleep(1)

zrhServo.write_angle(90)
print("当前角度:", zrhServo.angle)
time.sleep(1)

zrhServo.write_angle(0)

print("当前角度:", zrhServo.angle)

while 1:
    time.sleep(1)
    print("running...")
