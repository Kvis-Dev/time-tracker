import gi, time

gi.require_version('Wnck', '3.0')
from gi.repository import Wnck

import os

apps = []

for item in os.listdir("/usr/share/applications"):
    if item.endswith(".desktop"):
        with open("/usr/share/applications/" + item) as data_source:
            lines = data_source.readlines()

            interface_name = [l.replace("\n", "").replace("Name=", "") for l in lines if l.startswith("Name=")][0]
            try:

                cmd_name = [l.replace("\n", "").replace("Exec=", "") for l in lines if l.startswith("Exec=")][0]
            except IndexError:
                print lines
            fallback_cmd = cmd_name.split('/')[-1]

            apps.append((interface_name, cmd_name, fallback_cmd))

print apps
print '---------------------------------------------'

time.sleep(2)

screen = Wnck.Screen.get_default()
screen.force_update()  # recommended per Wnck documentation

# loop all windows
for window in screen.get_windows():
    if window.is_active() == True:
        print (window.get_geometry())
        window_name = window.get_name()
        print (window.get_application().get_icon_name())
        print (dir(window.get_application()))
        print (window_name)

# clean up Wnck (saves resources, check documentation)
window = None
screen = None
Wnck.shutdown()
