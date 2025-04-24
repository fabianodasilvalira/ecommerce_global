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
REPLACE INTO "alembic_version" ("version_num") VALUES
	('fcc41d2fcc1c');
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

-- Copiando estrutura para tabela public.carrinho
CREATE TABLE IF NOT EXISTS "carrinho" (
	"id" SERIAL NOT NULL,
	"usuario_id" INTEGER NULL DEFAULT NULL,
	"criado_em" TIMESTAMPTZ NULL DEFAULT now(),
	"atualizado_em" TIMESTAMPTZ NULL DEFAULT NULL,
	"is_finalizado" BOOLEAN NULL DEFAULT NULL,
	"data_finalizacao" TIMESTAMP NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "carrinho_usuario_id_fkey" FOREIGN KEY ("usuario_id") REFERENCES "usuario" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Copiando dados para a tabela public.carrinho: 2 rows
/*!40000 ALTER TABLE "carrinho" DISABLE KEYS */;
REPLACE INTO "carrinho" ("id", "usuario_id", "criado_em", "atualizado_em", "is_finalizado", "data_finalizacao") VALUES
	(6, 1, '2025-04-24 11:20:02.876924-03', '2025-04-24 11:20:31.33888-03', 'true', '2025-04-24 11:20:31.33888'),
	(7, 1, '2025-04-24 11:22:13.638071-03', '2025-04-24 11:22:24.341064-03', 'true', '2025-04-24 11:22:24.341064');
/*!40000 ALTER TABLE "carrinho" ENABLE KEYS */;

-- Copiando estrutura para tabela public.categorias
CREATE TABLE IF NOT EXISTS "categorias" (
	"id" SERIAL NOT NULL,
	"nome" VARCHAR(100) NOT NULL,
	"slug" VARCHAR(100) NOT NULL,
	"descricao" TEXT NULL DEFAULT NULL,
	"imagem_url" VARCHAR(255) NULL DEFAULT NULL,
	"cor_destaque" VARCHAR(7) NULL DEFAULT NULL,
	"ordem" INTEGER NULL DEFAULT NULL,
	"meta_title" VARCHAR(100) NULL DEFAULT NULL,
	"meta_description" VARCHAR(255) NULL DEFAULT NULL,
	"ativo" BOOLEAN NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	UNIQUE ("nome"),
	UNIQUE ("slug"),
	KEY ("id")
);

-- Copiando dados para a tabela public.categorias: 0 rows
/*!40000 ALTER TABLE "categorias" DISABLE KEYS */;
REPLACE INTO "categorias" ("id", "nome", "slug", "descricao", "imagem_url", "cor_destaque", "ordem", "meta_title", "meta_description", "ativo") VALUES
	(1, 'Masculino', 'masculino', 'Roupas, calçados e acessórios para homens', 'https://exemplo.com/categorias/masculino.jpg', '#2E86C1', 1, 'Moda Masculina | Loja Virtual', 'Encontre as melhores roupas e acessórios masculinos com os melhores preços', 'true'),
	(2, 'Feminino', 'feminino', 'Roupas, calçados e acessórios para mulheres', 'https://exemplo.com/categorias/feminino.jpg', '#E74C3C', 2, 'Moda Feminina | Loja Virtual', 'Descubra nossa coleção de roupas e acessórios femininos', 'true'),
	(3, 'Infantil', 'infantil', 'Roupas e acessórios para crianças de 0 a 12 anos', 'https://exemplo.com/categorias/infantil.jpg', '#F39C12', 3, 'Moda Infantil | Loja Virtual', 'Tudo para o look dos pequenos com conforto e qualidade', 'true'),
	(4, 'Unisex', 'unisex', 'Produtos que servem para ambos os sexos', 'https://exemplo.com/categorias/unisex.jpg', '#27AE60', 4, 'Produtos Unissex | Loja Virtual', 'Itens que combinam com qualquer estilo', 'true');
/*!40000 ALTER TABLE "categorias" ENABLE KEYS */;

-- Copiando estrutura para tabela public.categoria_imagem
CREATE TABLE IF NOT EXISTS "categoria_imagem" (
	"id" SERIAL NOT NULL,
	"categoria_id" INTEGER NOT NULL,
	"imagem_url" VARCHAR(500) NOT NULL,
	"tipo" VARCHAR(50) NOT NULL,
	"ordem" INTEGER NOT NULL,
	"criado_em" TIMESTAMP NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "categoria_imagem_categoria_id_fkey" FOREIGN KEY ("categoria_id") REFERENCES "categorias" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Copiando dados para a tabela public.categoria_imagem: 0 rows
/*!40000 ALTER TABLE "categoria_imagem" DISABLE KEYS */;
REPLACE INTO "categoria_imagem" ("id", "categoria_id", "imagem_url", "tipo", "ordem", "criado_em") VALUES
	(1, 1, 'https://exemplo.com/categorias/masculino-destaque1.jpg', 'destaque', 1, '2025-04-15 07:23:45.373101'),
	(2, 1, 'https://exemplo.com/categorias/masculino-thumbnail1.jpg', 'thumbnail', 1, '2025-04-15 07:23:45.373101'),
	(3, 1, 'https://exemplo.com/categorias/masculino-banner1.jpg', 'banner', 1, '2025-04-15 07:23:45.373101'),
	(4, 2, 'https://exemplo.com/categorias/feminino-destaque1.jpg', 'destaque', 1, '2025-04-15 07:23:45.373101'),
	(5, 2, 'https://exemplo.com/categorias/feminino-thumbnail1.jpg', 'thumbnail', 1, '2025-04-15 07:23:45.373101'),
	(6, 2, 'https://exemplo.com/categorias/feminino-banner1.jpg', 'banner', 1, '2025-04-15 07:23:45.373101'),
	(7, 3, 'https://exemplo.com/categorias/infantil-destaque1.jpg', 'destaque', 1, '2025-04-15 07:23:45.373101'),
	(8, 3, 'https://exemplo.com/categorias/infantil-thumbnail1.jpg', 'thumbnail', 1, '2025-04-15 07:23:45.373101'),
	(9, 4, 'https://exemplo.com/categorias/unisex-destaque1.jpg', 'destaque', 1, '2025-04-15 07:23:45.373101'),
	(10, 4, 'https://exemplo.com/categorias/unisex-banner1.jpg', 'banner', 1, '2025-04-15 07:23:45.373101');
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

-- Copiando dados para a tabela public.cupom: 0 rows
/*!40000 ALTER TABLE "cupom" DISABLE KEYS */;
REPLACE INTO "cupom" ("id", "codigo", "desconto", "validade", "criado_em", "ativo") VALUES
	(1, 'DESCONTO10', 10, '2025-12-31 23:59:59', '2025-04-23 08:05:12.232772', 'true');
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
REPLACE INTO "endereco" ("id", "usuario_id", "logradouro", "numero", "complemento", "bairro", "cidade", "estado", "cep", "criado_em", "atualizado_em", "ativo") VALUES
	(1, 1, 'Rua das Flores', '123', 'Apto 101', 'Centro', 'Cidade', 'SP', '12345-678', '2025-04-16 11:19:00.621719', '2025-04-16 11:19:00.621719', 'true');
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

-- Copiando estrutura para tabela public.entregador_info
CREATE TABLE IF NOT EXISTS "entregador_info" (
	"id" SERIAL NOT NULL,
	"usuario_id" INTEGER NULL DEFAULT NULL,
	"placa" VARCHAR(10) NULL DEFAULT NULL,
	"cnh" VARCHAR(20) NULL DEFAULT NULL,
	"endereco" VARCHAR(255) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	UNIQUE ("usuario_id"),
	CONSTRAINT "entregador_info_usuario_id_fkey" FOREIGN KEY ("usuario_id") REFERENCES "usuario" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Copiando dados para a tabela public.entregador_info: 0 rows
/*!40000 ALTER TABLE "entregador_info" DISABLE KEYS */;
/*!40000 ALTER TABLE "entregador_info" ENABLE KEYS */;

-- Copiando estrutura para tabela public.entrega_candidato
CREATE TABLE IF NOT EXISTS "entrega_candidato" (
	"id" SERIAL NOT NULL,
	"entrega_id" INTEGER NOT NULL,
	"usuario_id" INTEGER NOT NULL,
	"data_interesse" TIMESTAMPTZ NULL DEFAULT now(),
	"status" UNKNOWN NOT NULL,
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "entrega_candidato_entrega_id_fkey" FOREIGN KEY ("entrega_id") REFERENCES "entrega" ("id") ON UPDATE NO ACTION ON DELETE CASCADE,
	CONSTRAINT "entrega_candidato_usuario_id_fkey" FOREIGN KEY ("usuario_id") REFERENCES "usuario" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
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

-- Copiando dados para a tabela public.estoque: 2 rows
/*!40000 ALTER TABLE "estoque" DISABLE KEYS */;
REPLACE INTO "estoque" ("id", "produto_id", "quantidade", "criado_em", "atualizado_em") VALUES
	(2, 2, 48, '2025-04-16 11:27:02.205666', '2025-04-24 10:23:06.339867'),
	(1, 1, 9894, '2025-04-16 11:26:58.453187', '2025-04-24 11:22:24.341064');
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

-- Copiando estrutura para tabela public.item_carrinho
CREATE TABLE IF NOT EXISTS "item_carrinho" (
	"id" SERIAL NOT NULL,
	"carrinho_id" INTEGER NULL DEFAULT NULL,
	"produto_id" INTEGER NULL DEFAULT NULL,
	"quantidade" INTEGER NULL DEFAULT NULL,
	"valor_unitario" NUMERIC(10,2) NULL DEFAULT NULL,
	"valor_total" NUMERIC(10,2) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "item_carrinho_carrinho_id_fkey" FOREIGN KEY ("carrinho_id") REFERENCES "carrinho" ("id") ON UPDATE NO ACTION ON DELETE CASCADE,
	CONSTRAINT "item_carrinho_produto_id_fkey" FOREIGN KEY ("produto_id") REFERENCES "produto" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Copiando dados para a tabela public.item_carrinho: 1 rows
/*!40000 ALTER TABLE "item_carrinho" DISABLE KEYS */;
REPLACE INTO "item_carrinho" ("id", "carrinho_id", "produto_id", "quantidade", "valor_unitario", "valor_total") VALUES
	(14, 6, 1, 4, 129.90, 519.60),
	(15, 7, 1, 2, 129.90, 259.80);
/*!40000 ALTER TABLE "item_carrinho" ENABLE KEYS */;

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

-- Copiando dados para a tabela public.item_venda: 2 rows
/*!40000 ALTER TABLE "item_venda" DISABLE KEYS */;
REPLACE INTO "item_venda" ("id", "venda_id", "produto_id", "quantidade", "preco_unitario", "criado_em", "atualizado_em") VALUES
	(73, 72, 1, 4, 50, '2025-04-24 11:20:31.33888', '2025-04-24 11:20:31.33888'),
	(74, 73, 1, 2, 168.87, '2025-04-24 11:22:24.341064', '2025-04-24 11:22:24.341064');
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

-- Copiando dados para a tabela public.lista_desejos: 1 rows
/*!40000 ALTER TABLE "lista_desejos" DISABLE KEYS */;
REPLACE INTO "lista_desejos" ("id", "usuario_id", "produto_id", "criado_em") VALUES
	(3, 1, 2, '2025-04-15 10:57:32.522863');
/*!40000 ALTER TABLE "lista_desejos" ENABLE KEYS */;

-- Copiando estrutura para tabela public.movimentacao_estoque
CREATE TABLE IF NOT EXISTS "movimentacao_estoque" (
	"id" SERIAL NOT NULL,
	"venda_id" INTEGER NULL DEFAULT NULL,
	"produto_id" INTEGER NOT NULL,
	"quantidade" INTEGER NOT NULL,
	"tipo_movimentacao" UNKNOWN NOT NULL,
	"data" TIMESTAMP NOT NULL DEFAULT now(),
	"criado_em" TIMESTAMP NOT NULL DEFAULT now(),
	"atualizado_em" TIMESTAMP NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "movimentacao_estoque_produto_id_fkey" FOREIGN KEY ("produto_id") REFERENCES "produto" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "movimentacao_estoque_venda_id_fkey" FOREIGN KEY ("venda_id") REFERENCES "venda" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Copiando dados para a tabela public.movimentacao_estoque: 0 rows
/*!40000 ALTER TABLE "movimentacao_estoque" DISABLE KEYS */;
REPLACE INTO "movimentacao_estoque" ("id", "venda_id", "produto_id", "quantidade", "tipo_movimentacao", "data", "criado_em", "atualizado_em") VALUES
	(73, 72, 1, 4, 'SAIDA', '2025-04-24 14:20:31.350843', '2025-04-24 11:20:31.33888', '2025-04-24 11:20:31.33888'),
	(74, 73, 1, 2, 'SAIDA', '2025-04-24 14:22:24.350842', '2025-04-24 11:22:24.341064', '2025-04-24 11:22:24.341064');
/*!40000 ALTER TABLE "movimentacao_estoque" ENABLE KEYS */;

-- Copiando estrutura para tabela public.pagamento
CREATE TABLE IF NOT EXISTS "pagamento" (
	"id" SERIAL NOT NULL,
	"venda_id" INTEGER NOT NULL,
	"valor" NUMERIC(10,2) NOT NULL,
	"status" UNKNOWN NOT NULL,
	"metodo_pagamento" UNKNOWN NOT NULL,
	"transacao_id" VARCHAR(100) NULL DEFAULT NULL,
	"criado_em" TIMESTAMP NOT NULL DEFAULT now(),
	"atualizado_em" TIMESTAMP NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "pagamento_venda_id_fkey" FOREIGN KEY ("venda_id") REFERENCES "venda" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Copiando dados para a tabela public.pagamento: 1 rows
/*!40000 ALTER TABLE "pagamento" DISABLE KEYS */;
REPLACE INTO "pagamento" ("id", "venda_id", "valor", "status", "metodo_pagamento", "transacao_id", "criado_em", "atualizado_em") VALUES
	(72, 72, 200.00, 'PENDENTE', 'PIX', NULL, '2025-04-24 11:20:31.33888', '2025-04-24 11:20:31.33888'),
	(73, 73, 337.74, 'PENDENTE', 'PIX', NULL, '2025-04-24 11:22:24.341064', '2025-04-24 11:22:24.341064');
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

-- Copiando dados para a tabela public.produto: 15 rows
/*!40000 ALTER TABLE "produto" DISABLE KEYS */;
REPLACE INTO "produto" ("id", "sku", "nome", "descricao", "preco", "volume", "unidade_medida", "ativo", "categoria_id", "margem_lucro", "preco_final") VALUES
	(1, 'M001', 'Camisa Social Branca', 'Camisa social manga longa 100% algodão', 129.90, NULL, NULL, 'true', 1, 30.00, 168.87),
	(2, 'M002', 'Calça Jeans Slim', 'Calça jeans masculina modelo slim fit', 159.90, NULL, NULL, 'true', 1, 35.00, 215.87),
	(3, 'M003', 'Tênis Casual', 'Tênis masculino couro sintético', 199.90, NULL, NULL, 'true', 1, 25.00, 249.88),
	(4, 'M004', 'Cueca Boxer Algodão', 'Pack com 3 cuecas boxer cotton', 49.90, NULL, NULL, 'true', 1, 40.00, 69.86),
	(5, 'F001', 'Vestido Midi Floral', 'Vestido floral com decote V', 139.90, NULL, NULL, 'true', 2, 35.00, 188.87),
	(6, 'F002', 'Blusa Feminina Renda', 'Blusa manga longa com detalhes em renda', 89.90, NULL, NULL, 'true', 2, 40.00, 125.86),
	(7, 'F003', 'Saia Jeans', 'Saia jeans midi com cós alto', 79.90, NULL, NULL, 'true', 2, 30.00, 103.87),
	(8, 'F004', 'Bolsa Transversal', 'Bolsa feminina em couro sintético', 119.90, NULL, NULL, 'true', 2, 25.00, 149.88),
	(9, 'F005', 'Conjunto Pijama', 'Conjunto pijama algodão estampado', 69.90, NULL, NULL, 'true', 2, 35.00, 94.37),
	(10, 'I001', 'Conjunto Moletom Infantil', 'Conjunto moletom com estampa divertida', 59.90, NULL, NULL, 'true', 3, 30.00, 77.87),
	(11, 'I002', 'Body Bebê Algodão', 'Pack com 3 bodies manga curta', 39.90, NULL, NULL, 'true', 3, 35.00, 53.87),
	(12, 'I003', 'Tênis Infantil LED', 'Tênis infantil com luzes LED', 89.90, NULL, NULL, 'true', 3, 25.00, 112.38),
	(13, 'U001', 'Boné Ajustável', 'Boné unissex em algodão', 39.90, NULL, NULL, 'true', 4, 25.00, 49.88),
	(14, 'U002', 'Meias Cano Alto', 'Pack com 5 pares de meias', 29.90, NULL, NULL, 'true', 4, 40.00, 41.86),
	(15, 'U003', 'Mochila Escolar', 'Mochila resistente para notebooks', 99.90, NULL, NULL, 'true', 4, 30.00, 129.87);
/*!40000 ALTER TABLE "produto" ENABLE KEYS */;

-- Copiando estrutura para tabela public.produto_destaque
CREATE TABLE IF NOT EXISTS "produto_destaque" (
	"id" SERIAL NOT NULL,
	"produto_id" INTEGER NOT NULL,
	"criado_em" TIMESTAMP NULL DEFAULT NULL,
	"posicao" INTEGER NULL DEFAULT NULL,
	"ativo" BOOLEAN NULL DEFAULT NULL,
	"tipo_destaque" VARCHAR(20) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	UNIQUE ("produto_id"),
	KEY ("id"),
	CONSTRAINT "produto_destaque_produto_id_fkey" FOREIGN KEY ("produto_id") REFERENCES "produto" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Copiando dados para a tabela public.produto_destaque: 0 rows
/*!40000 ALTER TABLE "produto_destaque" DISABLE KEYS */;
REPLACE INTO "produto_destaque" ("id", "produto_id", "criado_em", "posicao", "ativo", "tipo_destaque") VALUES
	(3, 2, '2025-04-15 10:27:19.641042', 1, 'true', 'principal'),
	(1, 1, '2025-04-15 10:27:11.146805', 2, 'false', 'oferta');
/*!40000 ALTER TABLE "produto_destaque" ENABLE KEYS */;

-- Copiando estrutura para tabela public.produto_imagem
CREATE TABLE IF NOT EXISTS "produto_imagem" (
	"id" SERIAL NOT NULL,
	"produto_id" INTEGER NOT NULL,
	"imagem_url" VARCHAR(500) NOT NULL,
	"tipo" UNKNOWN NOT NULL,
	"ordem" INTEGER NULL DEFAULT NULL,
	"visivel" BOOLEAN NULL DEFAULT NULL,
	"criado_em" TIMESTAMP NOT NULL DEFAULT now(),
	"atualizado_em" TIMESTAMP NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	KEY ("produto_id", "ordem"),
	KEY ("id"),
	CONSTRAINT "produto_imagem_produto_id_fkey" FOREIGN KEY ("produto_id") REFERENCES "produto" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Copiando dados para a tabela public.produto_imagem: 0 rows
/*!40000 ALTER TABLE "produto_imagem" DISABLE KEYS */;
REPLACE INTO "produto_imagem" ("id", "produto_id", "imagem_url", "tipo", "ordem", "visivel", "criado_em", "atualizado_em") VALUES
	(1, 1, 'https://exemplo.com/produtos/M001-destaque.jpg', 'DESTAQUE', 1, 'true', '2025-04-15 07:25:08.271253', NULL),
	(4, 2, 'https://exemplo.com/produtos/M002-destaque.jpg', 'DESTAQUE', 1, 'true', '2025-04-15 07:25:08.271253', NULL),
	(7, 3, 'https://exemplo.com/produtos/M003-destaque.jpg', 'DESTAQUE', 1, 'true', '2025-04-15 07:25:08.271253', NULL),
	(2, 1, 'https://exemplo.com/produtos/M001-galeria1.jpg', 'GALERIA', 2, 'true', '2025-04-15 07:25:08.271253', NULL),
	(3, 1, 'https://exemplo.com/produtos/M001-zoom.jpg', 'ZOOM', 3, 'true', '2025-04-15 07:25:08.271253', NULL),
	(5, 2, 'https://exemplo.com/produtos/M002-thumbnail.jpg', 'THUMBNAIL', 2, 'true', '2025-04-15 07:25:08.271253', NULL),
	(6, 2, 'https://exemplo.com/produtos/M002-galeria1.jpg', 'GALERIA', 3, 'true', '2025-04-15 07:25:08.271253', NULL),
	(8, 3, 'https://exemplo.com/produtos/M003-galeria1.jpg', 'GALERIA', 2, 'true', '2025-04-15 07:25:08.271253', NULL),
	(9, 5, 'https://exemplo.com/produtos/F001-destaque.jpg', 'DESTAQUE', 1, 'true', '2025-04-15 07:25:08.271253', NULL),
	(10, 5, 'https://exemplo.com/produtos/F001-thumbnail.jpg', 'THUMBNAIL', 2, 'true', '2025-04-15 07:25:08.271253', NULL);
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

-- Copiando dados para a tabela public.promocao: 4 rows
/*!40000 ALTER TABLE "promocao" DISABLE KEYS */;
REPLACE INTO "promocao" ("id", "produto_id", "desconto_percentual", "preco_promocional", "data_inicio", "data_fim", "ativo", "criado_em") VALUES
	(3, 3, NULL, 50.00, '2025-04-06 00:00:00', '2026-06-06 23:59:59', 'true', '2025-04-23 08:11:29.430735'),
	(4, 4, NULL, 50.00, '2025-04-06 00:00:00', '2026-06-06 23:59:59', 'true', '2025-04-23 08:13:14.181258'),
	(5, 5, NULL, 50.00, '2025-04-06 00:00:00', '2026-06-06 23:59:59', 'true', '2025-04-23 08:20:14.619865'),
	(2, 2, 50.00, 50.00, '2025-04-06 00:00:00', '2026-06-06 23:59:59', 'true', '2025-04-23 08:10:35.118428');
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
	"tipo_usuario" VARCHAR(11) NOT NULL,
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
REPLACE INTO "usuario" ("id", "nome", "email", "senha", "cpf_cnpj", "telefone", "tipo_usuario", "refresh_token", "criado_em", "atualizado_em", "ativo") VALUES
	(1, 'João Silva', 'joao@email.com', '$2b$12$Vc4HCBeFCq9m8cF5FMn82./4aFv3I1v8Z4aZOUcWfiaRBqI2j5ISq', '123.456.789-09', '11987654321', 'ADMIN', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzQ2MTA0NzYxfQ.jWkOHeETaFt7WkS8KYi0dJ136ZuWSRFyhgOYXbicNwY', '2025-04-15 07:49:49.56323', '2025-04-24 10:06:01.51768', 'true');
/*!40000 ALTER TABLE "usuario" ENABLE KEYS */;

-- Copiando estrutura para tabela public.venda
CREATE TABLE IF NOT EXISTS "venda" (
	"id" SERIAL NOT NULL,
	"usuario_id" INTEGER NOT NULL,
	"endereco_id" INTEGER NULL DEFAULT NULL,
	"cupom_id" INTEGER NULL DEFAULT NULL,
	"carrinho_id" INTEGER NULL DEFAULT NULL,
	"total" NUMERIC(10,2) NOT NULL,
	"valor_total_bruto" NUMERIC(10,2) NOT NULL,
	"valor_desconto" NUMERIC(10,2) NOT NULL,
	"tipo_desconto" UNKNOWN NOT NULL,
	"status" UNKNOWN NOT NULL,
	"data_venda" TIMESTAMP NOT NULL DEFAULT now(),
	"is_ativo" BOOLEAN NOT NULL,
	PRIMARY KEY ("id"),
	KEY ("id"),
	CONSTRAINT "venda_carrinho_id_fkey" FOREIGN KEY ("carrinho_id") REFERENCES "carrinho" ("id") ON UPDATE NO ACTION ON DELETE SET NULL,
	CONSTRAINT "venda_cupom_id_fkey" FOREIGN KEY ("cupom_id") REFERENCES "cupom" ("id") ON UPDATE NO ACTION ON DELETE SET NULL,
	CONSTRAINT "venda_endereco_id_fkey" FOREIGN KEY ("endereco_id") REFERENCES "endereco" ("id") ON UPDATE NO ACTION ON DELETE SET NULL,
	CONSTRAINT "venda_usuario_id_fkey" FOREIGN KEY ("usuario_id") REFERENCES "usuario" ("id") ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Copiando dados para a tabela public.venda: 2 rows
/*!40000 ALTER TABLE "venda" DISABLE KEYS */;
REPLACE INTO "venda" ("id", "usuario_id", "endereco_id", "cupom_id", "carrinho_id", "total", "valor_total_bruto", "valor_desconto", "tipo_desconto", "status", "data_venda", "is_ativo") VALUES
	(72, 1, 1, NULL, 6, 200.00, 675.48, 475.48, 'NENHUM', 'PENDENTE', '2025-04-24 14:20:31.348717', 'true'),
	(73, 1, 1, NULL, 7, 337.74, 337.74, 0.00, 'NENHUM', 'PENDENTE', '2025-04-24 14:22:24.348662', 'true');
/*!40000 ALTER TABLE "venda" ENABLE KEYS */;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
