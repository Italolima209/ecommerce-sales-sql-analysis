
-- =========================================================
-- Projeto: Análise de Vendas de E-commerce
-- Arquivo: 06_retencao_coortes_clientes.sql
-- Banco: PostgreSQL
-- Objetivo: Analisar recorrência, ticket médio e retenção
-- de clientes por coortes mensais
-- =========================================================


-- 1. Quantidade de clientes com compra única e recorrente
WITH compras_cliente AS (
    SELECT
        id_cliente,
        COUNT(*) AS total_compras
    FROM pedidos
    WHERE status = 'pago'
    GROUP BY id_cliente
),
classificacao AS (
    SELECT
        CASE
            WHEN total_compras = 1 THEN 'COMPRA UNICA'
            ELSE 'COMPRA RECORRENTE'
        END AS perfil_cliente
    FROM compras_cliente
)
SELECT
    perfil_cliente,
    COUNT(*) AS quantidade_clientes
FROM classificacao
GROUP BY perfil_cliente
ORDER BY quantidade_clientes DESC;


-- 2. Comparação do ticket médio entre clientes únicos e recorrentes
WITH valor_pedidos AS (
    SELECT
        ped.id_pedido,
        ped.id_cliente,
        SUM(ip.quantidade * ip.preco_unitario) AS valor_pedido
    FROM pedidos ped
    INNER JOIN itens_pedido ip
        ON ped.id_pedido = ip.id_pedido
    WHERE ped.status = 'pago'
    GROUP BY ped.id_pedido, ped.id_cliente
),
classificacao AS (
    SELECT
        id_cliente,
        CASE
            WHEN COUNT(*) = 1 THEN 'COMPRA UNICA'
            ELSE 'COMPRA RECORRENTE'
        END AS perfil_cliente
    FROM valor_pedidos
    GROUP BY id_cliente
)
SELECT
    c.perfil_cliente,
    COUNT(DISTINCT vp.id_cliente) AS quantidade_clientes,
    COUNT(*) AS quantidade_pedidos,
    ROUND(AVG(vp.valor_pedido), 2) AS ticket_medio
FROM valor_pedidos vp
INNER JOIN classificacao c
    ON vp.id_cliente = c.id_cliente
GROUP BY c.perfil_cliente
ORDER BY ticket_medio DESC;


-- 3. Quantidade de novos clientes por coorte mensal
WITH primeira_compra AS (
    SELECT
        id_cliente,
        MIN(data_pedido) AS data_primeira_compra
    FROM pedidos
    WHERE status = 'pago'
    GROUP BY id_cliente
)
SELECT
    TO_CHAR(DATE_TRUNC('month', data_primeira_compra), 'YYYY-MM') AS coorte,
    COUNT(*) AS novos_clientes
FROM primeira_compra
GROUP BY DATE_TRUNC('month', data_primeira_compra)
ORDER BY coorte ASC;


-- 4. Taxa de retenção mensal por coorte de clientes
WITH primeira_compra AS (
    SELECT
        id_cliente,
        DATE_TRUNC('month', MIN(data_pedido))::date AS coorte
    FROM pedidos
    WHERE status = 'pago'
    GROUP BY id_cliente
),
atividade_mensal AS (
    SELECT DISTINCT
        id_cliente,
        DATE_TRUNC('month', data_pedido)::date AS mes_compra
    FROM pedidos
    WHERE status = 'pago'
),
retencao AS (
    SELECT
        pc.coorte,
        (
            (EXTRACT(YEAR FROM am.mes_compra) - EXTRACT(YEAR FROM pc.coorte)) * 12
            + EXTRACT(MONTH FROM am.mes_compra) - EXTRACT(MONTH FROM pc.coorte)
        )::int AS mes_desde_primeira_compra,
        COUNT(*) AS clientes_ativos
    FROM primeira_compra pc
    INNER JOIN atividade_mensal am
        ON pc.id_cliente = am.id_cliente
    GROUP BY pc.coorte, mes_desde_primeira_compra
)
SELECT
    TO_CHAR(r.coorte, 'YYYY-MM') AS coorte,
    r.mes_desde_primeira_compra,
    r.clientes_ativos,
    base.clientes_ativos AS clientes_iniciais,
    ROUND(
        r.clientes_ativos * 100.0
        / NULLIF(base.clientes_ativos, 0), 2
    ) AS taxa_retencao
FROM retencao r
INNER JOIN retencao base
    ON r.coorte = base.coorte
   AND base.mes_desde_primeira_compra = 0
ORDER BY r.coorte ASC, r.mes_desde_primeira_compra ASC;
