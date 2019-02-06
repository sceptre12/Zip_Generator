def server_init(main_var):
    from sanic import Sanic
    from .server_state import ServerState
    from db_storage import DbModule
    from models import ZipManager
    from .client_response_handler import get_user_info
    from remote.remote_config import SERVER_IP
    import socketio

    from .system_organizer import server_folder_setup, set_up_db, populate_db

    app = Sanic()
    sio = socketio.AsyncServer(async_mode='sanic')
    sio.attach(app)

    server_state = ServerState()
    db_instance = DbModule()
    z_manager = ZipManager()

    def init():
        server_folder_setup()
        set_up_db()
        populate_db()

    @sio.on('connect')
    def connect(sid,environ):
        print("User Connected")

    @sio.on('user_joined')
    async def who_joined(sid,data):
        await sio.emit('user_info', get_user_info(data['user'], server_state, db_instance, sio))

    if main_var == "__main__":
        print("hello")
        init()
        app.run(host=SERVER_IP, port=8084)
