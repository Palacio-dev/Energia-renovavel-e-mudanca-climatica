import pandas as pd
import psycopg2


sql = '''
    SELECT p.nome AS PAIS, AVG(g.mud_value) AS avg_valor_temp, te.valor as NOME, te.renovavel as RENOVAVEL
    FROM "MUD_TEMP" g
    JOIN "AREA" a ON g.id_area = a.id
    JOIN "PAIS" p ON a.id = p.id
    JOIN "GERACAO_ENERGIA" ge ON a.id = ge.id_area
    JOIN "TIPO_ENERGIA" te ON ge.id_tipo = te.id
    WHERE te.renovavel = 'true'
    GROUP BY p.nome, g.mud_value, te.valor, te.renovavel
'''

conn = psycopg2.connect(
        dbname="EnergiaTempDB",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )

df = pd.read_sql_query(sql, conn) 

df = pd.read_sql_query(sql, conn) 
df.to_csv('../Resultado_Consultas/consulta03.csv', index=False)

conn.commit()
conn.close()