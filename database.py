from models import model_queries
import clickhouse_connect
import os
from dotenv import load_dotenv

load_dotenv()

def startup():
    client = clickhouse_connect.get_client(host=f'{os.environ["HOST"]}', port=int(os.environ["PORT"]), username=f'{os.environ["USERNAME"]}', password=f'{os.environ["PASSWORD"]}')
    print(client.command('SHOW TABLES'))
    
    model_queries(client)
    return client
