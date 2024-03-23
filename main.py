from utils import full_chain 
from database import init_database

db = init_database()

response = full_chain("How many asrtists are here",db)
print(response)