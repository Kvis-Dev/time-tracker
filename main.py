import htmlPy,  os
from back_end import BackEnd

app = htmlPy.AppGUI(title=u"KV app time tracker", developer_mode=True)
app.maximized = True
app.bind(BackEnd(app))
app.width = 800
app.maximized = False
app.height = 600


# Initial confiurations
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.static_path = os.path.join(BASE_DIR, "web/")
app.template_path = app.static_path

app.template = ("front.html", {})
if __name__ == "__main__":
    app.start()


