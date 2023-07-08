import socket
import uasyncio as asyncio
from zrh_response_json import ZrhResponseJson
from zrh_wifi_html import html
import uasyncio as asyncio

resJson = ZrhResponseJson()
text_plain = b'HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n'
text_html = b'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
application_json = b'HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n'


# 启动socket TCP Server
async def do_socket_start():    
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind(('0.0.0.0', 8088))
    my_socket.listen(5)
    while True:
        await asyncio.sleep_ms(100)
        print("socket runing...")
        client_socket, _ = my_socket.accept()
        data = client_socket.recv(1024)
        if len(data) > 0:
            data_arr = data.decode().split("\r\n")
            print("dataArr:", data_arr)

            # 请求参数
            request_params = data_arr[len(data_arr)-1]
            print("params:", request_params)

            request_method = data_arr[0].split(" ")

            print("method:", request_method)
            if len(request_method) == 1:
                print("什么请求都没有")
                return
            # 请求wifi配置页面
            if request_method[0] == "GET" and request_method[1] == "/wifi":
                client_socket.send(text_html)
                client_socket.send(html.encode())

            elif request_method[0] == 'POST' or request_method[1] == '/cmd':
                resJson.success("成功")
                client_socket.send(application_json)
                client_socket.send(resJson.json())
            else:
                # 其他未知请求，全部拒绝
                resJson.error("请求被拒绝")
                client_socket.send(application_json)
                client_socket.send(resJson.json())
            client_socket.close()
