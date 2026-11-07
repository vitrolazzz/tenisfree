-- TenisFree MySQL/MariaDB dump
-- Generated from the project's SQLite database

CREATE DATABASE IF NOT EXISTS `tenisfree`
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `tenisfree`;

DROP TABLE IF EXISTS `produtos`;
CREATE TABLE `produtos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(150) NOT NULL,
  `marca` VARCHAR(100) NOT NULL,
  `categoria` VARCHAR(80) NOT NULL,
  `descricao` TEXT NULL,
  `tamanho` VARCHAR(10) NOT NULL,
  `cor` VARCHAR(60) NOT NULL,
  `preco` DECIMAL(10,2) NOT NULL,
  `estoque` INT NOT NULL DEFAULT 0,
  `imagem_url` VARCHAR(500) NULL,
  `criado_em` DATETIME NULL,
  `atualizado_em` DATETIME NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `contas`;
CREATE TABLE `contas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(150) NOT NULL,
  `email` VARCHAR(180) NOT NULL,
  `senha_hash` VARCHAR(255) NOT NULL,
  `criado_em` DATETIME NOT NULL,
  `reset_token_hash` CHAR(64) NULL,
  `reset_token_expira_em` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_contas_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `produtos` (
  `id`, `nome`, `marca`, `categoria`, `descricao`, `tamanho`, `cor`,
  `preco`, `estoque`, `imagem_url`, `criado_em`, `atualizado_em`
) VALUES
(1, 'Smash V2', 'Puma', 'Casual', 'O tênis Smash v2 expressa um estilo inigualável. A entressola EVA Smash V2 fará você sentir-se caminhando nas nuvens o dia todo.', '40', 'Preto/Branco', 205.90, 1, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk6N8uJO-iiuGE_0eFI8tOLNci_VALcqb0-9BqUIC0_Bedu1hsPoycg6Cb&s=10', '2026-11-04 00:23:12', '2026-11-04 00:23:12'),
(2, 'Big Low', 'Nike', 'Casual', 'O Nike Big Low garante um look elegante com couro na parte de cima e sobreposições costuradas. O couro legítimo e o sintético na parte de cima conferem durabilidade. A sola de borracha promove uma tração ideal.', '40', 'Preto/Branco', 360.99, 1, 'https://static.clube.netshoes.com.br/produtos/tenis-nike-big-low-masculino/06/JD8-9837-006/JD8-9837-006_zoom3.jpg?ts=1784759853', '2026-11-04 00:25:49', '2026-11-04 00:25:49'),
(3, 'Grand Court Base 3.0', 'Adidas', 'Casual', 'O Adidas Masculino Grand Court Base 3.0 na cor branca é a escolha ideal para quem busca conforto e estilo no dia a dia. Com um design liso e moderno, esses tênis são perfeitos para compor looks casuais, seja para um passeio no parque ou um encontro com amigos.', '40', 'Branco/Preto', 229.99, 1, 'https://imgcentauro-a.akamaihd.net/1500x1500/99738P51A2.jpg', '2026-11-04 00:27:40', '2026-11-04 00:27:40');
