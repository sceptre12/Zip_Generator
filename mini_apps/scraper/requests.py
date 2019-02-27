import requests
from concurrent.futures import ThreadPoolExecutor
from time import sleep


class Requester:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    def __init__(self, items=None):
        if items is None:
            self.items = []
        self.items = items

    def set_urls(self, items):
        self.items = items

    def get_data(self, link, headers=None):
        return requests.get(link, headers=self.headers if headers is None else headers)


class StateRequester(Requester):

    def __init__(self, urls=None):
        super().__init__(urls)

    def execute_cb_on_state_html(self, cb):
        from config.user_config import STATE_HTML_STORAGE
        for urlObj in self.items:
            cb(STATE_HTML_STORAGE, urlObj.state_acronym + ".html", self.get_data(urlObj.url).text)


# Inspect client action to see parameters for zipObj
class ZipRequester(Requester):
    def __init__(self, zips=None):
        super().__init__(zips)
        self.cb = None

    def set_cb(self,cb):
        self.cb = cb

    def __execute_cb(self,zip_obj):
        from remote.remote_config import ZIP_HTML
        sleep(18)
        print(zip_obj)
        self.cb(ZIP_HTML, str(zip_obj['zip_code']) + ".html", self.get_data(zip_obj['link']).text)

    def store_zip_concurrently(self):
        with ThreadPoolExecutor(max_workers=20) as executor:
            {executor.submit(self.__execute_cb,zip_obj): zip_obj for zip_obj in self.items}