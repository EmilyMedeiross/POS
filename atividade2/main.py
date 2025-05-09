from fastapi import FastAPI, HTTPException, status
from models import (
    LivroCriacao, LivroResposta,
    UsuarioCriacao, UsuarioResposta,
    EmprestimoResposta, bd
)
from uuid import UUID, uuid4
from datetime import date
from typing import List, Optional

app = FastAPI()


@app.post("/livros/", response_model=LivroResposta, status_code=status.HTTP_201_CREATED)
def cadastrar_livro(livro: LivroCriacao):

    novo_livro = livro.model_dump()
    novo_livro.update({
        "id": uuid4(),
        "disponivel": True
    })
    bd.livros.append(novo_livro)
    return novo_livro

@app.get("/livros/", response_model=List[LivroResposta])
def listar_livros(disponivel: Optional[bool] = None):
   
    if disponivel is None:
        return bd.livros
    return [livro for livro in bd.livros if livro["disponivel"] == disponivel]


@app.post("/usuarios/", response_model=UsuarioResposta, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(usuario: UsuarioCriacao):

    novo_usuario = usuario.model_dump()
    novo_usuario.update({
        "id": uuid4(),
        "livros_emprestados": []
    })
    bd.usuarios.append(novo_usuario)
    return novo_usuario

@app.post("/emprestimos/", response_model=EmprestimoResposta, status_code=status.HTTP_201_CREATED)
def emprestar_livro(livro_id: UUID, usuario_id: UUID):

    livro = next((l for l in bd.livros if l["id"] == livro_id), None)
    usuario = next((u for u in bd.usuarios if u["id"] == usuario_id), None)
    
    if not livro:
        raise HTTPException(404, "Livro não encontrado")
    if not livro["disponivel"]:
        raise HTTPException(400, "Livro já emprestado")
    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")
    
    livro["disponivel"] = False
    usuario["livros_emprestados"].append(livro_id)
    
    novo_emprestimo = {
        "id": uuid4(),
        "livro_id": livro_id,
        "usuario_id": usuario_id,
        "data_emprestimo": date.today(),
        "data_devolucao": None
    }
    bd.emprestimos.append(novo_emprestimo)
    return novo_emprestimo

@app.put("/emprestimos/devolver/", response_model=EmprestimoResposta)
def devolver_livro(livro_id: UUID, usuario_id: UUID):

    emprestimo = next(
        (e for e in bd.emprestimos 
         if e["livro_id"] == livro_id 
         and e["usuario_id"] == usuario_id 
         and e["data_devolucao"] is None),
        None
    )
    
    if not emprestimo:
        raise HTTPException(404, "Empréstimo ativo não encontrado")
    
    livro = next((l for l in bd.livros if l["id"] == livro_id), None)
    usuario = next((u for u in bd.usuarios if u["id"] == usuario_id), None)
    
    if livro:
        livro["disponivel"] = True
    if usuario and livro_id in usuario["livros_emprestados"]:
        usuario["livros_emprestados"].remove(livro_id)
    
    emprestimo["data_devolucao"] = date.today()
    return emprestimo

@app.get("/usuarios/{usuario_id}/livros", response_model=List[LivroResposta])
def livros_do_usuario(usuario_id: UUID):

    usuario = next((u for u in bd.usuarios if u["id"] == usuario_id), None)
    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")
    
    return [livro for livro in bd.livros if livro["id"] in usuario["livros_emprestados"]]

@app.get("/emprestimos/historico", response_model=List[EmprestimoResposta])
def historico_emprestimos():
    
    return bd.emprestimos