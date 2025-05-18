import pandas as pd
from main import conectar

sql = {
    '''
    SELECT g.nome AS grupo, SUM(e.valor) AS emissao_total
    FROM EMISSAO e
    JOIN PAIS_GRUPO pg ON e.pais_id = pg.pais_id
    JOIN GRUPO g ON pg.grupo_id = g.id
    WHERE e.ano_id = 2019
    GROUP BY g.nome
    ORDER BY emissao_total DESC;
'''
}
conn = conectar()
df = pd.read_sql_query(sql, conn) 
df.to_csv('../Resultado_Consultas/consulta01.csv', index=False)

conn.commit()
conn.close()