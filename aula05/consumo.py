import requests   #pip install requests

URL = "http://127.0.0.1:8000"

def listar_livros():
    r = requests.get(f"{URL}/livros")
    if r.status_code == 200:
        print(r.text)

def cadastrar_livro():
    titulo = input("Digite o titulo:")
    ano  = int(input("Digite o ano:"))
    edicao = int(input("Digite a edição:"))
    livro = {
        "titulo":titulo,
        "ano": ano,
        "edicao":edicao
    }
    r = requests.post(f"{URL}/livros",json=livro)

def listar_livro(titulo):
    r = requests.get(f"{URL}/livros/{titulo}")
    if r.status_code == 200:
        print(r.text)
    elif r.status_code == 404:
        print(r.text)

def excluir_livros():
    r = requests.delete(f"{URL}/livros/{titulo}")
    if r.status_code == 200:
        print("Excluido com sucesso")

    else:
        print(r.text)
def menu():
    print(" 1 - Listar Livros")
    print(" 2 - Listar Livros pelo Titulo")
    print(" 3 - Cadastrar livros")
    print(" 4 - Deletar Livro")
    print(" 5 - sair")
    return int(input("Digite sua opção:"))

opcao = menu()
while opcao != 5:

    if opcao == 1:
        listar_livros()

    elif opcao == 2:
        titulo = input("Digite o titulo:")
        listar_livro(titulo)

    elif opcao == 3:
        cadastrar_livro()

    elif opcao == 4:
        titulo = input("Digite o titulo:")
        excluir_livros(titulo)

    opcao = menu()
    
