import wlan
import server
import supervisor

supervisor.runtime.autoreload = False
wlan.do_wifi_stuff()
server.start()
