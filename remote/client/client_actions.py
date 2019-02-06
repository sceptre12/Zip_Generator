import os
from remote.remote_config import CLIENT_DIR, ZIP_HTML, ZIP_JSON
from threading import Thread
from app.scraper.requests import ZipRequester
from app.file_system.store_data import store_data_to_file
from db_storage import DbModule


def client_folder_setup():
    '''
        Sets up the client folder system
    '''
    if os.path.isdir(CLIENT_DIR) is False:
        os.makedirs(ZIP_HTML)
        os.makedirs(ZIP_JSON)


def launch_client_action(user_info):
    db_interface = DbModule()
    db_interface.start()

    table_name = user_info['table_name']

    zip_links = db_interface.get_rethink_instance().table(table_name).map(lambda doc:
        {'zip_code': doc['zip_code'],'link': doc['link']}
    ).run()

    zip_requests = ZipRequester(zip_links)

    zip_requests.set_cb(store_data_to_file)
    t = Thread(target=zip_requests.store_zip_concurrently, daemon=True)
    t.start()
    t.join()
    '''
        At this point I've stored all the data in the users file system
        Need to parse each file. I need to find some way to check each parsed link
        to see if it activates a failed condition. In the event it has failed
        store those files that were successful but close out the thread and delete
        failed files
        report failure to the db, giving the information on the zip that it failed on
        set a timer for 24 hours before script starts concurrently running again 
    '''


