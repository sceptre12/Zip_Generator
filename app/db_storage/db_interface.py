import rethinkdb as r


class DbModule:
    class __DbInterface:
        def __init__(self):
            self.rethink = r
            self.has_init = False
            self.db_name = "friendly_neighbor"
            self.connection = None

        def start(self):
            if not self.has_init:
                self.connect()
                if self.db_name not in self.__get_dbs():
                    self.rethink.db_create(self.db_name).run(self.connection)
                self.connection.use(self.db_name)
                self.has_init = True

        def connect(self):
            self.connection = self.rethink.connect("172.17.0.21", 28015).repl()

        def create_tables(self, tables):
            db_tables = self.__get_tables()
            operations = []
            for table in tables:
                if table not in db_tables:
                    operations.append(self.rethink.table_create(table))

            if len(operations) is not 0:
                # Expr allows me to chain multiple operations before I send the operation to the db
                self.rethink.expr(operations).run()

        def create_table(self, table_name, primary_key=None):
            if table_name not in self.__get_tables():
                self.rethink.table_create(table_name, primary_key=primary_key if primary_key is not None else "").run(self.connection)

        def batch_insert(self,table_name, datas):
            self.rethink.table(table_name).insert(datas).run(self.connection)

        def insert(self, table_name, data):
            self.rethink.table(table_name).insert(data).run(self.connection)

        def get_rethink_instance(self):
            return self.rethink

        def has_db_initialized(self):
            return self.has_init

        def __get_tables(self): return self.rethink.table_list().run(self.connection)

        def __get_dbs(self): return self.rethink.db_list().run(self.connection)

    instance = None

    def __init__(self):
        if not DbModule.instance:
            DbModule.instance = DbModule.__DbInterface()

    def __getattr__(self, item):
        return getattr(self.instance,item)
