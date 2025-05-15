# API SIMPLES - Genciador de tarefas (Sem BD - armazenamento em memória)
# pip install fastapi uvicorn pydantic ; pip freeze > requirements.text 
#uvicorn main:app - Copiar URL e colocar /docs

from fastapi import FastAPI, HTTPException
from typing import List
from models import Usuario, Livro, Emprestimo 
from datetime import date 
import uuid

acervo:List[Livro] = []
usuarios:List[Usuario] = []

app = FastAPI()

@app.post("/livros", response_model=Livro)
def cadastrar_livros(livro:Livro):
    livro.uuid = uuid.uuid4()
    acervo.append(livro)
    return livro

@app.get("/livros", response_model=List[Livro])
def listar_livros():
    return acervo

@app.get("/livros/{titulo}", response_model=Livro)
def listar_livros(titulo:str ):
    for livro in acervo:
        if livro.titulo == titulo:
            return livro
    return HTTPException(404, "Livro não encontrado")

@app.post("/usuarios", response_model=Usuario)
def cadastrar_usuarios(usuario:Usuario):
    usuario.uuid = str(uuid.uuid4())
    usuarios.append(usuario)
    return usuario

@app.post("/emprestimo", response_model=Emprestimo)
def emprestimo(usuario:str, livro:str, data_emprestimo:date, data_devolucao:date):
    user = None 
    book = None
    for u in usuarios:
        if u.uuid == usuario:
            user = u

    for l in acervo:
        if l.uuid == livro:
            if l.disponibilidade:
             book = l
             
    if book and user:
        dados ={
            "usuario":user,
            "livro":book,
            "emprestimo":data_emprestimo,
            "devolucao":data_devolucao
        }
        emprestimo = Emprestimo(**dados)
        emprestimos.append(emprestimo)
        return emprestimo

    raise HTTPException(404, "Emprestimo não realizado")