# from zrh_wifi import ZrhWifi


# def main():
#     zrhWifi = ZrhWifi()
#     zrhWifi.do_connect()


# if __name__ == "__main__":
#     print("开始运行...")
#     main()


from zrh_pir_motion_sensor import on_start


if __name__ == "__main__":
    print("开始运行...")
    on_start()
    while 1:
        pass
