import pandas as pd
from psycopg2._psycopg import connection
from main import conectar

sql = {
    '''
    SELECT a.id/10*10 AS decada, SUM(e.valor) AS total
    FROM EMISSAO e
    JOIN ANO a ON e.ano_id = a.id
    JOIN PAIS p ON e.pais_id = p.id
    WHERE p.nome = 'China'
    GROUP BY decada
    ORDER BY decada;
'''
}
conn = conectar()
df = pd.read_sql_query(sql, conn) 

conn = conectar()
df = pd.read_sql_query(sql, conn) 
df.to_csv('../Resultado_Consultas/consulta03.csv', index=False)

conn.commit()
conn.close()