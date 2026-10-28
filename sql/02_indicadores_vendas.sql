-- =========================================================
-- Projeto: Análise de Vendas de E-commerce
-- Arquivo: 02_indicadores_vendas.sql
-- Banco: PostgreSQL
-- Objetivo: Analisar os principais indicadores de vendas
-- =========================================================


-- 1. Faturamento total dos pedidos pagos
SELECT
    SUM(ip.quantidade * ip.preco_unitario) AS faturamento_total
FROM itens_pedido ip
INNER JOIN pedidos pd
    ON ip.id_pedido = pd.id_pedido
WHERE pd.status = 'pago';


-- 2. Quantidade de pedidos por status
SELECT
    status,
    COUNT(*) AS quantidade_pedidos
FROM pedidos
GROUP BY status
ORDER BY quantidade_pedidos DESC;


-- 3. Quantidade de clientes com pedidos pagos
SELECT
    COUNT(DISTINCT id_cliente) AS clientes_com_pedidos_pagos
FROM pedidos
WHERE status = 'pago';


-- 4. Faturamento por categoria e participação percentual
WITH receita_global AS (
    SELECT
        SUM(ip.quantidade * ip.preco_unitario) AS faturamento_total
    FROM itens_pedido ip
    INNER JOIN pedidos pd
        ON ip.id_pedido = pd.id_pedido
    WHERE pd.status = 'pago'
),
    faturamento_categorias AS (
    SELECT
        prod.categoria,
        SUM(ip.quantidade * ip.preco_unitario) AS faturamento_categoria
    FROM itens_pedido ip
    INNER JOIN pedidos pd 
        ON ip.id_pedido = pd.id_pedido
    INNER JOIN produtos prod
        ON ip.id_produto = prod.id_produto 
    WHERE pd.status = 'pago'
    GROUP BY prod.categoria
)
SELECT 
    f.categoria,
    f.faturamento_categoria,
    ROUND((f.faturamento_categoria / r.faturamento_total) * 100, 2) AS percentual_participacao
FROM faturamento_categorias f
CROSS JOIN receita_global r;


-- 5. Ticket médio por pedido pago
SELECT
    ROUND(AVG(pedidos_pagos.valor_pedido), 2) AS ticket_medio
FROM (
    SELECT
        pd.id_pedido,
        SUM(ip.quantidade * ip.preco_unitario) AS valor_pedido
    FROM pedidos pd
    INNER JOIN itens_pedido ip
        ON pd.id_pedido = ip.id_pedido
    WHERE pd.status = 'pago'
    GROUP BY pd.id_pedido
) AS pedidos_pagos;
