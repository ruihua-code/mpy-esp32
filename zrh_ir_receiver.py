
"""红外接收使用示例"""
from zrh_ir_remote import remote
import time

ir = remote.REMOTE_IR(23)
while 1:
    cmd, key_str = ir.remote_scan()
    # print(cmd,key_str)
    print("按下:", key_str)
    time.sleep_ms(500)
