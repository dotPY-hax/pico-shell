import zipfile

import requests


class Downloader:
    github = ""
    folder_name = ""
    file_names = []
    files = {}

    def download(self):
        self.files = {}
        for file_name in self.file_names:
            link = self.github + self.folder_name + "/" + file_name
            print("DOWNLOADING: " + link)
            self.files[file_name] = requests.get(link).text

class HIDDownloader(Downloader):
    github = "https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_HID/main/"
    folder_name = "adafruit_hid"
    file_names = ["__init__.py", "consumer_control.py", "consumer_control_code.py", "keyboard.py", "keyboard_layout_base.py", "keyboard_layout_us.py", "keycode.py", "mouse.py"]

class ServerDownloader(Downloader):
    github = "https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_HTTPServer/main/"
    folder_name = "adafruit_httpserver"
    file_names = ["__init__.py", "headers.py", "methods.py", "mime_type.py", "request.py", "response.py", "route.py",
                  "server.py", "status.py"]

class LayoutDownloader(Downloader):
    github = "https://raw.githubusercontent.com/Neradoc/Circuitpython_Keyboard_Layouts/main/libraries/"
    folder_name = "layouts"
    file_names = ["keyboard_layout_mac_fr.py", "keyboard_layout_us_dvo.py", "keyboard_layout_win_br.py",
                  "keyboard_layout_win_cz.py", "keyboard_layout_win_cz1.py", "keyboard_layout_win_da.py",
                  "keyboard_layout_win_de.py", "keyboard_layout_win_es.py", "keyboard_layout_win_fr.py",
                  "keyboard_layout_win_hu.py", "keyboard_layout_win_it.py", "keyboard_layout_win_po.py",
                  "keyboard_layout_win_sw.py", "keyboard_layout_win_tr.py", "keyboard_layout_win_uk.py"]


def own_the_libs():
    downloaders = [HIDDownloader(), ServerDownloader(), LayoutDownloader()]
    lib = "lib"
    with zipfile.ZipFile("libraries.zip", "w") as z:
        for downloader in downloaders:
            downloader.download()
            for filename, file in downloader.files.items():
                z.writestr(lib + "/" + downloader.folder_name + "/" + filename, file)
                print("writing: " + lib + "/" + downloader.folder_name + "/" + filename)
