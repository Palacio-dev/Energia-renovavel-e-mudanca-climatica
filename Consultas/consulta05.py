import pandas as pd
from psycopg2._psycopg import connection
from main import conectar

sql = {
    '''
    WITH media_global AS (
        SELECT AVG(valor) AS media
        FROM EMISSAO
        WHERE ano_id = 2020
    )
    SELECT p.nome, e.valor
    FROM EMISSAO e
    JOIN PAIS p ON e.pais_id = p.id
    JOIN PAIS_GRUPO pg ON p.id = pg.pais_id
    JOIN GRUPO g ON pg.grupo_id = g.id
    JOIN media_global mg ON TRUE
    WHERE g.nome = 'G20' AND e.ano_id = 2020 AND e.valor > mg.media
    ORDER BY e.valor DESC;
'''
}
conn = conectar()
df = pd.read_sql_query(sql, conn) 

conn = conectar()
df = pd.read_sql_query(sql, conn) 
df.to_csv('../Resultado_Consultas/consulta05.csv', index=False)

conn.commit()
conn.close()