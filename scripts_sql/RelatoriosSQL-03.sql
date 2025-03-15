-- Estudo de Caso 2 - Extraindo Relatórios do Data Warehouse com Linguagem SQL


-- Otimizar a query abaixo
SELECT c.PaisCliente, p.NomeCategoria, SUM(v.QuantidadeVendida) AS TotalVendas, SUM(v.CustoFrete) AS TotalCustoFrete
FROM dw.Vendas v
JOIN dw.Cliente c ON v.ClienteID = c.ClienteID
JOIN dw.Produto p ON v.ProdutoID = p.ProdutoID
JOIN dw.Data d ON v.DataID = d.DataID
WHERE d.Ano = 2024
GROUP BY c.PaisCliente, p.NomeCategoria
HAVING SUM(v.CustoFrete) > 30000
ORDER BY c.PaisCliente, p.NomeCategoria;


-- Para otimizar a performance de uma query, é recomendável considerar a criação de índices em colunas que são frequentemente usadas em condições de filtro (WHERE), 
-- junções (JOIN), agrupamentos (GROUP BY) e ordenação (ORDER BY). A criação de índices pode acelerar significativamente a execução de consultas ao reduzir 
-- o tempo necessário para buscar e filtrar dados nas tabelas. Aqui estão as sugestões de índices:


-- Índice na tabela dw.Data para a coluna Ano:

-- Dado que a consulta filtra por d.Ano = 2024, um índice na coluna Ano da tabela Data pode ajudar a filtrar rapidamente as linhas relevantes para o ano especificado.

CREATE INDEX idx_data_ano ON dw.Data(Ano);


-- Índices nas chaves estrangeiras utilizadas para as junções:

-- A consulta realiza junções usando as chaves estrangeiras ClienteID, ProdutoID, e DataID nas tabelas Vendas, Cliente, Produto, e Data. 
-- Índices nessas colunas podem acelerar o processo de junção.

CREATE INDEX idx_vendas_clienteid ON dw.Vendas(ClienteID);
CREATE INDEX idx_vendas_produtoid ON dw.Vendas(ProdutoID);
CREATE INDEX idx_vendas_dataid ON dw.Vendas(DataID);

-- Podemos ainda criar índices compostos
CREATE INDEX idx_cliente_paiscliente ON dw.Cliente(PaisCliente, ClienteID);

-- Drop do índice
DROP INDEX dw.idx_cliente_paiscliente;
