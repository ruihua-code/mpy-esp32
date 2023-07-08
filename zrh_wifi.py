import network
from micropython import const
from time import sleep

_ssid = const('1yongcloud')
_pwd = const('yiyongcloud')


def do_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    while not wlan.active(True):
        print("wait wlan")    
    wlan.connect(_ssid, _pwd)
    
    while not wlan.isconnected():
        print("wifi connecting...")        
        sleep(1)

    print(wlan.ifconfig())
    print("wifi success.")
