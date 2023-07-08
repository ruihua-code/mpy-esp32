import bluetooth
from time import sleep
from micropython import const,mem_info
import zrh_thread_var
import gc
import uasyncio as asyncio

_IRQ_SCAN_RESULT = const(5)
_XIAO_MI_MAC = const('D9:6E:B5:74:A8:E3')

def _scan_callback(event, data):
    if event == _IRQ_SCAN_RESULT:                    
        _, addr, _, rssi, _ = data
        device_address = ":".join("{:02X}".format(b) for b in addr)
        print("find ok", device_address, rssi)
        if _XIAO_MI_MAC == device_address:
            print("find ok", device_address, rssi)
            gc.collect()

async def do_ble_central():
    bt = bluetooth.BLE()
    bt.active(True)

    bt.gap_scan(0, 5000000, 2000000)
    bt.irq(_scan_callback)     

    while True:                
        await asyncio.sleep_ms(50)
        print("scaning...")
        # mem_info()
        if zrh_thread_var.ble_central_runing == False:
            bt.gap_scan(None)
            bt.active(False)            
            print("stop scan......")
            break
