from mini_apps.file_system.access_data import read_in_files
from .parsers import state_file_parser, zip_file_parser
from models.zip_manager import ZipManager
from db_storage.db_init import init_db
from db_storage.db_interface import DbModule
from config.user_config import STATE_HTML_STORAGE


def store_state_parsed_data_into_db():
    init_db()
    read_in_files(state_file_parser,STATE_HTML_STORAGE)

    db_instance = DbModule()
    zip_instance = ZipManager()

    db_instance.insert("zip_code_list",zip_instance.get_json_zips())


def store_zip_parsed_data_into_db(path,table_name,zip_list):
    db = DbModule()
    db.start()

    db.create_table("zip_codes","zip_code")
    db.create_table("communities","id")
    db.create_table("failed_zips","zip_code")

    if len(db.get_rethink_instance().table("communities").index_list().run()) is 0:
        db.get_rethink_instance().table("communities").index_create("simplicy_index").run()
        db.get_rethink_instance().table("communities").index_wait().run()

    read_in_files(zip_file_parser, path, table_name=table_name, zip_list=zip_list)




