import sqlmodel as sql

# setup engine
sqlite_file_name="database1.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread":False}
engine = sql.create_engine(sqlite_url, echo=True, connect_args=connect_args)

# create db and tables
def create_db_tables():
    sql.SQLModel.metadata.create_all(engine)