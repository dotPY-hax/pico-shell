# pico-shell
BadUsb pseudo shell for raspberry pi pico W

## What?
turns a Pico W into a keystroke injecting wifi connected BadUSB pseudo shell with a back channel i.e. you will see the output
## How?
* when plugging in the Pico W it starts a new wifi network named pico and a tiny http server and looks like a mass storage device - no stealth at all.
* when recieving a payload via POST on its only endpoint it will try to establish the back channel by finding its own mount point and redirecting command output into a file.
* when the file was written the Pico W will read the file and respond its contents to the POST request.

## Oh god why?
looks like I like Picos now...

## Installation
1. you need CircuitPython from https://circuitpython.org/downloads - make sure to use the correct board. (The Pico W!!)
2. run download.py to get a zipfile of all the dependencies. Copy the lib folder from the zip to your Pico W
3. plug in
4. pray to the machine god

## POST request

{"back": True, "system": "linux", "terminal": "whoami", "layout": "de"}

- "back": if the Pico W should return the input. when this is False it wont try to find itself and the storage could be deactivated.
- "system": "linux" or "win" ("win" only supports powershell)
- "terminal": the shell command (only tested for simple commands though)
- "layout": the keyboard layout. make sure to use the correct layout matching the target. the layout 'code' will be the last 2 chars of the layout python file 'keyboard_layout_win_de.py' would be 'de'

```
>>> import requests
>>> d = {"back": True, "system": "linux", "terminal": "whoami"}
>>> print(requests.post("http://192.168.4.1:42080/", json=d).json().get("result", ""))
dotpy
>>>
```

## Considerations
- important parameters can be changed in config.py
- its a bit fiddly
- absolutely no stealth
- when not using the back channel whatsoever - turn off the usb storage in boot.py
- it can also join an existing network
- unfortunately there is no https at the moment :( so be careful
- if it breaks (something) - sadge

## Future
- add some stealth
- make device name configureable
- optimize times for injections - on windows it seem faster for whatever reason
- allow for automated injection on boot
- add more out of the box functions
- fix ze bugs
- ...
- add ducky script some time (never lol)
