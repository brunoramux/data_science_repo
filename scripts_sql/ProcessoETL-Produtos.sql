-- Estudo de Caso 1 - Construindo e Implementando Modelo de Dados Para Portal de E-commerce
-- Processo ETL da Tabela de Produtos


-- Cria a Function
CREATE OR REPLACE FUNCTION dw.etl_produtos(num_produtos INTEGER)
RETURNS VOID AS $$
DECLARE
    i INTEGER := 1;
    nome_produto VARCHAR;
    descricao_produto VARCHAR;
    preco_produto DECIMAL;
    categoria_produto VARCHAR;
BEGIN
    WHILE i <= num_produtos LOOP
        nome_produto := 'Produto ' || i::TEXT;
        descricao_produto := 'Descrição do Produto ' || i::TEXT;
        preco_produto := ROUND((RANDOM() * 1000)::NUMERIC, 2); -- Preço entre 0.00 e 1000.00
        categoria_produto := 'Categoria ' || ((i % 5) + 1)::TEXT; -- 5 categorias diferentes

        INSERT INTO dw.Produto (Nome, Descricao, Preco, NomeCategoria)
        VALUES (nome_produto, descricao_produto, preco_produto, categoria_produto);

        i := i + 1;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


-- Executa a Function
SELECT dw.etl_produtos(100);


-- Visualiza os dados
SELECT * FROM dw.produto;



