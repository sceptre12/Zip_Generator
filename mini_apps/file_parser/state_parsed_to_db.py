from file_system.access_data import read_in_files
from .parsers import state_file_parser
from zip_manager import ZipManager
from db_storage.db_init import init_db
from db_storage.db_interface import DbModule
from config.user_config import STATE_HTML_STORAGE


def store_state_parsed_data_into_db():
    init_db()
    read_in_files(state_file_parser,STATE_HTML_STORAGE)

    db_instance = DbModule()
    zip_instance = ZipManager()

    db_instance.batch_insert("zip_code",zip_instance.get_json_zips())

