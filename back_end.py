import json
from threading import Thread
import htmlPy
import subprocess
import time
import os
from glob import glob


class BackEnd(htmlPy.Object):
    def get_from_title(self):
        cmd = ['xdotool getactivewindow getwindowname']
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        out = out.decode('utf-8')

        try:
            pname = [p for p in out.split('-') if p.strip()][-1].strip()
        except IndexError:
            return None
        except TypeError:
            return None

        return pname

    def wnck_name(self):
        cmd = ['python3 {}/winname.py '.format(os.path.dirname(os.path.abspath(__file__)))]

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        out = out.decode('utf-8').strip()
        if ';;;' in out:
            return out.split(';;;')

    def loop_fn(self):
        while True:
            cmd = ['cat /proc/`xdotool getactivewindow getwindowpid`/cmdline']
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            out = out.decode('utf-8')
            pname = None
            wn_name = self.wnck_name()

            if wn_name is not None and len(wn_name) == 2:
                pname = wn_name[0] if len(wn_name[0]) else None

            if not pname:
                if 'java' in out or 'python' in out:
                    pname = self.get_from_title()

            if not pname:
                pname = False
                try:
                    pname = [app for app in self.apps if app[1] == out][0][0]
                except IndexError:
                    try:
                        pname = [app for app in self.apps if app[2] == out][0][0]
                    except IndexError:
                        pass

            if not pname:
                from_title = self.get_from_title()
                if from_title:
                    pname = from_title
                else:
                    if wn_name is not None and len(wn_name) > 1 and len(wn_name[1]):
                        try:
                            pname = [p for p in wn_name[1].split('-') if p.strip()][-1].strip()
                        except IndexError:
                            pname = wn_name[1]
                    else:
                        pname = 'Error :('

            if pname in self.info:
                self.info[pname] += 1
            else:
                self.info[pname] = 2

            time.sleep(1)

    def __init__(self, app):
        super(BackEnd, self).__init__()
        self.app = app
        self.apps = []
        self.info = {}

        self.loop = Thread(target=self.loop_fn)
        self.loop.daemon = True
        self.loop.start()

        all_dirs = glob("/usr/share/applications/*") + glob(os.path.expanduser('~/.local/share/applications/*'))

        for item in all_dirs:
            if item.endswith(".desktop"):
                with open(item) as data_source:
                    lines = data_source.readlines()
                    interface_name = [l.replace("\n", "").replace("Name=", "") for l in lines if l.startswith("Name=")][
                        0]
                    try:

                        cmd_name = [l.replace("\n", "").replace("Exec=", "") for l in lines if l.startswith("Exec=")][0]
                    except IndexError:
                        pass
                    fallback_cmd = cmd_name.split('/')[-1]

                    w_cmd = 'which ' + fallback_cmd
                    p = subprocess.Popen(w_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    w_cmd_out, w_cmd_err = p.communicate()

                    self.apps.append((interface_name, cmd_name, fallback_cmd, w_cmd_out.strip()))

    @htmlPy.Slot(result=str)
    def get_info(self):
        return json.dumps(self.info)

    @htmlPy.Slot()
    def clear_timer(self):
        self.info = {}
