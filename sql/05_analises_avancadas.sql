-- =========================================================
-- Projeto: Análise de Vendas de E-commerce
-- Arquivo: 05_analises_avancadas.sql
-- Banco: PostgreSQL
-- Objetivo: Executar análises avançadas utilizando Funções de Janela (Window Functions)
-- =========================================================


-- 1. Top 3 produtos por faturamento dentro de cada categoria
WITH faturamento_produtos AS (
    SELECT
        prod.id_produto,
        prod.categoria,
        prod.nome AS nome_produto,
        SUM(ip.quantidade * ip.preco_unitario) AS faturamento_produto
    FROM produtos prod
    INNER JOIN itens_pedido ip
        ON prod.id_produto = ip.id_produto
    INNER JOIN pedidos ped
        ON ip.id_pedido = ped.id_pedido
    WHERE ped.status = 'pago'
    GROUP BY prod.id_produto, prod.categoria, prod.nome 
),
ranking_produto AS (
    SELECT
        *,
        ROW_NUMBER() OVER(
            PARTITION BY categoria
            ORDER BY faturamento_produto DESC, id_produto ASC
        ) AS ranking
    FROM faturamento_produtos
)
SELECT
    id_produto,
    categoria,
    ranking,
    nome_produto,
    faturamento_produto
FROM ranking_produto
WHERE ranking <= 3
ORDER BY categoria ASC, ranking ASC, nome_produto ASC;


-- 2. Evolução Mensal e Variação MoM (Month over Month) com LAG()
WITH faturamento_mensal AS (
    SELECT
        TO_CHAR(ped.data_pedido, 'YYYY-MM') AS mes,
        SUM(ip.quantidade * ip.preco_unitario) AS faturamento_total
    FROM pedidos ped
    INNER JOIN itens_pedido ip
        ON ped.id_pedido = ip.id_pedido
    WHERE ped.status = 'pago'
    GROUP BY mes
),
comparacao_mensal AS (
    SELECT
        mes,
        faturamento_total,
        LAG(faturamento_total) OVER(ORDER BY mes) AS faturamento_anterior
    FROM faturamento_mensal
)
SELECT
    mes,
    faturamento_total,
    faturamento_anterior,
    ROUND(
    ((faturamento_total - faturamento_anterior)
        / NULLIF(faturamento_anterior, 0) * 100), 2
) AS variacao_percentual_mom
FROM comparacao_mensal
ORDER BY mes ASC;


-- 3. Faturamento Acumulado por Mês (Running Total) com SUM() OVER()
WITH faturamento_mensal AS (
    SELECT
        TO_CHAR(ped.data_pedido, 'YYYY-MM') AS mes,
        SUM(ip.quantidade * ip.preco_unitario) AS faturamento_total
    FROM pedidos ped
    INNER JOIN itens_pedido ip
        ON ped.id_pedido = ip.id_pedido
    WHERE ped.status = 'pago'
    GROUP BY mes
)
SELECT
    mes,
    faturamento_total,
    SUM(faturamento_total) OVER (
        ORDER BY mes
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS faturamento_acumulado
FROM faturamento_mensal
ORDER BY mes ASC;
