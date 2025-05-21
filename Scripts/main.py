import psycopg2
from load_data import *

def conectar():
    return psycopg2.connect(
        dbname='EnergiaTempDB',
        user='postgres',
        password='',
        host='localhost',
        port='5432'
    ) 

def load_datasets(cursor):
    load_anos_meses(cursor)
    load_areas(cursor)
    load_tipo_energia(cursor)
    load_mudanca_temperatura(cursor)
    load_geracao_energia(cursor)
    load_pais_grupo(cursor)

def consulta(conn, n_consulta: int):
    with open(f'../Consultas/consulta0{n_consulta}.sql', "r", encoding="utf-8") as file:
        sql = file.read()

    df = pd.read_sql_query(sql, conn) 
    df.to_csv(f'../Resultado_Consultas/consulta0{n_consulta}.csv', index=False)

def main():
    conn = conectar()
    cursor = conn.cursor()

    #load_datasets(cursor)

    for i in range(1, 6):
        consulta(conn, i)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()