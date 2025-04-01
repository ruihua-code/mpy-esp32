from machine import Pin, PWM
import time


class ZrhServo:
    def __init__(self, pin: int) -> None:
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)
        self.angle = 0

    def write_angle(self, angle):
        '''-90到90度的舵机方法,最大旋转角度是90度'''
        self.pwm.duty(self._calculate_pwm_duty(angle))
        self.angle = angle

    def write_angle_speed(self, angle, speed=1):
        '''-90到90度的舵机方法, 最大旋转角度是90度, speed控制旋转速度'''
        step = 0.5 if angle > self.angle else -0.5  # 使用更小的步进值
        current_angle = self.angle

        while (step > 0 and current_angle < angle) or (step < 0 and current_angle > angle):
            current_angle += step
            if (step > 0 and current_angle > angle) or (step < 0 and current_angle < angle):
                current_angle = angle  # 确保最终角度精确到目标值
            self.pwm.duty(self._calculate_pwm_duty(current_angle))
            time.sleep(speed / 200)  # 根据速度调整延迟，值越大旋转越慢

        self.angle = angle

    def _calculate_pwm_duty(self, angle):
        '''根据角度计算 PWM 占空比'''
        return int(((angle + 90) * 2 / 180 + 0.5) / 20 * 1023)


'''使用示例'''


zrhServo = ZrhServo(12)

zrhServo.write_angle(90)

# 快速旋转到45度
zrhServo.write_angle_speed(45, speed=5)

# 慢速旋转到90度
zrhServo.write_angle_speed(90, speed=20)

# 快速旋转到0度
zrhServo.write_angle_speed(0, speed=0)

for i in range(20):
    if i % 2 == 0:
        zrhServo.write_angle_speed(45, speed=0)
    else:
        zrhServo.write_angle_speed(0, speed=0)


while 1:
    time.sleep(1)
    print("running...")
