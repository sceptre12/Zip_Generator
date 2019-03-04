from os import path, listdir


def read_in_files(cb,file_path, **kwargs):
    if not path.exists(file_path):
        return
    for file in listdir(file_path):
        if path.isfile(path.join(file_path, file)):
            with open(path.join(file_path, file), 'r') as f:
                cb(file, f.read(), **kwargs)

