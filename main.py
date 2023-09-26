from django.http import JsonResponse
from elasticsearch import Elasticsearch
from database import startup
from fastapi import FastAPI, Request, File, UploadFile, Form, Path, Query, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Callable, Optional
from fastapi.templating import Jinja2Templates
from models import CATEGORIES
from fastapi.staticfiles import StaticFiles
import os
from helper import add_to_dict
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
ELASTIC_QUERY_MAX_SIZE = 15

SECRET_KEY = "c90bacd9ba5d2bd54589318dddb1326883c16341e3badde22bb6e4f21f695d70"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

@app.on_event("startup")
async def database(**kwargs):
    global client
    client = startup()
    # client.command('INSERT INTO NEWS VALUES (\'1\', \'John stole an apple\', \'Wow, this is ridiculous\', 1, 1, \'static/img/default_user.png\', \'52.3676\', \'4.9041\');')
    client.command('INSERT INTO AUTHOR VALUES (\'1\', \'John\', 55, \'john@email.com\');')
    client.command('INSERT INTO CATEGORIES VALUES (\'1\', \'Category 1\');')
    client.command('INSERT INTO CHART_DATA VALUES (\'1\', \'5\'), (\'2\', \'2\');')
 
@app.get('/is_up/')
async def is_up():
    return "OK"

@app.get('/')
async def get_index(request: Request):

    data = client.command('SELECT *, id FROM NEWS ORDER BY id;')
    news_dict = add_to_dict(data)

    context = {"news_dict": news_dict}
    print(news_dict)
    return templates.TemplateResponse("index.html", {"request": request, **context})

#region OPERATIONS ON NEWS
@app.get('/get_news/{id}')
async def get_news(request: Request, id: str):
    availability = client.command(f'SELECT count(*) FROM NEWS WHERE id=\'{id}\';')
    if (availability == 0):
        return {"message": "Something went wrong"}
    data = client.command(f'SELECT *, id FROM NEWS WHERE id=\'{id}\';')
    news_dict = add_to_dict(data)

    context = {"news_dict": news_dict, "api_key": os.environ['MAPS_API_KEY']}
    print(news_dict)
    return templates.TemplateResponse("news_get_form.html", {"request": request, **context})

@app.get("/add_news/")
async def add_news(request: Request):
    return templates.TemplateResponse("news_create_form.html", {"request": request})

@app.post("/create_news/")
async def submit_form(id: str = Form('id'), title: str = Form('title'), description: str = Form('description'), category_id: str = Form('category_id'), author_id: str = Form('author_id'), coord_lat: str = Form('coord_lat'), coord_lon: str = Form('coord_lon')):

    photo_bytes = "static/img/default_user.png"

    client.command(f'INSERT INTO NEWS VALUES (\'{id}\', \'{title}\', \'{description}\', \'{category_id}\', \'{author_id}\', \'{photo_bytes}\', \'{coord_lat}\', \'{coord_lon}\');')
    # Create a news instance.

    # Return the ID of the newly created news instance.
    return {"message": "Form submitted successfully."}

@app.get("/change_news/{id}")
async def add_news(request: Request, id: int):
    print(id)
    data = client.command(f'SELECT *, id FROM NEWS WHERE id={id};')
    news_dict = add_to_dict(data)

    context = {"news_dict": news_dict}
    return templates.TemplateResponse("news_alter_form.html", {"request": request, **context})

@app.post("/create_news/{news_id}")
async def submit_form(news_id: int, title: str = Form('title'), description: str = Form('description'), category_id: str = Form('category_id'), author_id: str = Form('author_id'), photo: str = Form('photo'), coord_lat: str = Form('coord_lat'), coord_lon: str = Form('coord_lon')):

    # Create a news instance.
    client.command(f'ALTER TABLE NEWS UPDATE title=\'{title}\', description=\'{description}\', category_id=\'{category_id}\', author_id=\'{author_id}\', photo=\'{photo}\', coord_lat=\'{coord_lat}\', coord_lon=\'{coord_lon}\' WHERE id={news_id};')

    # Return the ID of the newly created news instance.
    return {"message": "Form submitted successfully."}

