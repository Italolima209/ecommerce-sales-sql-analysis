-- =========================================================
-- Projeto: Análise de Vendas de E-commerce
-- Arquivo: 04_auditoria_dados.sql
-- Banco: PostgreSQL
-- Objetivo: Identificar inconsistências de dados e registros órfãos ou inativos (Anti-Join Pattern)
-- =========================================================


-- 1. Clientes cadastrados sem pedidos cadastrados
SELECT
    c.id_cliente,
    c.nome,
    c.email,
    c.estado
FROM clientes c
LEFT JOIN pedidos ped
    ON c.id_cliente = ped.id_cliente
WHERE ped.id_pedido IS NULL
ORDER BY c.nome ASC;


-- 2. Vendedores cadastrados sem pedidos associados
SELECT
    v.id_vendedor,
    v.nome,
    v.email,
    v.regiao
FROM vendedores v
LEFT JOIN pedidos ped
    ON v.id_vendedor = ped.id_vendedor
WHERE ped.id_pedido IS NULL
ORDER BY v.nome ASC;


-- 3. Produtos cadastrados que nunca tiveram vendas pagas
SELECT
    prod.id_produto,
    prod.nome AS nome_produto
FROM produtos prod
WHERE NOT EXISTS (
    SELECT 1
    FROM itens_pedido ip
    INNER JOIN pedidos ped
        ON ip.id_pedido = ped.id_pedido
    WHERE ip.id_produto = prod.id_produto
      AND ped.status = 'pago'
)
ORDER BY prod.id_produto ASC;


-- 4. Pedidos que não possuem nenhum item associado
SELECT
    ped.id_pedido,
    ped.status,
    ped.data_pedido
FROM pedidos ped
LEFT JOIN itens_pedido ip
    ON ped.id_pedido = ip.id_pedido
WHERE ip.id_pedido IS NULL
ORDER BY ped.id_pedido ASC;


-- 5. Pedidos realizados antes do cadastro do cliente
SELECT
    ped.id_pedido,
    c.id_cliente,
    c.nome,
    c.data_cadastro,
    ped.data_pedido
FROM clientes c
INNER JOIN pedidos ped
    ON c.id_cliente = ped.id_cliente
WHERE ped.data_pedido < c.data_cadastro
ORDER BY ped.data_pedido ASC;
