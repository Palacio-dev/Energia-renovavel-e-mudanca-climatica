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
        )
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
    GROUP BY
        GE.id_area,
        GE.id_ano,
		GE.unidade_geracao,
		GE.unidade_emissao
),
-- temp_ano reúne o aumento de temperatura total de cada país em cada ano
temp_ano AS (
	SELECT
        MT.id_area,
        MT.id_ano,
        ROUND((SUM(MT.mud_value)/1000) :: numeric, 4) AS valor
	FROM
		"MUD_TEMP" AS MT
    GROUP BY
        MT.id_ano,
		MT.id_area
)

-- tabela final
SELECT
    a.nome AS area,
    t.id_ano AS ano,
    t.total_tudo,
    r.total_ren,
	t.unidade_geracao,
    ROUND(100 * r.total_ren / t.total_tudo, 2) AS PERCENTAGE,
	t.emissao,
	t.unidade_emissao,
    ta.valor AS aumento_temp
FROM
    tudo AS t
    -- join da soma total e de só renováveis pra cada país/ano
    JOIN renovs r ON t.id_area = r.id_area
        AND t.id_ano = r.id_ano
    JOIN temp_ano ta ON t.id_area = ta.id_area
        AND t.id_ano = ta.id_ano
    -- join para os nomes de cada área
    JOIN "AREA" a ON t.id_area = a.id
WHERE
    t.total_tudo != 0
ORDER BY
    PERCENTAGE DESC,
    area,
    ano DESC