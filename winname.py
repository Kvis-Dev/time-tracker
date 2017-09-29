import gi

gi.require_version('Wnck', '3.0')

from gi.repository import Wnck

screen = Wnck.Screen.get_default()
screen.force_update()  # recommended per Wnck documentation

# loop all windows
window_xid = 0

for window in screen.get_windows():
    if window.is_active():
        window_xid = window.get_xid()
        break

for window in screen.get_windows():

    if window.get_xid() == window_xid:

        window_name = str(window.get_name()).strip()
        window_icon = str(window.get_application().get_icon_name()).strip()
        if not len(window_name):
            window_name = window_icon

        if window_name != window_icon:
            o_name = window_icon
        else:
            o_name = ''
        print ('{};;;{}'.format(o_name, window_name))

# clean up Wnck (saves resources, check documentation)
window = None
screen = None
Wnck.shutdown()
