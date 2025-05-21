import pandas as pd
import psycopg2

sql = '''
    SELECT 
	p.nome AS pais,
	te.valor AS tipo_energia, 
	SUM(ge.valor_geracao) AS total_gerado,
	ge.unidade_geracao as unidade
	FROM "GERACAO_ENERGIA" ge
    JOIN "TIPO_ENERGIA" te ON ge.id_tipo = te.id
    JOIN "AREA" a ON ge.id_area = a.id
    JOIN "PAIS" p ON a.id = p.id
    WHERE te.renovavel = FALSE
    GROUP BY p.nome, te.valor, ge.unidade_geracao
    ORDER BY total_gerado DESC;
'''

conn = psycopg2.connect(
        dbname="EnergiaTempDB",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )

df = pd.read_sql_query(sql, conn) 
df.to_csv('../Resultado_Consultas/consulta02.csv', index=False)
conn.commit()
conn.close()
