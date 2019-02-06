class ZipManager:
    class __ZipManager:
        def __init__(self):
            self.zip_codes = []
            self.stateInfo = []

        def add_zip(self, zip_code):
            self.zip_codes.append(zip_code)

        def add_state_info(self, state_info):
            self.stateInfo.append(state_info)

        def get_zip(self): return self.zip_codes

        def get_state_info(self): return self.stateInfo

        def get_json_zips(self):
            return list(map(lambda zip_c: zip_c.get_json(), self.zip_codes))

        def __str__(self):
            return ''.join(self.zip_codes) + ''.join(self.stateInfo)

        def __repr__(self): return self.__str__()

        def clean_up(self):
            self.zip_codes = []
            self.stateInfo = []

    instance = None

    def __init__(self):
        if not ZipManager.instance:
            ZipManager.instance = ZipManager.__ZipManager()

    def __getattr__(self, item):
        return getattr(self.instance, item)
