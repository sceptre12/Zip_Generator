import os


def store_data_to_file(file_path, filename, data):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(os.path.join(file_path, filename), 'w') as f:
        f.write(data)
