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

        try:
            pname = [p for p in out.split('-') if p.strip()][-1].strip()
        except IndexError:
            pname = 'error:<%s>' % out

        return pname

    def loop_fn(self):

        while True:
            cmd = ['cat /proc/`xdotool getactivewindow getwindowpid`/cmdline']
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()

            if 'java' in out or 'python' in out:
                pname = self.get_from_title()
            else:
                pname = False
                print 'out', out
                try:
                    pname = [app for app in self.apps if app[1] == out][0][0]
                except IndexError:
                    try:
                        pname = [app for app in self.apps if app[2] == out][0][0]
                    except IndexError:
                        pass

                if not pname:
                    pname = " :( " + self.get_from_title()

            if pname in self.info:
                self.info[pname] += 1
            else:
                self.info[pname] = 1

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
                    print lines
                    interface_name = [l.replace("\n", "").replace("Name=", "") for l in lines if l.startswith("Name=")][
                        0]
                    try:

                        cmd_name = [l.replace("\n", "").replace("Exec=", "") for l in lines if l.startswith("Exec=")][0]
                    except IndexError:
                        print lines
                    fallback_cmd = cmd_name.split('/')[-1]

                    self.apps.append((interface_name, cmd_name, fallback_cmd))

        print self.apps

    @htmlPy.Slot(result=str)
    def get_info(self):
        return json.dumps(self.info)
