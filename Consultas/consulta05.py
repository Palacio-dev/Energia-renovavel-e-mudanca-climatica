import pandas as pd
import psycopg2

sql = '''
    SELECT p.nome AS pais, ROUND(SUM(mt.mud_value/1000.0)::numeric, 3) AS aumento_total_°C FROM "MUD_TEMP" mt
    JOIN "AREA" a ON mt.id_area = a.id
    JOIN "PAIS" p ON a.id = p.id
    GROUP BY p.nome
    ORDER BY aumento_total_°C DESC;
'''

conn = psycopg2.connect(
        dbname="EnergiaTempDB",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )

df = pd.read_sql_query(sql, conn) 
df.to_csv('../Resultado_Consultas/consulta05.csv', index=False)
conn.commit()
conn.close()