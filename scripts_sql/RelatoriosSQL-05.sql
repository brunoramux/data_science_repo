-- Estudo de Caso 2 - Extraindo Relatórios do Data Warehouse com Linguagem SQL


-- Cria tabela
CREATE TABLE dw.tb_auditoria_cliente (
    auditoria_id SERIAL PRIMARY KEY,
    operacao VARCHAR(10), -- 'INSERT', 'UPDATE', 'DELETE'
    cliente_id INT,
    nome_antigo VARCHAR(255),
    endereco_antigo VARCHAR(255),
    cidade_antiga VARCHAR(255),
    pais_antigo VARCHAR(255),
    nome_novo VARCHAR(255),
    endereco_novo VARCHAR(255),
    cidade_nova VARCHAR(255),
    pais_novo VARCHAR(255),
    data_operacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Cria a função
CREATE OR REPLACE FUNCTION dw.fn_auditoria_cliente()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO dw.tb_auditoria_cliente(operacao, cliente_id, nome_antigo, endereco_antigo, cidade_antiga, pais_antigo, nome_novo, endereco_novo, cidade_nova, pais_novo)
        VALUES ('DELETE', OLD.ClienteID, OLD.Nome, OLD.Endereco, OLD.CidadeCliente, OLD.PaisCliente, NULL, NULL, NULL, NULL);
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO dw.tb_auditoria_cliente(operacao, cliente_id, nome_antigo, endereco_antigo, cidade_antiga, pais_antigo, nome_novo, endereco_novo, cidade_nova, pais_novo)
        VALUES ('UPDATE', NEW.ClienteID, OLD.Nome, OLD.Endereco, OLD.CidadeCliente, OLD.PaisCliente, NEW.Nome, NEW.Endereco, NEW.CidadeCliente, NEW.PaisCliente);
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO dw.tb_auditoria_cliente(operacao, cliente_id, nome_antigo, endereco_antigo, cidade_antiga, pais_antigo, nome_novo, endereco_novo, cidade_nova, pais_novo)
        VALUES ('INSERT', NEW.ClienteID, NULL, NULL, NULL, NULL, NEW.Nome, NEW.Endereco, NEW.CidadeCliente, NEW.PaisCliente);
        RETURN NEW;
    END IF;
    RETURN NULL; -- Nunca acontecerá
END;
$$ LANGUAGE plpgsql;


-- Cria a trigger
CREATE TRIGGER trg_auditoria_cliente
AFTER INSERT OR UPDATE OR DELETE ON dw.Cliente
FOR EACH ROW EXECUTE FUNCTION dw.fn_auditoria_cliente();


-- Insere um novo cliente
INSERT INTO dw.Cliente (Nome, Endereco, CidadeCliente, PaisCliente)
VALUES ('Bob Silva', 'Rua JP, 10', 'São Paulo', 'Brasil');


-- Visualiza a tabela e auditoria
SELECT * FROM dw.tb_auditoria_cliente
ORDER BY auditoria_id ASC 


-- Atualiza o cliente
UPDATE dw.Cliente
SET Endereco = 'Av. Paulista, 77777777', CidadeCliente = 'São Paulo', PaisCliente = 'Brasil'
WHERE ClienteID = 51;


-- Visualiza a tabela e auditoria
SELECT * FROM dw.tb_auditoria_cliente
ORDER BY auditoria_id ASC 


-- Delete
DELETE FROM dw.Cliente WHERE ClienteID = 51;


-- Visualiza a tabela e auditoria
SELECT * FROM dw.tb_auditoria_cliente
ORDER BY auditoria_id ASC 







