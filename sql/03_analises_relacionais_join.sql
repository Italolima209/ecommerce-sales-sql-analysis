-- ============================================================================
-- PROJETO: Análise de Vendas de E-commerce
-- ARQUIVO: 03_analises_relacionais_join.sql
-- OBJETIVO: Consultas analíticas relacionais utilizando INNER JOIN, Agregações e HAVING
-- ============================================================================

-- 1. Faturamento total e volume de compras por cliente (apenas pedidos pagos)
SELECT
    c.nome,
    c.cidade,
    COUNT(p.id_pedido) AS pedidos_pagos,
    SUM(p.valor) AS faturamento_total
FROM pedidos p
JOIN clientes c ON p.id_cliente = c.id_cliente
WHERE p.status = 'pago'
GROUP BY c.id_cliente, c.nome, c.cidade
ORDER BY faturamento_total DESC;


-- 2. Análise de desempenho regional: Volume, Faturamento e Ticket Médio por Estado
SELECT 
    c.estado,
    COUNT(p.id_pedido) AS pedidos_pagos,
    SUM(p.valor) AS faturamento_total,
    ROUND(AVG(p.valor), 2) AS ticket_medio
FROM pedidos p
INNER JOIN clientes c ON p.id_cliente = c.id_cliente
WHERE p.status = 'pago'
GROUP BY c.estado
ORDER BY faturamento_total DESC;


-- 3. Categorias de alta demanda com filtro de faturamento mínimo (HAVING)
SELECT 
    categoria,
    COUNT(id_pedido) AS pedidos_pagos,
    SUM(valor) AS faturamento_total
FROM pedidos
WHERE status = 'pago'
GROUP BY categoria
HAVING COUNT(id_pedido) >= 3 AND SUM(valor) > 400
ORDER BY faturamento_total DESC;


-- 4. Monitoramento de perdas: Análise de pedidos pagos vs cancelados por Estado
SELECT
    c.estado,
    p.status,
    COUNT(p.id_pedido) AS total_pedidos,
    SUM(p.valor) AS valor_total
FROM pedidos p
INNER JOIN clientes c ON p.id_cliente = c.id_cliente
GROUP BY c.estado, p.status
ORDER BY c.estado ASC, p.status DESC;

