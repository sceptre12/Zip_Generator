import os

USER_HOME = os.path.expanduser('~')
MAIN_DIR = os.path.join(USER_HOME,"server_storage")
DB_STORAGE = os.path.join(MAIN_DIR, "db_storage")
STATE_HTML = os.path.join(MAIN_DIR, "STATE_STORAGE")
ZIP_HTML = os.path.join(MAIN_DIR, "zip_html")
ZIP_JSON = os.path.join(MAIN_DIR,"zip_info")
