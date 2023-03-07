import time

import config
import wifi


def make_access_point():
    try:
        wifi.radio.start_ap(config.WIFI_SSID, config.WIFI_PASSWORD)
        print(wifi.radio.ipv4_address_ap)
        while not wifi.radio.ipv4_address_ap:
            time.sleep(0.1)
    except NotImplementedError:
        pass


def join_network():
    wifi.radio.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
    while not wifi.radio.ipv4_address:
        time.sleep(0.1)


def ip():
    if config.WIFI_MAKE_OR_JOIN == 0:
        return str(wifi.radio.ipv4_address_ap)
    else:
        return str(wifi.radio.ipv4_address)


def do_wifi_stuff():
    if config.WIFI_MAKE_OR_JOIN == 0:
        make_access_point()
    else:
        join_network()
