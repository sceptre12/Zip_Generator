import os

USER_HOME = os.path.expanduser('~')
SERVER_DIR = os.path.join(USER_HOME, "server_storage")
DB_STORAGE = os.path.join(SERVER_DIR, "db_storage")
STATE_HTML = os.path.join(SERVER_DIR, "state_storage")

CLIENT_DIR = os.path.join(USER_HOME, "client_storage")

ZIP_HTML = os.path.join(CLIENT_DIR, "zip_html")
ZIP_JSON = os.path.join(CLIENT_DIR, "zip_info")

SERVER_URL = "http://localhost"
SERVER_PORT = 8084
SERVER_IP = "0.0.0.0"