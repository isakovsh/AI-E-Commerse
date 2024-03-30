from utils import full_chain , get_sql_chain
from database import init_database

db = init_database()

response = get_sql_chain("How many asrtists are here",db)
print(response)