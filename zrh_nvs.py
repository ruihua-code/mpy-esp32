from esp32 import NVS


class ZrhNvs:
    def __init__(self):
        self.wifi_config = NVS("WIFI_CONFIG")

    def get_wifi_config(self):
        '''读取持久存储wifi配置信息'''
        ssid = bytearray(12)
        password = bytearray(12)
        try:
            self.wifi_config.get_blob("ssid", ssid)
            self.wifi_config.get_blob("password", password)
            return {"ssid": ssid.decode(), "password": password.decode()}
        except OSError:
            return None

    def set_wifi_config(self, ssid, password):
        '''设置持久存储wifi配置信息'''
        self.wifi_config.set_blob("ssid", ssid)
        self.wifi_config.set_blob("password", password)
        self.wifi_config.commit()

    def erase_wifi_config(self):
        '''清除wifi配置信息'''
        try:
            self.wifi_config.erase_key("ssid")
            self.wifi_config.erase_key("password")
        except OSError:
            pass
