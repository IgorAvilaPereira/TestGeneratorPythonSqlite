# import psycopg2
import sqlite3
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post("/gerar", response_class=HTMLResponse)
async def gerar(tags: Annotated[int, Form()]):
    # print(tags[0])
    return tags
    # req_info = request.json()
    # print(request['tags'])
    # conn = sqlite3.connect("database.db")
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM tags")
    # vetTag = cur.fetchall()
    # cur.close()
    # conn.close()
    # return templates.TemplateResponse("prova.html", {"request": tags})

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tags")
    vetTag = cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "vetTag": vetTag})

    # conSqlite3 = sqlite3.connect("database.db")
    # curSqlite3 = conSqlite3.cursor()
    # curSqlite3.execute("INSERT INTO questoes (questao) VALUES(?)", [questao[1]])
    # conSqlite3.commit()     
    
    # conn = psycopg2.connect("host=localhost dbname=docente user=postgres password=postgres port=5432")
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM questoes;")
    # vetQuestao = cur.fetchall()
    # for questao in vetQuestao:               
    #     conSqlite3 = sqlite3.connect("database.db")
    #     curSqlite3 = conSqlite3.cursor()
    #     curSqlite3.execute("INSERT INTO questoes (questao) VALUES(?)", [questao[1]])
    #     conSqlite3.commit()    
    # cur.close()
    # conn.close()