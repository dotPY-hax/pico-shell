import storage
import os

storage.disable_usb_drive()
storage.remount(mount_path="/", readonly=False)
try:
    os.unlink("/pwnd.txt")
except Exception as e:
    print(e)
storage.remount(mount_path="/", readonly=True)
storage.enable_usb_drive()
