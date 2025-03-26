import network
import asyncio
import json
import machine

from microdot import Microdot
from zrh_wifi_html import html
from zrh_response_json import ZrhResponseJson
from zrh_nvs import ZrhNvs


app = Microdot()


class ZrhAP:
    def __init__(self):
        self.html = html
        self.zrh_nvs = ZrhNvs()
        self.res_json = ZrhResponseJson()
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(essid='ESP-AP', authmode=network.AUTH_WPA_WPA2_PSK,
                       password='esp123456')

    async def reboot(self):
        '''设置wifi成功之后,延时1秒重启设备'''
        await asyncio.sleep(1)
        self.ap.active(False)
        machine.reset()

    def init_ap(self):
        """创建wifi热点,ssid=ESP-AP password=esp123456"""
        while self.ap.active() == False:
            pass
        print('--- AP热点启动成功 ---')
        print(self.ap.ifconfig())

    async def init_wifi_page(self):
        print("启动microdot服务....")
        await app.start_server(debug=True, port=80)

    def start_ap(self):
        print("开始启动ap.....")
        self.init_ap()
        asyncio.run(self.init_wifi_page())

    def get_wifi_page(self):
        return html, 200, {'Content-Type': 'text/html'}

    def set_wifi(self, request):
        bodyJson = json.loads(request.body.decode())
        ssid = bodyJson['ssid']
        pwd = bodyJson["password"]
        self.zrh_nvs.set_wifi_config(ssid, pwd)
        self.res_json.success("配置wifi完成")
        asyncio.create_task(self.reboot())
        return self.res_json.json()


zrhAp = ZrhAP()


@app.get("/wifi")
async def show_wifi_page(request):
    return zrhAp.get_wifi_page()


@app.post("/setWifi")
async def set_wifi(request):
    return zrhAp.set_wifi(request)
