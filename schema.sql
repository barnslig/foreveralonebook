CREATE TABLE IF NOT EXISTS `feabook_posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `u_id` int(11) NOT NULL,
  `content` text NOT NULL,
  `datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
);

CREATE TABLE IF NOT EXISTS `feabook_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(42) NOT NULL,
  `password` varchar(40) NOT NULL,
  UNIQUE KEY `id` (`id`)
);
