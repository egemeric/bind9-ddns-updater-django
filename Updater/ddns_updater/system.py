import os
import platform
import subprocess

class Bind9():
    check_bind_dpkg = "dpkg-query -W -f='${Status} ${Version}' bind9"
    check_bind_rpm  =  "rpm -q bind"

    def __init__(self):
        self.system=platform.platform()
        self.user=os.getenv("USER")
        self.root_user=os.getenv("SUDO_USER")

    def __str__(self):
        return "User:{} Sudo user:{} Platform:{}".format(self.user, self.root_user, self.system)

    def reload_config(self):
        try:
            out=subprocess.check_output(["rndc", "reload"])
        except FileNotFoundError:
            out=subprocess.check_output(["service", "bind9", "reload"])
        return out


