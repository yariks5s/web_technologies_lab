import base64
import time

from fastapi.responses import HTMLResponse
from database import startup
from helper import add_to_dict
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Request, File, Response, UploadFile, Form, Path, Query, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis
import redis

from typing import Callable, Optional, Annotated
from models import CATEGORIES
import boto3
import os

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import index

from auth import CreateUserRequest, bcrypt_context, Token, authenticate_user, timedelta, create_access_token, get_current_user

load_dotenv()
user_dependency = Annotated[dict, Depends(get_current_user)]

app = FastAPI()

rd = redis.Redis(host="localhost", port=6379, db=0)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

@app.get('/compute_consumptive/')
async def long():
    in_cache = rd.get('compute_consumptive')
    if not in_cache:
        time.sleep(2)
        print("not in cache")
        rd.set('compute_consumptive', 'new_value', 5)
    return {'response': in_cache or 'default'}

@app.on_event("startup")
async def database(**kwargs):
    global client
    client = startup()
    client.command('INSERT INTO NEWS VALUES (\'1\', \'John stole an apple\', \'Wow, this is ridiculous\', 1, 1, \'static/img/default_user.png\', \'52.3676\', \'4.9041\');')
    client.command('INSERT INTO AUTHOR VALUES (\'1\', \'John\', 55, \'john@email.com\');')
    client.command('INSERT INTO CATEGORIES VALUES (\'1\', \'Category 1\');')
    client.command('INSERT INTO CHART_DATA VALUES (\'1\', \'5\'), (\'2\', \'2\');')
 
@app.get('/is_up/')
async def is_up():
    return "OK"

@cache()
async def get_cache():
    return 1

def factorial(n: int) -> int:
    time.sleep(0.1)
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

@app.get('/check_cache/')
@cache(expire=10)
async def check_cache():
    time_start = time.time()
    res = factorial(50)
    time_gone = time.time() - time_start
    return dict(factorial_of_50_with_sleep=res, time_spent=time_gone)

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
    print(title)
    
    writer = ix.writer()
    for id, item in news_dict.items():
        print(item)
        writer.add_document(title=item['title'], content=item['description'],
                            path=item['id'])
    writer.commit()
    qp = QueryParser("content", schema=ix.schema)
    q = qp.parse(name)

    with ix.searcher() as s:
        results = s.search(q)

        for hit in results:
            print(hit.items())
        context = {"results": results}

        return templates.TemplateResponse("search_form.html", {"request": request, **context})
    
@app.get("/s3_storage_image/{filename}")
async def s3_storage(request: Request, filename: str):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket='yariksbucket', Key=filename)
    data = response['Body'].read()
    base64_data = base64.b64encode(data).decode("utf-8")
    context = {"photo": base64_data}

    return templates.TemplateResponse("photo.html", {"request": request, **context})

@app.post("/auth")
async def create_user(create_user_request: CreateUserRequest):

    client.command(f'INSERT INTO USERS VALUES (\'{create_user_request.id}\', \'{create_user_request.username}\', \'{bcrypt_context.hash(create_user_request.password)}\', \'{create_user_request.is_admin}\');')
    return {"message": "OK"}

@app.post("/auth/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    print(form_data.__str__)
    user = authenticate_user(form_data.username, form_data.password, client)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token(user['username'], user['is_admin'], timedelta(minutes=20))

    # return token    
    return {'access_token': token, 'token_type': 'bearer'}

@app.get("/check_admin")
async def admin(user: user_dependency, request: Request):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed.')
    if user['is_admin']:
        return templates.TemplateResponse("special_admin_page.html", {"request": request})
    return {"Error: ": "You are not admin"}

@app.get("/add_admin")
async def add_admin(user: user_dependency, request: Request):
    return templates.TemplateResponse("give_admin_permission.html", {"request": request})

@app.post("/add_admin")
async def add_admin(user: user_dependency):
    client.command(f'ALTER TABLE USERS UPDATE is_admin=\'1\' WHERE id={user["is_admin"]};')

