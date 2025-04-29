import pandas as pd
import psycopg2


conn = psycopg2.connect(
    dbname="EnergiaTempDB",
    user="postgres",
    password="",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()


''' Os datasets contém dados de anos entre 1960 e 2024 '''
for ano in range(1960, 2025):
    for m in range(1, 13):
        cursor.execute(f'INSERT INTO "MES" (id, numero, id_ano) VALUES (\'{m}/{ano}\', {m}, {ano})')

conn.commit()
cursor.close()
conn.close()
