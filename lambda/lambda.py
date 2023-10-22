from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

@app.get('/is_up/')
async def is_up():
    return "OK"

@app.get('/')
async def index():
    return {"Program": "this is an index page of the program"}

