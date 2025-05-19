import pandas as pd
import psycopg2

sql = '''
    SELECT p.nome AS PAIS, SUM(g.mud_value) AS soma_mudanca
    FROM "MUD_TEMP" g
    JOIN "AREA" a ON g.id_area = a.id
    JOIN "PAIS" p ON a.id = p.id
    GROUP BY p.nome
    ORDER BY soma_mudanca DESC;

'''
# SELECT p.nome AS PAIS, SUM(g.mud_value) AS soma_mudanca
#     FROM "MUD_TEMP" g
#     JOIN "AREA" a ON g.id_area = a.id
#     JOIN "PAIS" p ON a.id = p.id
#     GROUP BY p.nome
#     ORDER BY soma_mudanca DESC;


conn = psycopg2.connect(
        dbname="EnergiaTempDB",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )
df = pd.read_sql_query(sql, conn) 

df = pd.read_sql_query(sql, conn) 
df.to_csv('../Resultado_Consultas/consulta02.csv', index=False)

conn.commit()
conn.close()
