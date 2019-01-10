import os

from numpy import array_split
from db_storage.db_interface import DbModule
from remote.remote_config import server_config
from remote.server.server_state import ServerState
from app.file_system.access_data import read_in_files
from app.file_parser import parsers, zip_manager


def server_folder_setup():
    '''
        Sets up the server folder system
    '''
    if os.path.isdir(server_config.MAIN_DIR) is False:
        os.makedirs(server_config.DB_STORAGE)
        os.makedirs(server_config.ZIP_HTML)
        os.makedirs(server_config.ZIP_JSON)


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
    z_manager = zip_manager.ZipManager()
    server_state = ServerState()
    db_instance = DbModule()

    print("Hello")

    # Populates a Zip Manager Object
    read_in_files(parsers.parse_file)
    print("hey")

    user_tables = server_state.get_user_tables()
    chunk_amount = len(user_tables)

    chunk_list = array_split(z_manager.get_json_zips(), chunk_amount)

    # Stores the data in the db under each users table
    for idx, user_table in enumerate(user_tables):
        print(idx)
        db_instance.batch_insert(user_table, chunk_list[idx])




