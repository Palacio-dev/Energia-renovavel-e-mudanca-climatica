import pandas as pd
from psycopg2._psycopg import connection
from main import conectar

sql = {
    '''
    SELECT p.nome, AVG(e.valor) AS media_emissao
    FROM EMISSAO e
    JOIN PAIS p ON e.pais_id = p.id
    JOIN ANO a ON e.ano_id = a.id
    WHERE a.id > 2000
    GROUP BY p.nome
    ORDER BY media_emissao DESC
    LIMIT 10;
'''
}
conn = conectar()
df = pd.read_sql_query(sql, conn) 

conn = conectar()
df = pd.read_sql_query(sql, conn) 
df.to_csv('../Resultado_Consultas/consulta04.csv', index=False)

conn.commit()
conn.close()