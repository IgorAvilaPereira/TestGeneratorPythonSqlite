# import psycopg2

import sqlite3
from flask import Flask, redirect, url_for
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


@app.route("/tela_adicionar_questao", methods=['GET'])
def tela_adicionar_questao():
    return render_template('tela_adicionar_questao.html')

@app.route("/tela_adicionar_tag", methods=['GET'])
def tela_adicionar_tag():
    return render_template('tela_adicionar_tag.html')

@app.route("/tela_adicionar_tags/<int:id>", methods=['GET'])
def tela_adicionar_tags(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM questoes where questoes.id = ?", [id])
    questao = cur.fetchone()

    cur.execute("SELECT * FROM tags")    
    vetTag = cur.fetchall()

    cur.execute("SELECT tag_id FROM questoes inner join questoes_tags on (questoes.id = questao_id) where questoes.id = ?", [id])
    vetQuestaoTag = []
    for i in cur.fetchall():
        vetQuestaoTag.append(i[0])
    cur.close()
    conn.close()
    return render_template('tela_adicionar_tags.html', vetTag=vetTag, questao=questao, vetQuestaoTag=vetQuestaoTag)    
    

@app.route("/tela_alterar_questao/<int:id>", methods=['GET'])
def tela_alterar_questao(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM questoes where id = ?", [id])
    # conn.commit()   
    questao = cur.fetchone()
    cur.close()
    conn.close()
    # return redirect(url_for('index'))
    return render_template('tela_alterar_questao.html', questao=questao)

@app.route("/tela_alterar_tag/<int:id>", methods=['GET'])
def tela_alterar_tag(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tags where id = ?", [id])
    # conn.commit()   
    tag = cur.fetchone()
    cur.close()
    conn.close()
    # return redirect(url_for('index'))
    return render_template('tela_alterar_tag.html', tag=tag)

@app.route("/remover_tag/<int:id>", methods=['GET'])
def remover_tag(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM tags where id = ?", [id])
    conn.commit()   
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route("/adicionar_tags", methods=['POST'])
def adicionar_tags():
    id = int(request.form.get("id"))
    
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM questoes_tags WHERE questao_id = ?;", [id])
    conn.commit()   

    for tag_id in request.form.getlist('tags'):    
        cur.execute("INSERT INTO questoes_tags (questao_id, tag_id) VALUES(?,?);", [id, tag_id])    
        conn.commit()   

    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route("/alterar_tag", methods=['POST'])
def alterar_tag():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    tag = request.form.get("tag")   
    id = int(request.form.get("id"))
    cur.execute("UPDATE tags SET tag = ? where id = ?", [tag, id])
    conn.commit()   
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route("/alterar_questao", methods=['POST'])
def alterar_questao():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    questao = request.form.get("questao")   
    id = int(request.form.get("id"))
    cur.execute("UPDATE questoes SET questao = ? where id = ?", [questao, id])
    conn.commit()   
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route("/remover_questao/<int:id>", methods=['GET'])
def remover_questao(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM questoes where id = ?", [id])
    conn.commit()   
    cur.close()
    conn.close()
    return redirect(url_for('listar_questao'))

@app.route("/adicionar_tag", methods=['POST'])
def adicionar_tag():
    tag = request.form.get("tag")        
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO tags (tag) VALUES (?)", [tag])
    conn.commit()   
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route("/adicionar_questao", methods=['POST'])
def adicionar_questao():
    questao = request.form.get("questao")        
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO questoes (questao) VALUES (?)", [questao])
    conn.commit()   
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route("/gerar", methods=['POST'])
def gerar():
    vetTag = list(map(int, request.form.getlist('tags')))    

    nro_questao = int(request.form.get("nro_questao"))        
    
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    
    if (vetTag is not None):
        if (len(vetTag) > 0):
            tags = "("
            for t in vetTag:
                tags = tags + str(t) + ","
            tags = tags + ")"
            tags = tags.replace(",)", ")")         

            cur.execute("SELECT * FROM questoes inner join questoes_tags where tag_id in "+tags+" ORDER BY random() limit "+nro_questao)
        else:
            print("aqui2")
            cur.execute("SELECT * FROM questoes ORDER BY random() limit "+nro_questao)
    else:
        print("aqui")
        cur.execute("SELECT * FROM questoes ORDER BY random() limit "+nro_questao)
    
    vetQuestao = cur.fetchall()
    
    cur.close()
    conn.close()
    return render_template('prova.html', vetQuestao=vetQuestao)

@app.route("/listar_questao")
def listar_questao():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM questoes")
    vet = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('listar_questao.html', vet=vet)

@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tags")
    vetTag = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', vetTag=vetTag)

# @app.route("/importar")
# def importar():
#     # conSqlite3 = sqlite3.connect("database.db")
#     # curSqlite3 = conSqlite3.cursor()
#     # curSqlite3.execute("INSERT INTO questoes (questao) VALUES(?)", [questao[1]])
#     # conSqlite3.commit()     
    
#     conn = psycopg2.connect("host=localhost dbname=docente user=postgres password=postgres port=5432")
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM avaliacoes where descricao is not null;")
#     vetQuestao = cur.fetchall()
#     for questao in vetQuestao:   
#         # print(questao)            
#         conSqlite3 = sqlite3.connect("database.db")
#         curSqlite3 = conSqlite3.cursor()
#         curSqlite3.execute("INSERT INTO questoes (questao) VALUES(?)", [questao[2]])
#         conSqlite3.commit()    
#     cur.close()
#     conn.close()
#     return "ok"