from sanic import Sanic
import socketio
import threading

from remote.server.system_organizer import server_folder_setup, set_up_db, populate_db


def init():
    server_folder_setup()
    set_up_db()
    populate_db()


t = threading.Thread(target=init)

app = Sanic()
sio = socketio.AsyncServer(async_mode='sanic')
sio.attach(app)


@sio.on('connect')
def connect(sid,environ):
    print('connect',sid)
    print("HELLO WORLDDD !!!!! ")
    print(environ)

# @sio.on('who_joined')
# def who_joined(sid,data):

if __name__ == "__main__":
    t.start()
    app.run(host="0.0.0.0", port=8084)
