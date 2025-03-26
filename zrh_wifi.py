import network
import time
from zrh_nvs import ZrhNvs
from zrh_ap import zrhAp


class ZrhWifi:
    '''wifi类,用来连接wifi网络'''

    def __init__(self):
        # 使用域名方式访问（esp.local）
        network.hostname("esp")
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.zrh_nvs = ZrhNvs()

    def do_connect(self):
        if not self.wlan.isconnected():
            wifi_config = self.zrh_nvs.get_wifi_config()
            if wifi_config is not None:
                self.wlan.connect(wifi_config['ssid'], wifi_config['password'])
        connectCount = 0
        while not self.wlan.isconnected():
            print("连接失败,正在重新连接")
            connectCount += 1
            time.sleep(1)
            if connectCount > 10:
                print("连接超时")
                break
        if self.wlan.isconnected():
            print("wifi连接成功:", self.wlan.ifconfig())
        else:
            '''连接失败,启动AP模式配网'''
            zrhAp.start_ap()
