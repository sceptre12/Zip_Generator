from app.configs.constants.state_info import StateAcronyms
from config.user_config import ZIP_CODE_WEBSITE


class StateUrl:
    def __init__(self,state_acronym):
        self.state_acronym = state_acronym
        self.url = ZIP_CODE_WEBSITE + "/" + state_acronym.lower()


def __generate_urls():
    urls = []
    for acronym in StateAcronyms:
        urls.append(StateUrl(acronym.value))
    return urls


Url_List = __generate_urls()
