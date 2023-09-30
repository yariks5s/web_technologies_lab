from typing import Optional

from pydantic import BaseModel

def model_queries(client):
    client.command('''CREATE TABLE IF NOT EXISTS 
                   NEWS(id String PRIMARY KEY, 
                       title String, 
                       description String, 
                       category_id UInt64,
                       author_id UInt64,
                       photo String,
                       coord_lat String,
                       coord_lon String) 
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
                               name Nullable(String))
                    engine=MergeTree 
                    order by id;''')
    client.command('''CREATE TABLE IF NOT EXISTS
                    CHART_DATA(id String PRIMARY KEY,
                               data String)
                    engine=MergeTree
                    order by id;''')
    client.command('''CREATE TABLE IF NOT EXISTS
                    USERS(id String PRIMARY KEY,
                            username String,
                            password String,
                            is_admin String)
                    engine=MergeTree
                    order by id;''')

class CATEGORIES(BaseModel):
    id: str
    name: str
