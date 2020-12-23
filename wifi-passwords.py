import subprocess
import sys


if sys.platform == 'win32':
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode(
        'utf-8', errors="backslashreplace").split('\n')
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    for i in profiles:
        try:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode(
                'utf-8', errors="backslashreplace").split('\n')
            results = [b.split(":")[1][1:-1]
                       for b in results if "Key Content" in b]
            try:
                print("{:<30}|  {:<}".format(i, results[0]))
            except IndexError:
                print("{:<30}|  {:<}".format(i, ""))
        except subprocess.CalledProcessError:
            print("{:<30}|  {:<}".format(i, "ENCODING ERROR"))
    input("")

elif sys.platform == "linux":
    """example use:
    $ python3 wifi-passwords.py | sudo sh
    Will give back all passwords saved in the system. 
    Unfortunately due to the command requiring elevated
    permissions, I cannot run and parse as I have done
    with windows. 
    """
    command = "grep psk= /etc/NetworkManager/system-connections/*"
    print(command)
else:
    print(
        f'Script is not currently supported for {sys.platform} or other Operating systems at the moment')
