from typing import Optional

from pydantic import BaseModel

def model_queries(client):
    client.command('''CREATE TABLE IF NOT EXISTS 
                   NEWS(id String PRIMARY KEY, 
                       title String, 
                       description String, 
                       category_id UInt64,
                       author_id UInt64,
                       photo String) 
                    engine=MergeTree 
                    order by id;''')
    client.command('''CREATE TABLE IF NOT EXISTS 
                   AUTHOR(id String PRIMARY KEY, 
                        name String, 
                        likes UInt64, 
                        email String) 
                   engine=MergeTree 
                   order by id;''')
    client.command('''CREATE TABLE IF NOT EXISTS
                    CATEGORIES(id String PRIMARY KEY,
                               name String)
                    engine=MergeTree 
                    order by id;''')
