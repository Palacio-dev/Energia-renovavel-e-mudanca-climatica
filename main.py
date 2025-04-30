import psycopg2
from extract import *

def main():
    conn = psycopg2.connect(
        dbname="EnergiaTempDB",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    query(cursor)

    conn.commit()
    cursor.close()
    conn.close()

# AÇÃO USANDO A CONEXÃO COM OO DB
def query(cursor):
    #load_anos_meses()
    load_areas(cursor)

    return 0

if __name__ == '__main__':
    main()