class JsonFormatter:
    def __init__(self):
        self.json_format = {}

    def set_json(self):
        self.json_format = {**self.__dict__}

    def get_json(self):
        self.set_json()
        return self.json_format