@app.get("/delete_news/{news_id}")
async def delete_news(news_id: int):
    client.command(f'DELETE FROM NEWS WHERE id={news_id}')

    return {"message": "Deleting submitted successfully."}
#endregion

#region OPERATIONS ON AUTHOR
@app.get("/add_author/")
async def add_news(request: Request):
    return templates.TemplateResponse("author_create_form.html", {"request": request})

@app.post("/create_author/")
async def submit_form(id: str = Form('id'), name: str = Form('name'), likes: str = Form('likes'), email: str = Form('email')):

    # Create a news instance.
    client.command(f'INSERT INTO AUTHOR VALUES (\'{id}\', \'{name}\', \'{likes}\', \'{email}\');')

    # Return the ID of the newly created news instance.
    return {"message": "Form submitted successfully."}

@app.get("/change_author/{id}")
async def change_author(request: Request, id: int):
    data = client.command(f'SELECT *, id FROM AUTHOR WHERE id={id};')
    author_dict = {}
    i = 0
    while i < len(data) - 3:
        author_dict[data[i]] = {
            'id': data[i],
            'name': data[i + 1],
            'likes': data[i + 2],
            'email': data[i + 3],
        }
        i += 4
    print(author_dict)

    context = {"author_dict": author_dict}
    return templates.TemplateResponse("author_alter_form.html", {"request": request, **context})

@app.post("/create_author/{author_id}")
async def submit_form(author_id: int, name: str = Form('name'), likes: str = Form('likes'), email: str = Form('email')):

    # Create a news instance.
    client.command(f'ALTER TABLE AUTHOR UPDATE name=\'{name}\', likes=\'{likes}\', email=\'{email}\' WHERE id={author_id};')

    # Return the ID of the newly created news instance.
    return {"message": "Form submitted successfully."}


@app.get("/delete_author/{author_id}")
async def delete_author(author_id: int):
    client.command(f'DELETE FROM AUTHOR WHERE id={author_id}')

    return {"message": "Deleting submitted successfully."}

#endregion

#region OPERATIONS ON CATEGORIES
@app.get('/get_categories/{id}')
async def get_news(request: Request, id: str):
    availability = client.command(f'SELECT count(*) FROM CATEGORIES WHERE id=\'{id}\';')
    if (availability == 0):
        return {"message": "Something went wrong"}
    data = client.command(f'SELECT *, id FROM CATEGORIES WHERE id=\'{id}\';')
    categories_dict = {}
    i = 0
    while i < len(data) - 1:
        categories_dict[data[i]] = {
            'id': data[i],
            'name': data[i + 1],
        }
        i += 2

    context = {"categories_dict": categories_dict}
    return templates.TemplateResponse("categories_get_form.html", {"request": request, **context})

@app.get("/add_categories/")
async def add_news(request: Request):
    return templates.TemplateResponse("categories_create_form.html", {"request": request})

@app.post("/create_categories/")
async def submit_form(id: str = Form('id'), name: str = Form('name')):

    # Create a news instance.
    client.command(f'INSERT INTO CATEGORIES VALUES (\'{id}\', \'{name}\');')

    # Return the ID of the newly created news instance.
    return {"message": "Form submitted successfully."}

@app.post("/createJSON_categories/")
async def submit_form(categories: CATEGORIES):
    try:
        client.command(f'INSERT INTO CATEGORIES VALUES (\'{categories.id}\', \'{categories.name}\');')
        return {"message": "OK"}
    except:
        return {"message": "FATAL"}

