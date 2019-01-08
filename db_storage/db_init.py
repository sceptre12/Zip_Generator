from .db_interface import DbModule


def init_db():
    db_instance = DbModule()

    db_instance.start()

    db_instance.create_tables(["coordinates","area","population"])
    db_instance.create_table("zip_code","zip_code")

