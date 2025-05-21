import pandas as pd
import psycopg2

sql = '''
    SELECT
    p.nome                   AS pais,
    an.id                    AS ano,
    ge.unidade_geracao       AS unidade,
    ROUND(SUM(ge.valor_geracao)::numeric, 3) AS total_gerado
    FROM "GERACAO_ENERGIA" ge
    JOIN "AREA"     a   ON ge.id_area = a.id
    JOIN "PAIS"     p   ON a.id  = p.id
    JOIN "ANO"      an  ON ge.id_ano  = an.id
    WHERE an.id BETWEEN 2000 AND 2024
    GROUP BY p.nome, an.id, ge.unidade_geracao
    ORDER BY p.nome, an.id;
'''

conn = psycopg2.connect(
        dbname="EnergiaTempDB",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )

df = pd.read_sql_query(sql, conn) 
df.to_csv('../Resultado_Consultas/consulta04.csv', index=False)
conn.commit()
conn.close()