import rethinkdb as r
from collections import OrderedDict


class DbModule:
    class __DbInterface:
        def __init__(self,db_connect_url="localhost",db_access_port=28015):
            self.rethink = r
            self.has_init = False
            self.db_name = "friendly_neighbor"
            self.connection = None
            self.db_connect_url = db_connect_url
            self.db_access_port = db_access_port

        def start(self):
            if not self.has_init:
                self.connect()
                if self.db_name not in self.__get_dbs():
                    self.rethink.db_create(self.db_name).run(self.connection)
                self.connection.use(self.db_name)
                self.has_init = True

        def connect(self):
            self.connection = self.rethink.connect(self.db_connect_url, self.db_access_port).repl()

        def create_tables(self, tables):
            db_tables = self.get_tables()
            operations = []
            for table in tables:
                if table not in db_tables:
                    operations.append(self.rethink.table_create(table))

            if len(operations) is not 0:
                # Expr allows me to chain multiple operations before I send the operation to the db
                self.rethink.expr(operations).run()

        def create_table(self, table_name, primary_key=None):
            if table_name not in self.get_tables():
                self.rethink.table_create(table_name, primary_key=primary_key if primary_key is not None else "id").run(self.connection)

        def insert(self, table_name, data):
            self.rethink.table(table_name).insert(data).run(self.connection)

        def get_rethink_instance(self):
            return self.rethink

        def has_db_initialized(self):
            return self.has_init

        def filter_w_criteria(self,table_name,criteria):
            return self.rethink.table(table_name).filter(criteria).run(self.connection)

        def get_val(self, table_name, id):
            return self.rethink.table(table_name).get(id).run(self.connection)

        def get_all(self,table_name, value_to_get,index=None):
            return self.rethink.table(table_name).get_all(value_to_get, index=index).run(self.connection)

        def get_tables(self): return self.rethink.table_list().run(self.connection)

        def __get_dbs(self): return self.rethink.db_list().run(self.connection)

    instance = None

    def __init__(self):
        if not DbModule.instance:
            DbModule.instance = DbModule.__DbInterface()

    def __getattr__(self, item):
        return getattr(self.instance,item)


class DbQueryHelper:
    def __init__(self,rethink_ref):
        self.rethink = rethink_ref
        self.queries = OrderedDict()

    def add_query(self, attr_name, query):
        self.queries[attr_name] = query

    def execute(self):
        result = self.rethink.expr(self.queries.values()).run()
        index = 0
        for key in self.queries:
            self.queries[key] = result[index]
            index += 1
        return self.queries
