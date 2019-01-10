from sanic import Sanic
import socketio

from .system_organizer import server_folder_setup, set_up_db, populate_db

app = Sanic()
sio = socketio.AsyncServer(async_mode='sanic')
sio.attach(app)


def init():
    server_folder_setup()
    set_up_db()
    populate_db()


@sio.on('connect')
def connect(sid,environ):
    print('connect',sid)
    print("HELLO WORLDDD !!!!! ")
    print(environ)

# @sio.on('who_joined')
# def who_joined(sid,data):

if __name__ == "__main__":
    init()
    app.run(host="0.0.0.0", port=8084)
