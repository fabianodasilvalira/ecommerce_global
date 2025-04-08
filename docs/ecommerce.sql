-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           PostgreSQL 11.21, compiled by Visual C++ build 1914, 64-bit
-- OS do Servidor:               
-- HeidiSQL Versão:              12.10.0.7000
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES  */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Copiando estrutura para tabela public.alembic_version
CREATE TABLE IF NOT EXISTS "alembic_version" (
	"version_num" VARCHAR(32) NOT NULL,
	PRIMARY KEY ("version_num")
);

-- Copiando dados para a tabela public.alembic_version: 0 rows
/*!40000 ALTER TABLE "alembic_version" DISABLE KEYS */;
INSERT IGNORE INTO "alembic_version" ("version_num") VALUES
	('13b20b3cb6d0');
/*!40000 ALTER TABLE "alembic_version" ENABLE KEYS */;

-- Copiando estrutura para tabela public.avaliacao
CREATE TABLE IF NOT EXISTS "avaliacao" (
	"id" SERIAL NOT NULL,
	"produto_id" INTEGER NOT NULL,
	"usuario_id" INTEGER NOT NULL,
	"nota" DOUBLE PRECISION NOT NULL,
	"comentario" VARCHAR(500) NULL DEFAULT NULL,
	"criado_em" TIMESTAMP NULL DEFAULT now(),
	"atualizado_em" TIMESTAMP NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "avaliacao_produto_id_fkey" FOREIGN KEY ("produto_id") REFERENCES "produto" ("id") ON UPDATE NO ACTION ON DELETE CASCADE,
	CONSTRAINT "avaliacao_usuario_id_fkey" FOREIGN KEY ("usuario_id") REFERENCES "usuario" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Copiando dados para a tabela public.avaliacao: 0 rows
/*!40000 ALTER TABLE "avaliacao" DISABLE KEYS */;
/*!40000 ALTER TABLE "avaliacao" ENABLE KEYS */;

-- Copiando estrutura para tabela public.categorias
CREATE TABLE IF NOT EXISTS "categorias" (
	"id" SERIAL NOT NULL,
	"nome" VARCHAR(100) NOT NULL,
	"descricao" TEXT NULL DEFAULT NULL,
	"imagem_url" VARCHAR(255) NULL DEFAULT NULL,
	"cor_destaque" VARCHAR(7) NULL DEFAULT NULL,
	"ativo" BOOLEAN NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	UNIQUE ("nome"),
	KEY ("id")
);

-- Copiando dados para a tabela public.categorias: 0 rows
/*!40000 ALTER TABLE "categorias" DISABLE KEYS */;
INSERT IGNORE INTO "categorias" ("id", "nome", "descricao", "imagem_url", "cor_destaque", "ativo") VALUES
	(1, 'Feminino', 'Produtos feminino', 'https://example.com/img.jpg', '#ff00ff', 'true');
/*!40000 ALTER TABLE "categorias" ENABLE KEYS */;

-- Copiando estrutura para tabela public.categoria_imagem
CREATE TABLE IF NOT EXISTS "categoria_imagem" (
	"id" SERIAL NOT NULL,
	"categoria_id" INTEGER NOT NULL,
	"imagem_url" VARCHAR(500) NOT NULL,
	"tipo" VARCHAR(50) NOT NULL,
	"ordem" INTEGER NULL DEFAULT NULL,
	"criado_em" TIMESTAMP NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "categoria_imagem_categoria_id_fkey" FOREIGN KEY ("categoria_id") REFERENCES "categorias" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Copiando dados para a tabela public.categoria_imagem: 0 rows
/*!40000 ALTER TABLE "categoria_imagem" DISABLE KEYS */;
/*!40000 ALTER TABLE "categoria_imagem" ENABLE KEYS */;

-- Copiando estrutura para tabela public.cupom
CREATE TABLE IF NOT EXISTS "cupom" (
	"id" SERIAL NOT NULL,
	"codigo" VARCHAR(50) NOT NULL,
	"desconto" DOUBLE PRECISION NOT NULL,
	"validade" TIMESTAMP NOT NULL,
	"criado_em" TIMESTAMP NULL DEFAULT now(),
	"ativo" BOOLEAN NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	UNIQUE ("codigo"),
	KEY ("id")
);

-- Copiando dados para a tabela public.cupom: 1 rows
/*!40000 ALTER TABLE "cupom" DISABLE KEYS */;
INSERT IGNORE INTO "cupom" ("id", "codigo", "desconto", "validade", "criado_em", "ativo") VALUES
	(1, 'DESCONTO10', 20, '2025-12-31 23:59:59', '2025-04-08 12:34:32.562114', 'true');
/*!40000 ALTER TABLE "cupom" ENABLE KEYS */;

-- Copiando estrutura para tabela public.endereco
CREATE TABLE IF NOT EXISTS "endereco" (
	"id" SERIAL NOT NULL,
	"usuario_id" INTEGER NOT NULL,
	"logradouro" VARCHAR(255) NOT NULL,
	"numero" VARCHAR(10) NOT NULL,
	"complemento" VARCHAR(100) NULL DEFAULT NULL,
	"bairro" VARCHAR(100) NOT NULL,
	"cidade" VARCHAR(100) NOT NULL,
	"estado" VARCHAR(2) NOT NULL,
	"cep" VARCHAR(9) NOT NULL,
	"criado_em" TIMESTAMP NOT NULL DEFAULT now(),
	"atualizado_em" TIMESTAMP NOT NULL DEFAULT now(),
	"ativo" BOOLEAN NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "endereco_usuario_id_fkey" FOREIGN KEY ("usuario_id") REFERENCES "usuario" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Copiando dados para a tabela public.endereco: 0 rows
/*!40000 ALTER TABLE "endereco" DISABLE KEYS */;
INSERT IGNORE INTO "endereco" ("id", "usuario_id", "logradouro", "numero", "complemento", "bairro", "cidade", "estado", "cep", "criado_em", "atualizado_em", "ativo") VALUES
	(1, 1, 'Rua das Flores', '123', 'Apto 101', 'Centro', 'Cidade', 'SP', '12345-678', '2025-04-08 12:33:25.601402', '2025-04-08 12:33:25.601402', 'true'),
	(2, 1, 'Rua das Flores', '123', 'Apto 101', 'Centro', 'Cidade', 'SP', '12345-678', '2025-04-08 12:33:32.715763', '2025-04-08 12:33:32.715763', 'true');
/*!40000 ALTER TABLE "endereco" ENABLE KEYS */;

-- Copiando estrutura para tabela public.entrega
CREATE TABLE IF NOT EXISTS "entrega" (
	"id" SERIAL NOT NULL,
	"venda_id" INTEGER NOT NULL,
	"status" UNKNOWN NOT NULL,
	"criado_em" TIMESTAMP NOT NULL DEFAULT now(),
	"atualizado_em" TIMESTAMP NOT NULL DEFAULT now(),
	"entregador_id" INTEGER NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "entrega_entregador_id_fkey" FOREIGN KEY ("entregador_id") REFERENCES "usuario" ("id") ON UPDATE NO ACTION ON DELETE SET NULL,
	CONSTRAINT "entrega_venda_id_fkey" FOREIGN KEY ("venda_id") REFERENCES "venda" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Copiando dados para a tabela public.entrega: 0 rows
/*!40000 ALTER TABLE "entrega" DISABLE KEYS */;
/*!40000 ALTER TABLE "entrega" ENABLE KEYS */;

-- Copiando estrutura para tabela public.entregador
CREATE TABLE IF NOT EXISTS "entregador" (
	"id" SERIAL NOT NULL,
	"nome" VARCHAR NOT NULL,
	PRIMARY KEY ("id"),
	KEY ("id")
);

-- Copiando dados para a tabela public.entregador: 0 rows
/*!40000 ALTER TABLE "entregador" DISABLE KEYS */;
/*!40000 ALTER TABLE "entregador" ENABLE KEYS */;

-- Copiando estrutura para tabela public.entrega_candidato
CREATE TABLE IF NOT EXISTS "entrega_candidato" (
	"id" SERIAL NOT NULL,
	"entrega_id" INTEGER NOT NULL,
	"entregador_id" INTEGER NOT NULL,
	"data_interesse" TIMESTAMPTZ NULL DEFAULT now(),
	"status" UNKNOWN NOT NULL,
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "entrega_candidato_entrega_id_fkey" FOREIGN KEY ("entrega_id") REFERENCES "entrega" ("id") ON UPDATE NO ACTION ON DELETE CASCADE,
	CONSTRAINT "entrega_candidato_entregador_id_fkey" FOREIGN KEY ("entregador_id") REFERENCES "entregador" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Copiando dados para a tabela public.entrega_candidato: 0 rows
/*!40000 ALTER TABLE "entrega_candidato" DISABLE KEYS */;
/*!40000 ALTER TABLE "entrega_candidato" ENABLE KEYS */;

-- Copiando estrutura para tabela public.estoque
CREATE TABLE IF NOT EXISTS "estoque" (
	"id" SERIAL NOT NULL,
	"produto_id" INTEGER NOT NULL,
	"quantidade" INTEGER NOT NULL,
	"criado_em" TIMESTAMP NOT NULL DEFAULT now(),
	"atualizado_em" TIMESTAMP NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "estoque_produto_id_fkey" FOREIGN KEY ("produto_id") REFERENCES "produto" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Copiando dados para a tabela public.estoque: 0 rows
/*!40000 ALTER TABLE "estoque" DISABLE KEYS */;
INSERT IGNORE INTO "estoque" ("id", "produto_id", "quantidade", "criado_em", "atualizado_em") VALUES
	(1, 1, 15, '2025-04-08 12:44:05.967641', '2025-04-08 13:03:18.926516'),
	(2, 2, 13, '2025-04-08 13:02:29.699748', '2025-04-08 13:14:52.646332');
/*!40000 ALTER TABLE "estoque" ENABLE KEYS */;

-- Copiando estrutura para tabela public.historico_pagamento
CREATE TABLE IF NOT EXISTS "historico_pagamento" (
	"id" SERIAL NOT NULL,
	"pagamento_id" INTEGER NOT NULL,
	"status" UNKNOWN NOT NULL,
	"metodo_pagamento" VARCHAR(50) NULL DEFAULT NULL,
	"observacao" VARCHAR(255) NULL DEFAULT NULL,
	"data_evento" TIMESTAMP NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "historico_pagamento_pagamento_id_fkey" FOREIGN KEY ("pagamento_id") REFERENCES "pagamento" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Copiando dados para a tabela public.historico_pagamento: 0 rows
/*!40000 ALTER TABLE "historico_pagamento" DISABLE KEYS */;
/*!40000 ALTER TABLE "historico_pagamento" ENABLE KEYS */;

-- Copiando estrutura para tabela public.item_venda
CREATE TABLE IF NOT EXISTS "item_venda" (
	"id" SERIAL NOT NULL,
	"venda_id" INTEGER NOT NULL,
	"produto_id" INTEGER NOT NULL,
	"quantidade" INTEGER NOT NULL,
	"preco_unitario" DOUBLE PRECISION NOT NULL,
	"criado_em" TIMESTAMP NOT NULL DEFAULT now(),
	"atualizado_em" TIMESTAMP NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "item_venda_produto_id_fkey" FOREIGN KEY ("produto_id") REFERENCES "produto" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "item_venda_venda_id_fkey" FOREIGN KEY ("venda_id") REFERENCES "venda" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Copiando dados para a tabela public.item_venda: 3 rows
/*!40000 ALTER TABLE "item_venda" DISABLE KEYS */;
INSERT IGNORE INTO "item_venda" ("id", "venda_id", "produto_id", "quantidade", "preco_unitario", "criado_em", "atualizado_em") VALUES
	(8, 8, 2, 1, 1000, '2025-04-08 13:12:13.789921', '2025-04-08 13:12:13.789921'),
	(9, 9, 2, 1, 1125, '2025-04-08 13:14:37.704266', '2025-04-08 13:14:37.704266'),
	(10, 10, 2, 1, 1000, '2025-04-08 13:14:52.646332', '2025-04-08 13:14:52.646332');
/*!40000 ALTER TABLE "item_venda" ENABLE KEYS */;

-- Copiando estrutura para tabela public.lista_desejos
CREATE TABLE IF NOT EXISTS "lista_desejos" (
	"id" SERIAL NOT NULL,
	"usuario_id" INTEGER NOT NULL,
	"produto_id" INTEGER NOT NULL,
	"criado_em" TIMESTAMP NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "lista_desejos_produto_id_fkey" FOREIGN KEY ("produto_id") REFERENCES "produto" ("id") ON UPDATE NO ACTION ON DELETE CASCADE,
	CONSTRAINT "lista_desejos_usuario_id_fkey" FOREIGN KEY ("usuario_id") REFERENCES "usuario" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Copiando dados para a tabela public.lista_desejos: 0 rows
/*!40000 ALTER TABLE "lista_desejos" DISABLE KEYS */;
/*!40000 ALTER TABLE "lista_desejos" ENABLE KEYS */;

-- Copiando estrutura para tabela public.movimentacao_estoque
CREATE TABLE IF NOT EXISTS "movimentacao_estoque" (
	"id" SERIAL NOT NULL,
	"produto_id" INTEGER NOT NULL,
	"quantidade" INTEGER NOT NULL,
	"tipo_movimentacao" UNKNOWN NOT NULL,
	"data" TIMESTAMP NOT NULL DEFAULT now(),
	"criado_em" TIMESTAMP NOT NULL DEFAULT now(),
	"atualizado_em" TIMESTAMP NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "movimentacao_estoque_produto_id_fkey" FOREIGN KEY ("produto_id") REFERENCES "produto" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Copiando dados para a tabela public.movimentacao_estoque: 0 rows
/*!40000 ALTER TABLE "movimentacao_estoque" DISABLE KEYS */;
/*!40000 ALTER TABLE "movimentacao_estoque" ENABLE KEYS */;

-- Copiando estrutura para tabela public.pagamento
CREATE TABLE IF NOT EXISTS "pagamento" (
	"id" SERIAL NOT NULL,
	"venda_id" INTEGER NOT NULL,
	"valor" NUMERIC(10,2) NOT NULL,
	"status" UNKNOWN NOT NULL,
	"metodo_pagamento" VARCHAR(30) NOT NULL,
	"transacao_id" VARCHAR(100) NULL DEFAULT NULL,
	"criado_em" TIMESTAMP NOT NULL DEFAULT now(),
	"atualizado_em" TIMESTAMP NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "pagamento_venda_id_fkey" FOREIGN KEY ("venda_id") REFERENCES "venda" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Copiando dados para a tabela public.pagamento: 0 rows
/*!40000 ALTER TABLE "pagamento" DISABLE KEYS */;
/*!40000 ALTER TABLE "pagamento" ENABLE KEYS */;

-- Copiando estrutura para tabela public.produto
CREATE TABLE IF NOT EXISTS "produto" (
	"id" SERIAL NOT NULL,
	"sku" VARCHAR(50) NOT NULL,
	"nome" VARCHAR(100) NOT NULL,
	"descricao" VARCHAR(255) NULL DEFAULT NULL,
	"preco" NUMERIC(10,2) NOT NULL,
	"volume" DOUBLE PRECISION NULL DEFAULT NULL,
	"unidade_medida" VARCHAR(10) NULL DEFAULT NULL,
	"ativo" BOOLEAN NULL DEFAULT NULL,
	"categoria_id" INTEGER NULL DEFAULT NULL,
	"margem_lucro" NUMERIC(5,2) NOT NULL,
	"preco_final" NUMERIC(10,2) NOT NULL,
	PRIMARY KEY ("id"),
	KEY ("id"),
	UNIQUE ("sku"),
	CONSTRAINT "produto_categoria_id_fkey" FOREIGN KEY ("categoria_id") REFERENCES "categorias" ("id") ON UPDATE NO ACTION ON DELETE SET NULL
);

-- Copiando dados para a tabela public.produto: 0 rows
/*!40000 ALTER TABLE "produto" DISABLE KEYS */;
INSERT IGNORE INTO "produto" ("id", "sku", "nome", "descricao", "preco", "volume", "unidade_medida", "ativo", "categoria_id", "margem_lucro", "preco_final") VALUES
	(1, 'FAB-FEM-7071', 'fabio', 'Notbook com GPU dedicada', 5999.90, NULL, NULL, 'true', 1, 20.00, 7199.88),
	(2, 'CSA-FEM-1019', 'csa', 'casa com GPU dedicada', 1000.00, NULL, NULL, 'true', 1, 25.00, 1250.00);
/*!40000 ALTER TABLE "produto" ENABLE KEYS */;

-- Copiando estrutura para tabela public.produto_destaque
CREATE TABLE IF NOT EXISTS "produto_destaque" (
	"id" SERIAL NOT NULL,
	"produto_id" INTEGER NOT NULL,
	"criado_em" TIMESTAMP NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	UNIQUE ("produto_id"),
	KEY ("id"),
	CONSTRAINT "produto_destaque_produto_id_fkey" FOREIGN KEY ("produto_id") REFERENCES "produto" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Copiando dados para a tabela public.produto_destaque: 0 rows
/*!40000 ALTER TABLE "produto_destaque" DISABLE KEYS */;
/*!40000 ALTER TABLE "produto_destaque" ENABLE KEYS */;

-- Copiando estrutura para tabela public.produto_imagem
CREATE TABLE IF NOT EXISTS "produto_imagem" (
	"id" SERIAL NOT NULL,
	"produto_id" INTEGER NOT NULL,
	"imagem_url" VARCHAR(500) NOT NULL,
	"tipo" VARCHAR(50) NOT NULL,
	"ordem" INTEGER NULL DEFAULT NULL,
	"criado_em" TIMESTAMP NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "produto_imagem_produto_id_fkey" FOREIGN KEY ("produto_id") REFERENCES "produto" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Copiando dados para a tabela public.produto_imagem: 0 rows
/*!40000 ALTER TABLE "produto_imagem" DISABLE KEYS */;
/*!40000 ALTER TABLE "produto_imagem" ENABLE KEYS */;

-- Copiando estrutura para tabela public.promocao
CREATE TABLE IF NOT EXISTS "promocao" (
	"id" SERIAL NOT NULL,
	"produto_id" INTEGER NOT NULL,
	"desconto_percentual" NUMERIC(5,2) NULL DEFAULT NULL,
	"preco_promocional" NUMERIC(10,2) NULL DEFAULT NULL,
	"data_inicio" TIMESTAMP NOT NULL,
	"data_fim" TIMESTAMP NOT NULL,
	"ativo" BOOLEAN NOT NULL,
	"criado_em" TIMESTAMP NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	KEY ("id"),
	KEY ("produto_id"),
	CONSTRAINT "promocao_produto_id_fkey" FOREIGN KEY ("produto_id") REFERENCES "produto" ("id") ON UPDATE NO ACTION ON DELETE CASCADE,
	CONSTRAINT "check_datas_promocao" CHECK (((data_fim > data_inicio))),
	CONSTRAINT "check_desconto" CHECK ((((desconto_percentual >= (0)::numeric) AND (desconto_percentual <= (100)::numeric)))),
	CONSTRAINT "check_preco_promocional" CHECK ((((preco_promocional IS NULL) OR (preco_promocional > (0)::numeric))))
);

-- Copiando dados para a tabela public.promocao: 0 rows
/*!40000 ALTER TABLE "promocao" DISABLE KEYS */;
/*!40000 ALTER TABLE "promocao" ENABLE KEYS */;

-- Copiando estrutura para tabela public.rastreamento_entrega
CREATE TABLE IF NOT EXISTS "rastreamento_entrega" (
	"id" SERIAL NOT NULL,
	"entrega_id" INTEGER NOT NULL,
	"status" VARCHAR(100) NOT NULL,
	"atualizado_em" TIMESTAMP NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	KEY ("entrega_id"),
	KEY ("id"),
	CONSTRAINT "rastreamento_entrega_entrega_id_fkey" FOREIGN KEY ("entrega_id") REFERENCES "entrega" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Copiando dados para a tabela public.rastreamento_entrega: 0 rows
/*!40000 ALTER TABLE "rastreamento_entrega" DISABLE KEYS */;
/*!40000 ALTER TABLE "rastreamento_entrega" ENABLE KEYS */;

-- Copiando estrutura para tabela public.usuario
CREATE TABLE IF NOT EXISTS "usuario" (
	"id" SERIAL NOT NULL,
	"nome" VARCHAR(100) NOT NULL,
	"email" VARCHAR(100) NOT NULL,
	"senha" VARCHAR(255) NOT NULL,
	"cpf_cnpj" VARCHAR(20) NOT NULL,
	"telefone" VARCHAR(20) NULL DEFAULT NULL,
	"tipo_usuario" UNKNOWN NOT NULL,
	"refresh_token" VARCHAR(500) NULL DEFAULT NULL,
	"criado_em" TIMESTAMP NOT NULL DEFAULT now(),
	"atualizado_em" TIMESTAMP NOT NULL DEFAULT now(),
	"ativo" BOOLEAN NOT NULL,
	PRIMARY KEY ("id"),
	UNIQUE ("cpf_cnpj"),
	UNIQUE ("email"),
	KEY ("id")
);

-- Copiando dados para a tabela public.usuario: 0 rows
/*!40000 ALTER TABLE "usuario" DISABLE KEYS */;
INSERT IGNORE INTO "usuario" ("id", "nome", "email", "senha", "cpf_cnpj", "telefone", "tipo_usuario", "refresh_token", "criado_em", "atualizado_em", "ativo") VALUES
	(2, 'João Silva', 'anovos@email.com', '$2b$12$CsbhRIoTLIM113JsIb5FyekD8vwonRQgcRf/ccmOZgUeOF7ia9QFS', '123.456.789-09', '11987654321', 'ADMIN', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzQ0NjM0MjI5fQ.nvEkCGEZobDbUhnU1vByej6bLILGH8Hmn7vzVu4Wm-o', '2025-04-07 07:51:18.103978', '2025-04-07 10:04:37.187244', 'true'),
	(1, 'Novo Nomes', 'josao@email.com', '$2b$12$cCBSRsJpH0s9ls/JeyIfRuKVCHJPrICaM7ytgeyhfp0aDHzKlRJNi', '12345678909', '11999999999s2', 'ADMIN', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzQ0NzM0MzY4fQ.QWXkzoz-27sQRbbvdLhTuWW1yRiaeAmXr03CgusgigA', '2025-04-07 07:40:56.228734', '2025-04-08 13:26:08.547009', 'true');
/*!40000 ALTER TABLE "usuario" ENABLE KEYS */;

-- Copiando estrutura para tabela public.venda
CREATE TABLE IF NOT EXISTS "venda" (
	"id" SERIAL NOT NULL,
	"usuario_id" INTEGER NOT NULL,
	"endereco_id" INTEGER NULL DEFAULT NULL,
	"cupom_id" INTEGER NULL DEFAULT NULL,
	"total" NUMERIC(10,2) NOT NULL,
	"status" UNKNOWN NOT NULL,
	"data_venda" TIMESTAMP NOT NULL DEFAULT now(),
	"is_ativo" BOOLEAN NULL DEFAULT true,
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "venda_cupom_id_fkey" FOREIGN KEY ("cupom_id") REFERENCES "cupom" ("id") ON UPDATE NO ACTION ON DELETE SET NULL,
	CONSTRAINT "venda_endereco_id_fkey" FOREIGN KEY ("endereco_id") REFERENCES "endereco" ("id") ON UPDATE NO ACTION ON DELETE SET NULL,
	CONSTRAINT "venda_usuario_id_fkey" FOREIGN KEY ("usuario_id") REFERENCES "usuario" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Copiando dados para a tabela public.venda: 0 rows
/*!40000 ALTER TABLE "venda" DISABLE KEYS */;
INSERT IGNORE INTO "venda" ("id", "usuario_id", "endereco_id", "cupom_id", "total", "status", "data_venda", "is_ativo") VALUES
	(1, 1, 1, 1, 10799.82, 'PENDENTE', '2025-04-08 12:51:50.670434', 'true'),
	(2, 1, 1, 1, 10799.82, 'PENDENTE', '2025-04-08 12:53:42.413455', 'true'),
	(3, 1, 1, 1, 5399.91, 'PENDENTE', '2025-04-08 13:03:18.926516', 'true'),
	(4, 1, 1, 1, 900.00, 'PENDENTE', '2025-04-08 13:03:29.679711', 'true'),
	(5, 1, 1, 1, 900.00, 'PENDENTE', '2025-04-08 13:08:04.923645', 'true'),
	(6, 1, 1, 1, 900.00, 'PENDENTE', '2025-04-08 13:11:16.039655', 'true'),
	(7, 1, 1, 1, 900.00, 'PENDENTE', '2025-04-08 13:11:19.780273', 'true'),
	(8, 1, 1, 1, 900.00, 'PENDENTE', '2025-04-08 13:12:13.789921', 'true'),
	(9, 1, 1, 1, 1125.00, 'PENDENTE', '2025-04-08 13:14:37.704266', 'true'),
	(10, 1, 1, 1, 1000.00, 'PENDENTE', '2025-04-08 13:14:52.646332', 'true');
/*!40000 ALTER TABLE "venda" ENABLE KEYS */;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
