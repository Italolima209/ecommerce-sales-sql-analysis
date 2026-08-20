# 📊 Análise de Vendas de E-commerce e Modelagem Relacional (PostgreSQL)

Projeto prático desenvolvido para demonstrar modelagem relacional, integridade referencial e consultas analíticas avançadas em SQL.

## 🎯 Objetivo
Analisar dados transacionais de um e-commerce estruturado em modelo relacional (Chave Primária e Chave Estrangeira) para responder perguntas de negócio sobre:
- Faturamento e frequência de compra por cliente (LTV).
- Desempenho de vendas e ticket médio por região geográfica.
- Categorias de maior impacto financeiro e volume de vendas.
- Monitoramento de perdas por pedidos cancelados por estado.

## 🛠️ Tecnologias Utilizadas
- **PostgreSQL (pgAdmin 4 / VS Code)**
- **SQL (DQL, DDL, DML)**: `INNER JOIN`, `GROUP BY`, `HAVING`, `SUM`, `COUNT`, `AVG`, `ROUND`.

## 🗄️ Estrutura do Banco de Dados
- **`clientes`**: Tabela dimensão contendo dados cadastrais e geográficos (`id_cliente` [PK], `nome`, `cidade`, `estado`).
- **`pedidos`**: Tabela fato contendo transações financeiras (`id_pedido` [PK], `id_cliente` [FK], `categoria`, `valor`, `status`, `data_pedido`).

## 📈 Principais Descobertas (Insights)
1. **Concentração de Receita:** Clientes dos estados do Sul e Sudeste concentraram o maior faturamento total e ticket médio por compra.
2. **Desempenho por Categoria:** A categoria 'Eletrônicos' manteve liderança em faturamento, mesmo com volume equilibrado em relação a 'Roupas' e 'Livros'.
3. **Eficiência Operacional:** O volume de cancelamentos permaneceu concentrado em categorias de maior valor unitário, indicando oportunidade de melhoria nos meios de pagamento.

## 🚀 Como Executar
1. Execute o script `01_schema_e_dados.sql` para criar as tabelas relacionais e popular os 20 registros.
2. Execute `02_consultas_analiticas.sql` para verificar as consultas básicas de agregação.
3. Execute `03_analises_relacionais_join.sql` para extrair os relatórios com junção de tabelas.