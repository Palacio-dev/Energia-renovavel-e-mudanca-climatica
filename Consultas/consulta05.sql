-- CONSULTA 05
SELECT
    p.nome AS pais,
    ROUND(SUM(mt.mud_value / 1000.0) :: numeric, 3) AS aumento_total_°C
FROM
    "MUD_TEMP" mt
    JOIN "PAIS" p ON mt.id_area = p.id
GROUP BY
    p.nome
ORDER BY
    aumento_total_°C DESC;