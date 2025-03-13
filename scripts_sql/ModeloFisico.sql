-- Estudo de Caso 1 - Construindo e Implementando Modelo de Dados Para Portal de E-commerce
-- Modelo Físico

-- Cria o schema no banco de dados
CREATE SCHEMA dw AUTHORIZATION dsa;

-- Criação da Dimensão Cliente
CREATE TABLE dw.Cliente (
    ClienteID SERIAL PRIMARY KEY,
    Nome VARCHAR(255),
    Endereco VARCHAR(255),
    CidadeCliente VARCHAR(255),
    PaisCliente VARCHAR(255)
);

-- Criação da Dimensão Produto
CREATE TABLE dw.Produto (
    ProdutoID SERIAL PRIMARY KEY,
    Nome VARCHAR(255),
    Descricao VARCHAR(255),
    Preco DECIMAL(10, 2),
    NomeCategoria VARCHAR(255)
);

-- Criação da Dimensão Distribuidor
CREATE TABLE dw.Distribuidor (
    DistribuidorID SERIAL PRIMARY KEY,
    NomeDistribuidor VARCHAR(255),
    CidadeDistribuidor VARCHAR(255),
    PaisDistribuidor VARCHAR(255)
);

-- Criação da Dimensão Data
CREATE TABLE dw.Data (
    DataID SERIAL PRIMARY KEY,
    Data DATE,
    Dia INT,
    Mes INT,
    Ano INT,
    DiaDaSemana VARCHAR(255)
);

-- Criação da Tabela Fato Vendas
CREATE TABLE dw.Vendas (
    ClienteID INT,
    ProdutoID INT,
    DistribuidorID INT,
    DataID INT,
    QuantidadeVendida INT,
    Faturamento DECIMAL(10, 2),
    CustoFrete DECIMAL(10, 2),
    FOREIGN KEY (ClienteID) REFERENCES dw.Cliente(ClienteID),
    FOREIGN KEY (ProdutoID) REFERENCES dw.Produto(ProdutoID),
    FOREIGN KEY (DistribuidorID) REFERENCES dw.Distribuidor(DistribuidorID),
    FOREIGN KEY (DataID) REFERENCES dw.Data(DataID)
);
