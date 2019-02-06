from functools import reduce


def _create_user_state(obj, user):
    obj[user] = {
        'table_name': user + "_table",
        'row_count': 0,  # Number of Rows in the table
        'current_zip_id': '',  # The Id representing the last zip that was transferred over,
        # These let me know the range of zips that was sent to the user
        'start_zip': 0,
        'end_zip': 0
    }
    return obj


class ServerState:
    class __ServerState:
        def __init__(self):
            self.user_list = ['x1','x2','malcolm', 'tai', 'marcine', 'erika', 'brian','kidd']
            self.user_state = reduce(_create_user_state, self.user_list, {})

        def get_list_of_users(self):
            return self.user_list

        def get_user_info(self, user):
            return self.user_state[user] if user in self.user_state else None

        def set_user_info(self, user, data):
            self.user_state[user] = data

        def get_user_tables(self):
            return list(map(lambda user: self.user_state[user]['table_name'], self.user_list))

    instance = None

    def __init__(self):
        if not ServerState.instance:
            ServerState.instance = ServerState.__ServerState()

    def __getattr__(self, item):
        return getattr(self.instance, item)



