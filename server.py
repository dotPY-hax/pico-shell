import json
import socketpool
import wifi

from adafruit_httpserver.mime_type import MIMEType
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.server import HTTPServer
from adafruit_httpserver.methods import HTTPMethod

import config
from system_interaction import LinuxInteraction, WindowsInteraction
import wlan

pool = socketpool.SocketPool(wifi.radio)
server = HTTPServer(pool)

system_interaction_object = None

@server.route("/", HTTPMethod.POST)
def cpu_information_handler(request: HTTPRequest):
    incoming = json.loads(request.body)
    print(incoming)
    result = do_stuff(incoming)
    data = {"result": result}
    with HTTPResponse(request, content_type=MIMEType.TYPE_JSON) as response:
        response.send(json.dumps(data))


def start():
    ip = wlan.ip()
    port = config.SERVER_PORT
    print(f"Listening on http://{ip}:{port}")
    server.serve_forever(host=ip, port=port)


def do_stuff(request_dict):
    global system_interaction_object

    layout = request_dict.get("layout", "de")
    payload = request_dict.get("terminal", "")
    back_channel = request_dict.get("back", False)
    system = request_dict.get("system", "linux")

    if not system_interaction_object:
        systems = {"windows": WindowsInteraction, "win": WindowsInteraction, "linux": LinuxInteraction}
        system_interaction_object = systems[system]()

    if layout:
        system_interaction_object.keyboard.change_layout(layout)
    if back_channel and payload:
        return system_interaction_object.run_terminal_command_with_back_channel(payload)
    elif not back_channel and payload:
        return system_interaction_object.run_terminal_command(payload)
