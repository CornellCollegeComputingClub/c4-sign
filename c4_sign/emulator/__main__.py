import flask
from flask_socketio import send, emit, SocketIO
import multiprocessing

def start_heart():
    import c4_sign.__main__ as main
    main.main()

app = flask.Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return flask.render_template('index.html')

@socketio.on('update')
def update(data):
    print('Received', data)
    socketio.emit('update', data)

if __name__ == '__main__':
    p = multiprocessing.Process(target=start_heart)
    p.start()
    socketio.run(app)