-- ============================================================================
-- PROJETO: Análise de Vendas de E-commerce
-- ARQUIVO: 04_auditoria_joins_avancados.sql
-- OBJETIVO: Diagnóstico de integridade, auditoria cadastral e tratamento de nulos
-- ============================================================================

-- 1. Faturamento geral por cliente na base completa com tratamento de nulos
SELECT 
    c.id_cliente,
    c.nome,
    c.estado,
    COUNT(p.id_pedido) AS total_pedidos,
    COALESCE(SUM(p.valor), 0.00) AS faturamento_total
FROM clientes c
LEFT JOIN pedidos p ON c.id_cliente = p.id_cliente
GROUP BY c.id_cliente, c.nome, c.estado
ORDER BY c.id_cliente ASC;


-- 2. Identificação de clientes inativos / leads sem pedidos (Anti-Join)
SELECT 
    c.id_cliente,
    c.nome,
    c.cidade,
    c.estado
FROM clientes c
LEFT JOIN pedidos p ON c.id_cliente = p.id_cliente
WHERE p.id_pedido IS NULL
ORDER BY c.id_cliente ASC;


-- 3. Taxa de ativação regional: Total de cadastros vs Clientes com compras
SELECT 
    c.estado,
    COUNT(DISTINCT c.id_cliente) AS total_cadastrados,
    COUNT(DISTINCT p.id_cliente) AS clientes_compradores
FROM clientes c 
LEFT JOIN pedidos p ON c.id_cliente = p.id_cliente
GROUP BY c.estado
ORDER BY total_cadastrados DESC, c.estado ASC;

-- 4. Auditoria de cancelamentos na base total com filtro na junção e COALESCE
SELECT 
    c.id_cliente,
    c.nome,
    c.estado,
    COUNT(p.id_pedido) AS pedidos_cancelados,
    COALESCE(SUM(p.valor), 0.00) AS total_perdido
FROM clientes c
LEFT JOIN pedidos p ON c.id_cliente = p.id_cliente AND p.status = 'cancelado'
GROUP BY c.id_cliente, c.nome, c.estado
ORDER BY total_perdido DESC, c.id_cliente ASC;