import logging
import webbrowser
from multiprocessing import Queue
from threading import Thread

import flask
from flask_socketio import SocketIO

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


def emit_to_web(emit, to_web: Queue):
    while True:
        data = to_web.get()
        emit("update", data)


def start_server(to_web: Queue, from_web: Queue):
    thread = Thread(
        target=emit_to_web,
        args=(
            socketio.emit,
            to_web,
        ),
        daemon=True,
    )
    thread.start()

    @socketio.on("update")
    def update(data):
        print("Received", data)
        from_web.put(data)

    print("Starting server on port 5000")
    print("Opening http://localhost:5000 in your browser...")
    webbrowser.open("http://localhost:5000")

    socketio.run(app, allow_unsafe_werkzeug=True, log_output=False)


app = flask.Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/static/<path:path>")
def send_static(path):
    return flask.send_from_directory("static", path)
