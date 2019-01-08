from os import path, listdir

from config.user_config import STATE_HTML_STORAGE


def read_in_files(cb):
    if not path.exists(STATE_HTML_STORAGE):
        return

    for file in listdir(STATE_HTML_STORAGE):
        if path.isfile(path.join(STATE_HTML_STORAGE, file)):
            with open(path.join(STATE_HTML_STORAGE, file), 'r') as f:
                cb(file, f.read())

