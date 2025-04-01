from machine import Pin
import time


class REMOTE_IR:
    # 定义键值及内容
    REMOTE_CODE = {
        69: "off", 71: "menu", 68: "test", 64: "VOL+",
        25: "VOL-", 67: "BACK", 7: "PREV", 21: "PLAY/PAUSE",
        9: "NEXT", 13: "EQ", 22: "0", 12: "1", 24: "2",
        94: "3", 8: "4", 28: "5", 90: "6", 66: "7",
        82: "8", 74: "9"
    }

    def __init__(self, gpio_num):
        """
        初始化红外接收器
        :param gpio_num: GPIO引脚号
        """
        self.irRecv = Pin(gpio_num, Pin.IN, Pin.PULL_UP)
        self.irRecv.irq(trigger=Pin.IRQ_RISING |
                        Pin.IRQ_FALLING, handler=self._ex_handler)
        self._reset_state()

    def _reset_state(self):
        """重置接收器状态"""
        self.ir_step = 0
        self.ir_count = 0
        self.rx_buf = [0] * 64
        self.rx_ok = False
        self.cmd = None
        self.repeat = 0
        self.start = 0

    def _ex_handler(self, source):
        """
        中断回调函数，用于处理红外信号
        """
        thisComeInTime = time.ticks_us()
        curtime = time.ticks_diff(thisComeInTime, self.start)
        self.start = thisComeInTime

        if 8500 <= curtime <= 9500:  # 起始信号
            self.ir_step = 1
            return

        if self.ir_step == 1:  # 处理起始信号后的步骤
            if 4000 <= curtime <= 5000:  # 数据开始
                self.ir_step = 2
                self.rx_ok = False
                self.ir_count = 0
            elif 2000 <= curtime <= 3000:  # 长按重复信号
                self.ir_step = 3
                self.repeat += 1

        elif self.ir_step == 2:  # 接收数据
            self.rx_buf[self.ir_count] = curtime
            self.ir_count += 1
            if self.ir_count >= 64:
                self.rx_ok = True
                self.ir_step = 0

        elif self.ir_step == 3:  # 处理重复信号
            if 500 <= curtime <= 650:
                self.repeat += 1

    def _decode_command(self):
        """
        解码接收到的红外信号
        """
        one_byte = 0
        for i in range(32):
            x = i * 2
            t = self.rx_buf[x] + self.rx_buf[x + 1]
            one_byte <<= 1
            if 1800 <= t <= 2800:
                one_byte += 1
        self.cmd = (one_byte & 0x0000FF00) >> 8

    def remote_scan(self):
        """
        扫描红外信号并返回解码结果
        :return: (命令码, 按键字符)
        """
        if self.rx_ok:
            self._decode_command()
            self.rx_ok = False
        return self.cmd, self.REMOTE_CODE.get(self.cmd, "UNKNOWN")
