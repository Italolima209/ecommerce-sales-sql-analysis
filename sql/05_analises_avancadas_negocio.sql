-- ============================================================================
-- PROJETO: Análise de Vendas de E-commerce
-- ARQUIVO: 05_analises_avancadas_negocio.sql
-- OBJETIVO: Segmentação condicional (CASE WHEN), CTEs e Window Functions
-- ============================================================================


-- 1. Segmentação de clientes por faixa de faturamento acumulado (CASE WHEN)
SELECT
    c.id_cliente,
    c.nome,
    c.estado,
    SUM(p.valor) AS faturamento_total,
    CASE
        WHEN SUM(p.valor) >= 1500 THEN 'VIP'
        WHEN SUM(p.valor) BETWEEN 500 AND 1499.99 THEN 'Recorrente'
        ELSE 'Inicial'
    END AS categoria_cliente
FROM clientes c 
INNER JOIN pedidos p ON c.id_cliente = p.id_cliente
WHERE p.status = 'pago'
GROUP BY c.id_cliente, c.nome, c.estado
ORDER BY faturamento_total DESC, c.id_cliente ASC;


-- 2. Auditoria de Conversão por Categoria (CASE WHEN dentro de agregações)
SELECT
    categoria,
    SUM(CASE WHEN status = 'pago' THEN 1 ELSE 0 END) AS total_pagos,
    SUM(CASE WHEN status = 'cancelado' THEN 1 ELSE 0 END) AS total_cancelados,
    COUNT(id_pedido) AS total_pedidos
FROM pedidos
GROUP BY categoria
ORDER BY total_pedidos DESC;


-- 3. Clientes com faturamento acima da média geral (CTE + Subquery Escalar)
WITH faturamento_por_cliente AS 
(
    SELECT 
        c.id_cliente,
        c.nome,
        c.estado,
        SUM(p.valor) AS total_gasto
    FROM clientes c
    INNER JOIN pedidos p ON c.id_cliente = p.id_cliente
    WHERE p.status = 'pago'
    GROUP BY c.id_cliente, c.nome, c.estado
)
SELECT 
    id_cliente,
    nome,
    estado,
    total_gasto
FROM faturamento_por_cliente
WHERE total_gasto > (SELECT AVG(total_gasto) FROM faturamento_por_cliente)
ORDER BY total_gasto DESC;


-- 4. Participação percentual de cada categoria no faturamento total (Múltiplas CTEs)
WITH faturamento_categorias AS 
(
    SELECT 
        p.categoria,
        SUM(p.valor) AS faturamento_categoria
    FROM pedidos p 
    WHERE p.status = 'pago'
    GROUP BY p.categoria
),
receita_global AS 
(
    SELECT 
        SUM(valor) AS faturamento_total_empresa
    FROM pedidos
    WHERE status = 'pago'
)
SELECT 
    f.categoria,
    f.faturamento_categoria,
    ROUND((f.faturamento_categoria / r.faturamento_total_empresa) * 100, 2) AS perc_participacao
FROM faturamento_categorias f
CROSS JOIN receita_global r
ORDER BY f.faturamento_categoria DESC;


-- 5. Maior transação individual por cliente (Window Function: ROW_NUMBER)
WITH ranking_pedidos_cliente AS (
    SELECT 
        p.id_pedido,
        p.id_cliente,
        c.nome,
        p.categoria,
        p.valor,
        p.data_pedido,
        ROW_NUMBER() OVER (
            PARTITION BY p.id_cliente 
            ORDER BY p.valor DESC, p.data_pedido DESC
        ) AS posicao_compra
    FROM pedidos p
    INNER JOIN clientes c ON p.id_cliente = c.id_cliente
    WHERE p.status = 'pago'
)
SELECT 
    id_pedido,
    id_cliente,
    nome,
    categoria,
    valor AS maior_compra,
    data_pedido
FROM ranking_pedidos_cliente
WHERE posicao_compra = 1
ORDER BY maior_compra DESC, id_cliente ASC;


-- 6. Ranking analítico de clientes por volume financeiro (Window Function: DENSE_RANK)
WITH faturamento_consolidado AS (
    SELECT 
        c.id_cliente,
        c.nome,
        c.estado,
        SUM(p.valor) AS total_gasto
    FROM clientes c
    INNER JOIN pedidos p ON c.id_cliente = p.id_cliente
    WHERE p.status = 'pago'
    GROUP BY c.id_cliente, c.nome, c.estado
)
SELECT 
    id_cliente,
    nome,
    estado,
    total_gasto,
    DENSE_RANK() OVER (ORDER BY total_gasto DESC) AS posicao_ranking
FROM faturamento_consolidado
ORDER BY posicao_ranking ASC, id_cliente ASC;
