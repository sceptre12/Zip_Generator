import argparse
import sys

parser = argparse.ArgumentParser(description='Main Application')

parser.add_argument('-s','--server',action='store_true',help='Launching Server',dest='server')
parser.add_argument('-c','--client',action='store_true',help='Launching Client',dest='client')


args = parser.parse_args()
if args.client is True and args.server is True:
    print("Cannot run both Client and Server")
    sys.exit(1)
if args.server:
'''
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
'''