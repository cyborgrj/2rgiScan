BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "users" (
	"user"	CHAR,
	"password"	CHAR,
	"access"	CHAR,
	"username"	CHAR,
	PRIMARY KEY("user")
);
INSERT INTO "users" VALUES ('edu','$2b$12$mAMQ9LHqnQRuU6j/aoyZkeCyRYuGE3rVfdH03f/hcpjTUYMWnr816','$2b$12$mAMQ9LHqnQRuU6j/aoyZkecQshYodZb/ZgeNA8dH3mL5HzoFlKKCu','Eduardo Rossini Xavier');
INSERT INTO "users" VALUES ('ocp','$2b$12$iYpJm6y9a8p9Tp5NEksY5uN7lMRYAkOK.hEcsnPPCqBnnwNLyqFFu','$2b$12$iYpJm6y9a8p9Tp5NEksY5uQhTTXj6UmD3eGxZQsxvcf232sm04rFC','Olivia Carvalho Pereira');
INSERT INTO "users" VALUES ('con','$2b$12$s734S52/Ll5axjoYVN233e8/l0tCY5HGd/TbQHCayxOOJL6UDiqxW','$2b$12$s734S52/Ll5axjoYVN233erHUvk9kbDieh4N4QYcQrw1MM3UOsyna','Teste Usuário Contabilidade');
INSERT INTO "users" VALUES ('adm','$2b$12$LC.a1gXhHvRp75QKzcSeaegz1O.TnHCpL4LkUDuvkbetupkTevZTq','$2b$12$LC.a1gXhHvRp75QKzcSeaeMmybvV.QoooUlnMVAo0tT3u.YJe1cl2','Administrador');
INSERT INTO "users" VALUES ('fcs','$2b$12$OIY6Bm.S7dsLUCOvf4RvouHaDJ2NkSApXWJqhTwmv3wZUvmBdgpnC','$2b$12$OIY6Bm.S7dsLUCOvf4RvousnSa4MWKR5Czb9N5T3zUcROUvU.SpsW','Franklin Cordeiro da Silva');
INSERT INTO "users" VALUES ('gui','$2b$12$dBH0QB6GAQnSzGRhvjZ/DuFGddrQnIwijNkn2oGZKZLxrQX5L5rZS','$2b$12$dBH0QB6GAQnSzGRhvjZ/DuCFUvsuIBFSQjWLjjQ4oWG6oOkEfigRe','Guilherme Silva');
COMMIT;
