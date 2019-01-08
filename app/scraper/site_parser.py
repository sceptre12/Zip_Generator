import requests
from config.user_config import STATE_HTML_STORAGE


class SiteParser:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    def __init__(self, urls=None):
        if urls is None:
            self.urls = []
        self.urls = urls

    def set_urls(self, urls):
        self.urls = urls

    def get_data(self, url, headers=None):
        return requests.get(url, headers=self.headers if headers is None else headers)

    def execute_cb_on_state_html(self, cb):
        for urlObj in self.urls:
            cb(STATE_HTML_STORAGE, urlObj.state_acronym + ".html", self.get_data(urlObj.url).text)

    # def execute_cb_on_zip_info(self, cb):

