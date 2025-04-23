import psycopg2

conn = psycopg2.connect(
    dbname="Energia_temp_db",
    user="postgres",
    password="",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()


sql = """
COPY *MES* (atributos, ordem, no, csv)
FROM STDIN WITH (
    FORMAT CSV,
    HEADER, *se tiver heaer no csv
    DELIMITER ',',
    NULL ''
)
COPY *ANO* (atributos, ordem, no, csv)
FROM STDIN WITH (
    FORMAT CSV,
    HEADER, *se tiver heaer no csv
    DELIMITER ',',
    NULL ''
)
COPY *MUD_TEMP* (atributos, ordem, no, csv)
FROM STDIN WITH (
    FORMAT CSV,
    HEADER, *se tiver heaer no csv
    DELIMITER ',',
    NULL ''
)
COPY *GERACAO_ENERGIA* (atributos, ordem, no, csv)
FROM STDIN WITH (
    FORMAT CSV,
    HEADER, *se tiver heaer no csv
    DELIMITER ',',
    NULL ''
)
COPY *TIPO_ENERGIA* (atributos, ordem, no, csv)
FROM STDIN WITH (
    FORMAT CSV,
    HEADER, *se tiver heaer no csv
    DELIMITER ',',
    NULL ''
)
COPY *AREA* (atributos, ordem, no, csv)
FROM STDIN WITH (
    FORMAT CSV,
    HEADER, *se tiver heaer no csv
    DELIMITER ',',
    NULL ''
)
COPY *GRUPO* (atributos, ordem, no, csv)
FROM STDIN WITH (
    FORMAT CSV,
    HEADER, *se tiver heaer no csv
    DELIMITER ',',
    NULL ''
)
COPY *PAIS* (atributos, ordem, no, csv)
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
