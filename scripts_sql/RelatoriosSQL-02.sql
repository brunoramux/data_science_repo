-- Estudo de Caso 2 - Extraindo Relatórios do Data Warehouse com Linguagem SQL


-- Cria View
CREATE OR REPLACE VIEW dw.vw_faturamento_cliente AS
SELECT c.ClienteID, c.Nome, SUM(v.Faturamento) AS TotalFaturamento
FROM dw.Vendas v
JOIN dw.Cliente c ON v.ClienteID = c.ClienteID
GROUP BY c.ClienteID
HAVING SUM(v.Faturamento) > (
    SELECT AVG(TotalFaturamento) 
    FROM (
        SELECT SUM(v.Faturamento) AS TotalFaturamento
        FROM dw.Vendas v
        GROUP BY v.ClienteID
    ) AS SubQuery
)
ORDER BY TotalFaturamento DESC;


-- Consulta a View
SELECT * FROM dw.vw_faturamento_cliente;


-- Cria View Materializada
CREATE MATERIALIZED VIEW dw.mv_vendas_frete_cliente_categoria AS
SELECT c.PaisCliente, p.NomeCategoria, SUM(v.QuantidadeVendida) AS TotalVendas, SUM(v.CustoFrete) AS TotalCustoFrete
FROM dw.Vendas v
JOIN dw.Cliente c ON v.ClienteID = c.ClienteID
JOIN dw.Produto p ON v.ProdutoID = p.ProdutoID
JOIN dw.Data d ON v.DataID = d.DataID
WHERE d.Ano = 2024
GROUP BY c.PaisCliente, p.NomeCategoria
HAVING SUM(v.CustoFrete) > 30000
ORDER BY c.PaisCliente, p.NomeCategoria;


-- Consulta a MView
SELECT * FROM dw.mv_vendas_frete_cliente_categoria;


-- Atualiza os dados da MView
REFRESH MATERIALIZED VIEW dw.mv_vendas_frete_cliente_categoria;


