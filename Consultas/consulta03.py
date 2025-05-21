import pandas as pd
import psycopg2

sql = '''
    SELECT 
    p.nome                  AS pais,
    te.valor                AS tipo_de_emissao,
    te.renovavel            AS eh_renovavel,
    ge.unidade_emissao      AS unidade,
    ROUND(SUM(ge.valor_emissao)::numeric, 3) AS total_emissao,
	ge.id_ano 				AS ano
    FROM "GERACAO_ENERGIA" ge
    JOIN "TIPO_ENERGIA"   te ON ge.id_tipo    = te.id
    JOIN "AREA"           a  ON ge.id_area    = a.id
    JOIN "PAIS"           p  ON a.id     = p.id
    WHERE ge.valor_emissao > 0
    GROUP BY p.nome, te.valor, te.renovavel, ge.unidade_emissao, ge.id_ano
    ORDER BY total_emissao DESC;
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