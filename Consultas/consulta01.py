import pandas as pd
import psycopg2

sql = """
    SELECT p.nome AS PAIS, g.valor_emissao as EMISSAO, g.unidade_emissao as UNIDADE
    FROM "GERACAO_ENERGIA" g
    JOIN "AREA" a ON g.id_area = a.id
    JOIN "PAIS" p ON a.id = p.id 
    WHERE g.valor_emissao > 0
    GROUP BY p.nome, g.valor_emissao, g.unidade_emissao
    ORDER BY g.valor_emissao DESC
    
"""
conn = psycopg2.connect(
        dbname="EnergiaTempDB",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )
df = pd.read_sql_query(sql, conn) 
df.to_csv('../Resultado_Consultas/consulta01.csv', index=False)

conn.commit()
conn.close()