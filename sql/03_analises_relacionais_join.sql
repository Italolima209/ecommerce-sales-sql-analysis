-- =========================================================
-- Projeto: Análise de Vendas de E-commerce
-- Arquivo: 03_analises_relacionais_join.sql
-- Banco: PostgreSQL
-- Objetivo: Analisar o desempenho e comportamento por dimensões (Clientes, Vendedores e Região)
-- =========================================================


-- 1. Top 10 clientes por faturamento e quantidade de pedidos pagos
SELECT
    c.id_cliente,
    c.nome,
    SUM(ip.quantidade * ip.preco_unitario) AS faturamento,
    COUNT(DISTINCT ped.id_pedido) AS pedidos_pagos
FROM clientes c
INNER JOIN pedidos ped
    ON c.id_cliente = ped.id_cliente
INNER JOIN itens_pedido ip
    ON ped.id_pedido = ip.id_pedido
WHERE ped.status = 'pago'
GROUP BY c.id_cliente, c.nome
ORDER BY faturamento DESC, c.nome ASC
LIMIT 10;


-- 2. Desempenho dos vendedores por faturamento e quantidade de pedidos
SELECT
    v.id_vendedor,
    v.nome,
    SUM(ip.quantidade * ip.preco_unitario) AS faturamento_vendedor,
    COUNT(DISTINCT ped.id_pedido) AS pedidos_vendedor
FROM vendedores v
INNER JOIN pedidos ped
    ON v.id_vendedor = ped.id_vendedor
INNER JOIN itens_pedido ip
    ON ped.id_pedido = ip.id_pedido
WHERE ped.status = 'pago'
GROUP BY v.id_vendedor, v.nome
ORDER BY faturamento_vendedor DESC, v.nome ASC;


-- 3. Distribuição geográfica (faturamento e volume de pedidos por estado/UF do cliente)
SELECT
    c.estado,
    SUM(ip.quantidade * ip.preco_unitario) AS faturamento_estado,
    COUNT(DISTINCT ped.id_pedido) AS total_pedidos_estado
FROM clientes c
INNER JOIN pedidos ped
    ON c.id_cliente = ped.id_cliente
INNER JOIN itens_pedido ip
    ON ped.id_pedido = ip.id_pedido
WHERE ped.status = 'pago'
GROUP BY c.estado
ORDER BY faturamento_estado DESC, c.estado ASC;
