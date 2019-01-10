from .site_parser import SiteParser
from .url_builder import Url_List
from app.file_system.store_data import store_data_to_file


def grab_and_store_data():
    """
    Grabs html and download the webpage and store it in a file
    :return:
    """
    site_parser = SiteParser(Url_List)

    site_parser.execute_cb_on_state_html(store_data_to_file)
