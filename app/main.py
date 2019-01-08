from file_system.access_data import read_in_files
from file_parser.parsers import parse_file, ZipManager
from db_storage.db_init import init_db
from db_storage.db_interface import DbModule


init_db()
read_in_files(parse_file)

db_instance = DbModule()
zip_instance = ZipManager()

db_instance.batch_insert("zip_code",zip_instance.get_json_zips())
