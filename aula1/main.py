# API SIMPLES - Genciador de tarefas (Sem BD - armazenamento em memória)
# pip install fastapi uvicorn pydantic ; pip freeze > requirements.text 
#uvicorn main:app - Copiar URL e colocar /docs

from fastapi import FastAPI, HTTPException
from models import Tarefa
from typing import List

app = FastAPI()

tarefas:List[Tarefa] = []

@app.get("/tarefas/",response_model=List[Tarefa])
def listar_tarefas():
    return tarefas

@app.get("/tarefas/{id}", response_model=Tarefa)
def listar_tarefa(id:int):
    for tarefa in tarefas:
        if tarefa.id == id:
            return tarefa
    raise HTTPException(status_code=404, detail="Não encontrada")

@app.post("/tarefas/",response_model=Tarefa)
def criar_tarefa(tarefa:Tarefa):
    tarefas.append(tarefa)
    return tarefa

