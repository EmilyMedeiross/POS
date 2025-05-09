from pydantic import BaseModel
from uuid import UUID, uuid4
from datetime import date
from typing import List, Optional

class LivroCriacao(BaseModel):
    titulo: str
    autor: str
    ano_publicacao: int

class LivroResposta(LivroCriacao):
    id: UUID
    disponivel: bool

class UsuarioCriacao(BaseModel):
    nome: str

class UsuarioResposta(UsuarioCriacao):
    id: UUID
    livros_emprestados: List[UUID] = []

class EmprestimoResposta(BaseModel):
    id: UUID
    livro_id: UUID
    usuario_id: UUID
    data_emprestimo: date
    data_devolucao: Optional[date] = None

class BancoDeDados:
    def __init__(self):
        self.livros: List[dict] = []
        self.usuarios: List[dict] = []
        self.emprestimos: List[dict] = []


bd = BancoDeDados()