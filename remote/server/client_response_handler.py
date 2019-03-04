from db_storage import DbQueryHelper


def get_user_info(user, server_state, db_interface, sio):
    user_info = None
    if server_state.get_user_info(user) is not None:
        user_info = server_state.get_user_info(user)
        query_helper = DbQueryHelper(db_interface.get_rethink_instance())

        query_helper.add_query('count',db_interface.get_rethink_instance().table(user_info['table_name']).count())
        query_helper.add_query('start_zip',db_interface.get_rethink_instance().table(user_info['table_name']).nth(0))
        query_helper.add_query('end_zip',db_interface.get_rethink_instance().table(user_info['table_name']).nth(-1))

        result = query_helper.execute()
        user_info['row_count'] = result['count']
        user_info['start_zip'] = result['start_zip']
        user_info['end_zip'] = result['end_zip']

    return user_info
