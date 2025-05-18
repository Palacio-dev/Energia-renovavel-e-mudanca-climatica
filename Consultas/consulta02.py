import pandas as pd
from psycopg2._psycopg import connection
from main import conectar

sql = {
    '''
    SELECT p.nome AS pais, SUM(e.valor) AS total_emissao
    FROM EMISSAO e
    JOIN PAIS p ON e.pais_id = p.id
    JOIN CATEGORIA c ON e.categoria_id = c.id
    WHERE c.nome IN ('Energy', 'Power sector emissions')
    GROUP BY p.nome
    ORDER BY total_emissao DESC
    LIMIT 10;
'''
}
conn = conectar()
df = pd.read_sql_query(sql, conn) 

conn = conectar()
df = pd.read_sql_query(sql, conn) 
df.to_csv('../Resultado_Consultas/consulta02.csv', index=False)

conn.commit()
conn.close()
