import urllib.request
import os
from bottle import route, run
import threading


@route("/github/onPush")
def update():
    path = os.path.dirname(__file__)

    with urllib.request.urlopen("https://example.com/latest.zip") as upd:
        with open(path, "wb+") as f:
            f.write(upd.read())


server = threading.Thread(target=run(host="0.0.0.0"))
server.start()
print("bottle server started")
