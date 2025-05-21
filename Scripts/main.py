'''
MC536 - Grupo 1
Este é o código principal para rodar as transações no banco de dados.

OBS:
- import do load_data.py que contém as funções que lêem os datasets e carregam pras tabelas
- a função de consulta acessa os arquivos .sql na pasta Consultas do repositório
'''

import psycopg2
from load_data import *

def main():

    # conexão com o banco
    conn = conectar()
    cursor = conn.cursor()

    # carrega todos os dados no banco
    #load_datasets(cursor)

    # roda as 5 consultas
    for i in range(1, 6):
        consulta(conn, i)

    # salva e fecha a conexão com o banco
    conn.commit()
    cursor.close()
    conn.close()


# estabele a conexão base com o banco
def conectar():
    return psycopg2.connect(
        dbname='EnergiaTempDB',
        user='postgres',
        password='',
        host='localhost',
        port='5432'
    ) 

# chama as funções de load de load_data
def load_datasets(cursor):
    load_anos_meses(cursor)
    load_areas(cursor)
    load_tipo_energia(cursor)
    load_mudanca_temperatura(cursor)
    load_geracao_energia(cursor)
    load_pais_grupo(cursor)

# roda a query no arquivo consulta0X.sql da pasta Consultas do repositório e salva em csv na pasta Resultado_Consultas
# onde X é o n_consulta
def consulta(conn, n_consulta: int):
    with open(f'../Consultas/consulta0{n_consulta}.sql', "r", encoding="utf-8") as file:
        sql = file.read()

    df = pd.read_sql_query(sql, conn) 
    df.to_csv(f'../Resultado_Consultas/consulta0{n_consulta}.csv', index=False)

if __name__ == '__main__':
    main()