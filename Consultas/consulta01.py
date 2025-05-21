import pandas as pd
import psycopg2

sql = '''
    WITH
    renovs AS (
        SELECT 	GE.id_area,
                GE.id_ano,
                ROUND(SUM(GE.valor_geracao)::numeric, 2) AS total_ren
        FROM "GERACAO_ENERGIA" AS GE
        WHERE GE.id_tipo IN (
            SELECT tipo.id FROM "TIPO_ENERGIA" as tipo
            WHERE tipo.renovavel = TRUE
        )
        GROUP BY GE.id_area, GE.id_ano
    ),
    tudo AS (
        SELECT 	GE.id_area,
                GE.id_ano,
                ROUND(SUM(GE.valor_geracao)::numeric, 2) AS total_tudo
        FROM "GERACAO_ENERGIA" AS GE
        GROUP BY GE.id_area, GE.id_ano
    )
    SELECT 	t.id_ano AS ano,
            a.nome AS area,
            t.total_tudo,
            r.total_ren,
            ROUND(100*r.total_ren/t.total_tudo, 2) AS PERCENTAGE
            
    FROM tudo AS t
    JOIN renovs r ON t.id_area = r.id_area AND t.id_ano = r.id_ano
    JOIN "AREA" a ON t.id_area = a.id
    WHERE t.total_tudo != 0
    ORDER BY PERCENTAGE DESC, area, ano
'''

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