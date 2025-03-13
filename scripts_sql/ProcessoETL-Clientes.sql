-- Estudo de Caso 1 - Construindo e Implementando Modelo de Dados Para Portal de E-commerce
-- Processo ETL da Tabela de Clientes


-- Cria a Function
CREATE OR REPLACE FUNCTION dw.etl_clientes(num_clientes INTEGER)
RETURNS VOID AS $$
DECLARE
    i INTEGER := 1;
    nome_cliente VARCHAR;
    endereco_cliente VARCHAR;
    cidade_cliente VARCHAR;
    pais_cliente VARCHAR;
    cidades VARCHAR[] := ARRAY['São Paulo, Brasil', 'Rio de Janeiro, Brasil', 'Salvador, Brasil', 'New York, EUA', 'Los Angeles, EUA', 'Chicago, EUA'];
BEGIN
    WHILE i <= num_clientes LOOP
        nome_cliente := 'Cliente DSA ' || i::TEXT;
        endereco_cliente := 'Rua ' || chr(trunc(65 + random()*25)::int) || ', ' || trunc(random()*1000)::text;
        cidade_cliente := cidades[1 + TRUNC(RANDOM() * (ARRAY_LENGTH(cidades, 1) - 1))];

        -- Separando a cidade e o país
        pais_cliente := SPLIT_PART(cidade_cliente, ', ', 2);
        cidade_cliente := SPLIT_PART(cidade_cliente, ', ', 1);

        INSERT INTO dw.Cliente (Nome, Endereco, CidadeCliente, PaisCliente)
        VALUES (nome_cliente, endereco_cliente, cidade_cliente, pais_cliente);

        i := i + 1;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


-- Executa a Function
SELECT dw.etl_clientes(50); 


-- Visualiza os dados
SELECT * FROM dw.cliente ORDER BY clienteid ASC;



