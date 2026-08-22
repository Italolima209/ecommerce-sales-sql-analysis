-- 1. Faturamento Total (Apenas Pedidos Pagos)
SELECT SUM(valor) AS faturamento_total
FROM pedidos
WHERE status = 'pago';


-- Análise de categorias secundárias (Livros e Roupas)
SELECT categoria, COUNT(*) AS total_pedidos,
    SUM(valor) AS total_faturamento
FROM pedidos
WHERE status = 'pago' and categoria <> 'Eletrônicos'
GROUP BY categoria;


-- 3. Impacto financeiro de pedidos pagos vs cancelados
SELECT status, COUNT(valor) AS total_pedidos,
    SUM(valor) AS total_acumulado
FROM pedidos
GROUP BY status;


-- 4. Clientes VIPs (Gasto total acima de R$ 1.000 em pedidos pagos)
SELECT id_cliente,
    SUM(valor) AS valor_gasto
FROM pedidos
WHERE status = 'pago'
GROUP BY id_cliente
HAVING SUM(valor) > 1000
ORDER BY valor_gasto DESC;


