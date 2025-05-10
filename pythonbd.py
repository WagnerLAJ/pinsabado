#pip install mysql-connector-python
#pip install pandas

import mysql.connector
import pandas as pd
from mysql.connector import Error

nomeColuna1 = "ID"
nomeColuna2 = "Descrição"
nomeColuna3 = "Fabricante"
nomeColuna4 = "Valor"

dataframe = pd.DataFrame()


def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',          # Altere para o seu host
            user='root',        # Altere para seu usuário
            password='',      # Altere para sua senha
            database='pinrelacionamento'  # Altere para seu banco de dados
        )
        if connection.is_connected():
            print("Conexão com o banco de dados estabelecida com sucesso.")
            return connection
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def insert_data(connection, descricao, fabricante, valor):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO produtos (descricao, fabricante, valor) VALUES (%s, %s, %s)"
        values = (descricao, fabricante, valor)
        cursor.execute(query, values)
        connection.commit()
        print("Dados inseridos com sucesso.")
    except Error as e:
        print(f"Erro ao inserir dados: {e}")
    finally:
        cursor.close()

def update_data(connection, id, descricao, fabricante, valor):
    try:
        cursor = connection.cursor()
        query = "UPDATE produtos SET descricao = %s, fabricante = %s, valor = %s  WHERE id = %s"
        values = (descricao, fabricante, valor, id)
        cursor.execute(query, values)
        connection.commit()
        print("Dados atualizados com sucesso.")
    except Error as e:
        print(f"Erro ao atualizar dados: {e}")
    finally:
        cursor.close()

def delete_data(connection, id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM produtos WHERE id = %s"
        values = (id,)
        cursor.execute(query, values)
        connection.commit()
        print("Dados deletados com sucesso.")
    except Error as e:
        print(f"Erro ao deletar dados: {e}")
    finally:
        cursor.close()

def read_data(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM produtos"
        cursor.execute(query)
        rows = cursor.fetchall()
        listaColuna1 = []
        listaColuna2 = []
        listaColuna3 = []
        listaColuna4 = []
        for row in rows:
            listaColuna1.append(row[0]) 
            listaColuna2.append(row[1])
            listaColuna3.append(row[2])
            listaColuna4.append(row[3])
            #print(row)
        dataframe = pd.DataFrame()
        dataframe[nomeColuna1] = listaColuna1
        dataframe[nomeColuna2] = listaColuna2
        dataframe[nomeColuna3] = listaColuna3
        dataframe[nomeColuna4] = listaColuna4
        print(dataframe)
    except Error as e:
        print(f"Erro ao ler dados: {e}")
    finally:
        cursor.close()

def read_transacional(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM vendas"
        cursor.execute(query)
        rows = cursor.fetchall()
        listaColuna1 = []
        listaColuna2 = []
        listaColuna3 = []
        listaColuna4 = []
        listaColuna5 = []
        for row in rows:
            listaColuna1.append(row[0]) 
            listaColuna2.append(row[1])
            listaColuna3.append(row[2])
            listaColuna4.append(row[3])
            listaColuna5.append(row[4])
            #print(row)
        dataframe = pd.DataFrame()
        dataframe["id"] = listaColuna1
        dataframe["datadia"] = listaColuna2
        dataframe["qtd"] = listaColuna3
        dataframe["ref_produto"] = listaColuna4
        dataframe["ref_cliente"] = listaColuna5
        print(dataframe)
    except Error as e:
        print(f"Erro ao ler dados: {e}")
    finally:
        cursor.close()
def read_analitica(connection):
    try:
        cursor = connection.cursor()
        query = '''select vendas.datadia, vendas.qtd,cliente.nome,cliente.sobrenome,produtos.descricao,produtos.valor
                    from vendas 
                    join cliente on vendas.ref_cliente=cliente.id
                    join produtos on vendas.ref_produto=produtos.id'''
        cursor.execute(query)
        rows = cursor.fetchall()
        listaColuna1 = []
        listaColuna2 = []
        listaColuna3 = []
        listaColuna4 = []
        listaColuna5 = []
        listaColuna6 = []
        for row in rows:
            listaColuna1.append(row[0]) 
            listaColuna2.append(row[1])
            listaColuna3.append(row[2])
            listaColuna4.append(row[3])
            listaColuna5.append(row[4])
            listaColuna6.append(row[5])
            #print(row)
        dataframe = pd.DataFrame()
        dataframe["datadia"] = listaColuna1
        dataframe["qtd"] = listaColuna2
        dataframe["nome"] = listaColuna3
        dataframe["sobrenome"] = listaColuna4
        dataframe["descricao"] = listaColuna5
        dataframe["valor"] = listaColuna6
        print(dataframe)
    except Error as e:
        print(f"Erro ao ler dados: {e}")
    finally:
        cursor.close()

def main():
    """Função principal do script."""
    connection = connect_to_database()
    if connection:
        while True:
            print("\nEscolha uma opção:")
            print("1. Inserir produto")
            print("2. Atualizar produto")
            print("3. Deletar produto")
            print("4. Ler produto")
            print("5. Ler transacinal")
            print("6. Ler analítica")
            print("7. Sair\n")
            choice = input("Digite o número da opção: ")

            if choice == '1':
                nome = input("Digite o nome do produto: ")
                fabricante = input("Digite o fabricante do produto: ")
                valor = float(input("Digite o valor do produto: "))
                insert_data(connection, nome, fabricante, valor)
            elif choice == '2':
                id = int(input("Digite o ID do produto para atualizar: "))
                nome = input("Digite o novo nome: ")
                fabricante = input("Digite o novo fabricante do produto: ")
                valor = float(input("Digite o novo valor do produto: "))
                update_data(connection, id, nome, fabricante, valor)
            elif choice == '3':
                id = int(input("Digite o ID do produto para deletar: "))
                delete_data(connection, id)
            elif choice == '4':
                print("Dados da tabela 'produtos':")
                read_data(connection)
            elif choice == '5':
                print("Dados da tabela transacional:")
                read_transacional(connection)
            elif choice == '6':
                print("Dados da tabela analítica:")
                read_analitica(connection)
            elif choice == '7':
                break
            else:
                print("Opção inválida. Tente novamente.")

        connection.close()

if __name__ == "__main__":
    main()
