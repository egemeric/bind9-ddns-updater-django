import os
import platform
import subprocess


class Bind9:
    check_bind_dpkg = "dpkg-query -W -f='${Status} ${Version}' bind9"
    check_bind_rpm = "rpm -q bind"

    def __init__(self):
        self.system = platform.platform()
        self.user = os.getenv("USER")
        self.root_user = os.getenv("SUDO_USER")

    def __str__(self):
        return "User:{} Sudo user:{} Platform:{}".format(self.user, self.root_user, self.system)


def reload_config():
    try:
        out = subprocess.check_output(["sudo", "/etc/init.d/bind9", "reload"])
    except subprocess.CalledProcessError:
        out = subprocess.check_output(["sudo", "/etc/init.d/named restart", "restart"])
    except subprocess.CalledProcessError:
        print("The named service cant be restarted check sudoers or restart script in system.py")
    return out


