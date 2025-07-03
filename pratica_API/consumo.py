import requests

if __name__ == "__main__":
    url = "http://127.0.0.1:8000"

    def listar_livros():
        r = requests.get(f"{url}/livros")
        if r.status_code == 200:
            print(r.text)
        else:
            print(f"Erro: {r.status_code}")

    def cadastrar_livro():
        titulo = input("Digite o título do livro: ")
        ano = int(input("Digite o ano do livro: "))
        edicao = int(input("Digite a edição do livro: "))
        livro = {
            "titulo": titulo,
            "ano": ano,
            "edicao": edicao
        }
        r = requests.post(f"{url}/livros", json=livro)
        print(f"Resposta: {r.status_code} - {r.text}")

    def pesquisar_livro(pesquisa):
        r = requests.get(f"{url}/livros/{pesquisa}")
        if r.status_code == 200:
            print(r.text)
        elif r.status_code == 400:
            print(r.text)
        else:
            print("Livro não encontrado.")

    def editar_livro():
        titulo = input("Digite o título do livro que deseja editar: ")
        r = requests.get(f"{url}/livros/{titulo}")

        if r.status_code == 200:
            print("Livro encontrado. Digite os novos dados:")
            novo_titulo = input("Novo título: ")
            novo_ano = int(input("Novo ano: "))
            nova_edicao = int(input("Nova edição: "))

            novos_dados = {
                "titulo": novo_titulo,
                "ano": novo_ano,
                "edicao": nova_edicao
            }

            r_put = requests.put(f"{url}/livros/{titulo}", json=novos_dados)

            if r_put.status_code == 200:
                print("Livro atualizado com sucesso.")
            else:
                print(f"Erro ao atualizar o livro: {r_put.text}")
        else:
            print("Livro não encontrado.")

    def excluir_livros(titulo):
        r = requests.delete(f"{url}/livros/{titulo}")
        if r.status_code == 200:
            print("Excluído com sucesso")
        else:
            print(r.text)

    def menu():
        print("\nMENU:")
        print(" 1 - Listar livros cadastrados")
        print(" 2 - Pesquisar livro por título")
        print(" 3 - Cadastrar um livro")
        print(" 4 - Editar livro")
        print(" 5 - Deletar livro")
        print(" 6 - Sair")
        return int(input("Digite sua opção: "))

    opcao = menu()
    while opcao != 6:
        if opcao == 1:
            listar_livros()
        elif opcao == 2:
            titulo = input("Digite o título: ")
            pesquisar_livro(titulo)
        elif opcao == 3:
            cadastrar_livro()
        elif opcao == 4:
            editar_livro()
        elif opcao == 5:
            titulo = input("Digite o título: ")
            excluir_livros(titulo)
        else:
            print("Opção inválida.")
        opcao = menu()
