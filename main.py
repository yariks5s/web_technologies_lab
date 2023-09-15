from database import startup
from fastapi import FastAPI, Request, File, UploadFile, Form, Path
# from PIL import Image
import base64
from fastapi.templating import Jinja2Templates
from router import router as users_router
from fastapi.responses import JSONResponse
# from database import con, create_db, users, books, chapters, authors
from forms import NewsForm
from models import CATEGORIES
from fastapi.staticfiles import StaticFiles
from PIL import Image
from io import BytesIO

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

@app.on_event("startup")
async def database(**kwargs):
    global client
    client = startup()
    client.command('INSERT INTO NEWS VALUES (\'1\', \'John killed mother\', \'Wow, this is ridiculous\', 1, 1, \'photo\');')
    client.command('INSERT INTO AUTHOR VALUES (\'1\', \'John\', 55, \'john@email.com\');')
    client.command('INSERT INTO CATEGORIES VALUES (\'1\', \'Category 1\');')
 
@app.get('/is_up/')
async def is_up():
    return "OK"

@app.get('/')
async def get_index(request: Request):

    data = client.command('SELECT *, id FROM NEWS ORDER BY id;')
    news_dict = {}

    i = 0
    while i < len(data) - 5:
        news_dict[data[i]] = {
            'title': data[i + 1],
            'description': data[i + 2],
            'category_id': data[i + 3],
            'author_id': data[i + 4],
            'photo': data[i + 5]
        }
        i += 6

    print(news_dict)
    for id, news in news_dict.items():
        print(news['title'])

    context = {"news_dict": news_dict}
    return templates.TemplateResponse("index.html", {"request": request, **context})

#region OPERATIONS ON NEWS
@app.get("/add_news/")
async def add_news(request: Request):
    return templates.TemplateResponse("news_create_form.html", {"request": request})

@app.post("/create_news/")
async def submit_form(id: str = Form('id'), title: str = Form('title'), description: str = Form('description'), category_id: str = Form('category_id'), author_id: str = Form('author_id'), photo: UploadFile = File(None)):

    photo_bytes = "static/img/default_user.png"

    client.command(f'INSERT INTO NEWS VALUES (\'{id}\', \'{title}\', \'{description}\', \'{category_id}\', \'{author_id}\', \'{photo_bytes}\');')
    # Create a news instance.

    # Return the ID of the newly created news instance.
    return {"message": "Form submitted successfully."}

@app.get("/change_news/{id}")
async def add_news(request: Request, id: int):
    print(id)
    data = client.command(f'SELECT *, id FROM NEWS WHERE id={id};')
    news_dict = {}
    i = 0
    while i < len(data) - 5:
        news_dict[data[i]] = {
            'id': data[i],
            'title': data[i + 1],
            'description': data[i + 2],
            'category_id': data[i + 3],
            'author_id': data[i + 4],
            'photo': data[i + 5]
        }
        i += 6
    print(news_dict)

    context = {"news_dict": news_dict}
    return templates.TemplateResponse("news_alter_form.html", {"request": request, **context})

@app.post("/create_news/{news_id}")
async def submit_form(news_id: int, title: str = Form('title'), description: str = Form('description'), category_id: str = Form('category_id'), author_id: str = Form('author_id'), photo: str = Form('photo')):

    # Create a news instance.
    client.command(f'ALTER TABLE NEWS UPDATE title=\'{title}\', description=\'{description}\', category_id=\'{category_id}\', author_id=\'{author_id}\', photo=\'{photo}\' WHERE id={news_id};')

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
