import sqlite3
from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)

# from flask import Blueprint, render_template, abort
# from jinja2 import TemplateNotFound

# simple_page = Blueprint('simple_page', __name__,
#                         template_folder='templates', static_folder="static")

# @simple_page.route('/')
# def show():
#     try:
#         return render_template("/simple_page/templates/index.html")
#     except TemplateNotFound:
#         return "agora"
#         # abort(404)
# app.register_blueprint(simple_page)

@app.route("/gerar", methods=['POST'])
def gerar():
    # vetTag = list(map(int, request.form.getlist('tags')))    
    # print("{tag}".format(tag=','.join(vetTag)))
    nro_questao = int(request.form.get("nro_questao"))        
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM questoes ORDER BY random() limit ?", [nro_questao])
    vetQuestao = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('prova.html', vetQuestao=vetQuestao)

@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tags")
    vetTag = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', vetTag=vetTag)

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