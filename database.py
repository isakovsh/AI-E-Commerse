from langchain_community.utilities import SQLDatabase

def init_database() -> SQLDatabase: 
    db_url = "mysql+mysqlconnector://{name}:{passwod}@localhost:3306/Chinook"
    db = SQLDatabase.from_uri(db_url)
    return db

