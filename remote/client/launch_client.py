

def client_init(user):
    from remote.remote_config import SERVER_URL, SERVER_PORT
    from .client_state import ClientState
    from .client_actions import client_folder_setup, launch_client_action
    import socketio

    client_folder_setup()
    sio = socketio.Client()

    client_state = ClientState()

    @sio.on('connect')
    def on_connect():
        sio.emit('user_joined', {'user': user})

    @sio.on('user_info')
    def get_user_info(data):
        if data is not None:
            client_state.set_user_info(data)
            launch_client_action(data)
        else:
            import sys
            print("User does not exist")
            sio.disconnect()
            sys.exit(1)

    sio.connect(SERVER_URL + ":" + str(SERVER_PORT))
    sio.wait()