import psycopg2

conn = psycopg2.connect(
    dbname="raDoPalacio",
    user="postgres",
    password="senha",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()


sql = """
COPY *entidade* (atributos, ordem, no, csv)
FROM STDIN WITH (
    FORMAT CSV,
    HEADER, *se tiver heaer no csv
    DELIMITER ',',
    NULL ''
)
"""

arquivo = open('*arquivo*.csv', 'r', encoding='utf-8')
cursor.copy_expert(sql, arquivo)

arquivo.close()

conn.commit()
cursor.close()
conn.close()
