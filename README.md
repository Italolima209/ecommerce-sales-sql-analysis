# 📊 Análise de Vendas de E-commerce com SQL (PostgreSQL)

Projeto prático desenvolvido para demonstrar consultas analíticas, filtros de negócio e agregações em SQL.

## 🎯 Objetivo
Analisar os dados de transações de um e-commerce para entender:
- Faturamento consolidado por categoria de produtos.
- Impacto financeiro de pedidos cancelados.
- Identificação de clientes VIPs com alto volume de compras.

## 🛠️ Tecnologias Utilizadas
- **PostgreSQL**
- **DBeaver / pgAdmin4 / VS Code**

## 📈 Principais Descobertas (Insights)
1. **Eletrônicos é o carro-chefe:** Representa a maior parte do faturamento da loja e possui o maior ticket médio.
2. **Impacto dos Cancelamentos:** Pedidos cancelados representaram perda de receita considerável no período analisado.
3. **Clientes Principais:** Clientes como Ana Silva e Diego Rocha concentraram os maiores volumes de compra no período.

## 🚀 Como Executar
1. Execute o script `01_schema_e_dados.sql` para criar a tabela e popular os dados.
2. Execute as consultas do arquivo `02_consultas_analiticas.sql` para gerar os relatórios.
