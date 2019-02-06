from numpy import array_split
from db_storage import DbModule
from remote.remote_config import *
from remote.server.server_state import ServerState
from app.file_system.access_data import read_in_files
from app.scraper.file_parser import parsers
from models import ZipManager


def server_folder_setup():
    '''
        Sets up the server folder system
    '''
    if os.path.isdir(SERVER_DIR) is False:
        os.makedirs(DB_STORAGE)
        os.makedirs(ZIP_JSON)


def set_up_db():
    server_state = ServerState()
    db_instance = DbModule()
    db_instance.start()

    db_instance.create_table("zip_code","zip_code")
    db_instance.create_tables(server_state.get_user_tables())


def populate_db():
    '''
        This function reads in and parses the file on the system
        The data is then split into chunks that gets pushed into each user table
    '''
    z_manager = ZipManager()
    server_state = ServerState()
    db_instance = DbModule()

    # Populates a Zip Manager Object
    read_in_files(parsers.state_file_parser)

    user_tables = server_state.get_user_tables()
    chunk_amount = len(user_tables)

    chunk_list = array_split(z_manager.get_json_zips(), chunk_amount)

    # Stores the data in the db under each users table
    for idx, user_table in enumerate(user_tables):
        print(idx)
        db_instance.batch_insert(user_table, chunk_list[idx])

    z_manager.clean_up()



