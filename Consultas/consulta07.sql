-- CONSULTA 01
-- Essa consulta reúne em uma tabela os dados de geração de energia total e renovável (valor bruto e em porcentagem),
-- emissão de CO2 e aumento de temperatura de cada país por ano

WITH
-- renovs é uma abstração com as somas de gerações de energia renovável para cada país/ano
renovs AS (
    SELECT
        GE.id_area,
        GE.id_ano,
        ROUND(SUM(GE.valor_geracao) :: numeric, 2) AS total_ren
    FROM
        "GERACAO_ENERGIA" AS GE
    WHERE
        GE.id_tipo IN (
            SELECT
                tipo.id
            FROM
                "TIPO_ENERGIA" as tipo
            WHERE
                tipo.renovavel = TRUE
        ) AND GE.id_ano = 2023
    GROUP BY
        GE.id_area,
        GE.id_ano
),
-- renovs é uma abstração com as somas de gerações de energia totais para cada país/ano
tudo AS (
    SELECT
        GE.id_area,
        GE.id_ano,
        ROUND(SUM(GE.valor_geracao) :: numeric, 2) AS total_tudo,
		GE.unidade_geracao,
		ROUND(sum(GE.valor_emissao) :: numeric, 2) AS emissao,
		GE.unidade_emissao
    FROM
        "GERACAO_ENERGIA" AS GE
	WHERE GE.id_ano = 2023
    GROUP BY
        GE.id_area,
        GE.id_ano,
		GE.unidade_geracao,
		GE.unidade_emissao
),

-- tabela de países que tem mais de 50% de geração de energia renovável
p_tops as (SELECT
    t.id_area AS pais_top_2023
	
FROM
    tudo AS t
    -- join da soma total e de só renováveis pra cada país/ano
    JOIN renovs r ON t.id_area = r.id_area
WHERE
    t.total_tudo != 0 AND ROUND(100 * r.total_ren / t.total_tudo, 2) > 50
	AND t.id_area IN (SELECT "id" FROM "PAIS")
ORDER BY
    pais_top_2023
)

SELECT * FROM p_tops
	







		
