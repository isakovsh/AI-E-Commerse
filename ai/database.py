from langchain_community.utilities import SQLDatabase

def init_database() -> SQLDatabase: 
    db_url = "mysql+mysqlconnector://root:kiuf2021@localhost:3306/datashop"
    db = SQLDatabase.from_uri(db_url)
    return db

