import uasyncio as asyncio
from zrh_web_server import do_web_server
from zrh_ble_central import do_ble_central
from zrh_wifi import do_wifi



async def main():
    do_wifi()
    tasks = [do_web_server(), do_ble_central()]
    await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
