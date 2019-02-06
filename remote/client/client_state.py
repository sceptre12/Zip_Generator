
class ClientState:
    class __ClientState:
        def __init__(self):
            self.user_info = {}

        def set_user_info(self,info):
            self.user_info = info

        def get_user_info(self): return self.user_info

    instance = None

    def __init__(self):
        if not ClientState.instance:
            ClientState.instance = ClientState.__ClientState()

    def __getattr__(self, item):
        return getattr(self.instance,item)
