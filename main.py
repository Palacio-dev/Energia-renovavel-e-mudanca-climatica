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

def query(cursor):
    load_anos_meses(cursor)
    load_areas(cursor)
    load_tipo_energia(cursor)
    load_mudanca_temperatura(cursor)
    load_geracao_energia(cursor)
    load_pais_grupo(cursor)
    return 0

def main():
    conn = conectar()
    cursor = conn.cursor()
    query(cursor)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()