@app.get("/change_categories/{id}")
async def change_author(request: Request, id: int):
    data = client.command(f'SELECT *, id FROM CATEGORIES WHERE id=\'{id}\';')
    categories_dict = {}
    i = 0
    while i < len(data) - 1:
        categories_dict[data[i]] = {
            'id': data[i],
            'name': data[i + 1],
        }
        i += 2
    print(categories_dict)

    context = {"categories_dict": categories_dict}
    return templates.TemplateResponse("categories_alter_form.html", {"request": request, **context})

@app.put("/changeJSON_categories/")
async def submit_form(categories: CATEGORIES):
    try:
        client.command(f'ALTER TABLE CATEGORIES UPDATE name = \'{categories.name}\' WHERE id = \'{categories.id}\';')
        return {"message": "OK"}
    except:
        return {"message": "FATAL"}

@app.post("/create_categories/{categories_id}")
async def submit_form(categories_id: int, name: str = Form('name')):

    # Create a news instance.
    client.command(f'ALTER TABLE CATEGORIES UPDATE name=\'{name}\' WHERE id=\'{categories_id}\';')

    # Return the ID of the newly created news instance.
    return {"message": "Form submitted successfully."}

@app.get("/delete_categories/{categories_id}")
async def delete_categories(categories_id: int):
    client.command(f'DELETE FROM CATEGORIES WHERE id=\'{categories_id}\'')

    return {"message": "Deleting submitted successfully."}

@app.delete("/deleteJSON_categories/")
async def delete_categories(categories: CATEGORIES):
    try:
        client.command(f'DELETE FROM CATEGORIES WHERE id=\'{categories.id}\'')
        return {"message": "OK"}
    except:
        return {"message": "FATAL"}

#endregion

@app.get("/chart")
async def chart(request: Request):
    availability = client.command(f'SELECT count(*) FROM CHART_DATA;')
    if (availability == 0):
        return {"message": "Something went wrong"}
    data = client.command(f'SELECT *, id FROM CHART_DATA;')
    data_dict = {}
    i = 0
    while i < len(data) - 1:
        data_dict[data[i]] = {
            'id': data[i][-(len(data[i])-2)//2:],
            'data': data[i + 1],
        }
        i += 2
    context = {"data_dict": data_dict}
    return templates.TemplateResponse("chart_example.html", {"request": request, **context})

from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh.query import Every
from whoosh import index

@app.get("/search")
async def search(request: Request, name: str = Form('name')):
    return templates.TemplateResponse("search_form.html", {"request": request})

@app.post("/search")
async def results(request: Request, name: str = Form('name')):
    # schema = Schema(path=ID(stored=True, unique=True), content=TEXT, doc=STORED, title=TEXT)

    # writer = ix.writer()
    data = client.command('SELECT *, id FROM NEWS ORDER BY id;')
    news_dict = add_to_dict(data)
    print(news_dict['1']['description'])
    content=news_dict['1']['description']
    myid=news_dict['1']['id']
    title=news_dict['1']['title']

    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored = True))
 
    try:
        os.mkdir('indexdir')
        ix = create_in("indexdir", schema)
    except:
        print("indexdir already exists")
        ix = open_dir('indexdir')

    ix = index.create_in("indexdir", schema)
    print(content)
    
    writer = ix.writer()
    writer.add_document(title=title, content=content,
                        path=u"/a")
    writer.add_document(title=u"Second try", content=u"This is the second example hello world.",
                        path=u"/b")
    writer.add_document(title=u"Third time's the charm", content=u"More examples. Examples are many.",
                        path=u"/c")
    writer.commit()
    with ix.searcher() as searcher:
        print(name)
        query = QueryParser("content", ix.schema).parse(name)
        results = searcher.search(query, terms=True)
        print(results)
        
        for r in results:
            print (r, r.score)
            # Was this results object created with terms=True?
            if results.has_matched_terms():
                # What terms matched in the results?
                print(results.matched_terms())
            
        # What terms matched in each hit?
        print ("matched terms")
        for hit in results:
            print(hit.matched_terms())

        # return templates.TemplateResponse("search_form.html", {"request": request, **context})