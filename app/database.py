import sqlmodel as sql 

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = sql.create_engine(
    sqlite_url, 
    echo=True, 
    connect_args=connect_args
)

def create_db_tables():
    sql.SQLModel.metadata.create_all(engine)