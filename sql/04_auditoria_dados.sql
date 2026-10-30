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


-- 4. Pedidos pagos que não possuem nenhum item associado
SELECT
    p.id_pedido,
    p.status,
    p.data_pedido
FROM pedidos p
LEFT JOIN itens_pedido ip
    ON p.id_pedido = ip.id_pedido
WHERE p.status = 'pago'
  AND ip.id_pedido IS NULL
ORDER BY p.id_pedido ASC;
