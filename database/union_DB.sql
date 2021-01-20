CREATE SCHEMA unionschema;

SET
search_path TO unionschema;

CREATE TABLE tckno_roles
(
    tckno_id serial,
    tckno varchar(11),
    related_role integer,
    PRIMARY KEY (tckno_id)
);

CREATE TABLE firms
(
    firm_id serial,
    firm_name varchar(50),
	firm_abstract varchar(500),
	firm_logo varchar(100),
	firm_lnt float,
	firm_lng float,
    PRIMARY KEY (firm_id)
);

CREATE TABLE news
(
    news_id serial,
    news_ilceid integer,
    news_name varchar(500),
	news_abstract varchar(10000),
	news_logo varchar(100),
    PRIMARY KEY (news_id)
);

CREATE TABLE categories
(
    cat_id serial,
    cat_name varchar(50),
	sale_percent integer,
    PRIMARY KEY (cat_id)
);

CREATE TABLE members
(
    member_ID serial,
    member_TC varchar(11),
    member_mail varchar(50),
	member_password varchar(80),
	member_name varchar(50),
    PRIMARY KEY (member_ID),
);

CREATE TABLE member_role
(
    member_ID serial,
    member_role integer,
	PRIMARY KEY (member_ID),
    FOREIGN KEY (member_ID) REFERENCES members (member_ID)
);

CREATE TABLE serves
(
    cat_id integer,
    firm_id integer,
    PRIMARY KEY (cat_id, firm_id),
    FOREIGN KEY (cat_id) REFERENCES categories (cat_id),
    FOREIGN KEY (firm_id) REFERENCES firms (firm_id)
);

CREATE TABLE news_about
(
    cat_id integer,
    news_id integer,
    PRIMARY KEY (cat_id, news_id),
    FOREIGN KEY (cat_id) REFERENCES categories (cat_id),
    FOREIGN KEY (news_id) REFERENCES news (news_id)
);

CREATE TABLE system_logs
(
    log_id serial,
    member_id integer,
	action_id integer,
	action_name varchar(50),
	action_date date,
    PRIMARY KEY (log_id),
    FOREIGN KEY (member_id) REFERENCES members (member_id)
);

CREATE TABLE message_log
(
    log_id serial,
    channel_name varchar(15),
    sender_id varchar(15),
    reciever_id varchar(15),
    message varchar(200),
    mesdate varchar (12),
    mestime varchar (12),
    PRIMARY KEY (log_id)
);

CREATE TABLE talep_log
(
    channel_name varchar(15),
    sender_id varchar(15),
    reciever_id varchar(15),
    ticket_status integer,
    mesdate varchar (12),
    mestime varchar (12),
    PRIMARY KEY (channel_name)
);

CREATE TABLE tuzuk
(
    tuzuk_id serial,
    tuzuk_abstract varchar(100000),
    PRIMARY KEY(tuzuk_id)
);

CREATE TABLE ilce
(
    ilce_id integer,
    ilce_name varchar(25)
);

CREATE TABLE ilce_sorumlulari
(
    ilce_id integer,
    ilce_sorumlu_name varchar(30),
    ilce_sorumlu_phone varchar(11),
    ilce_sorumlu_mail varchar(50),
    FOREIGN KEY (ilce_id) REFERENCES ilce (ilce_id)
);

CREATE TABLE yonetim
(
    yonetim_id serial,
    yonetim_name varchar(25),
    PRIMARY KEY(yonetim_id)
);

CREATE TABLE dummy
(
    dummycol varchar(15)
);

/*
INSERT INTO unionschema.ilce (ilce_id, ilce_name) values (1, 'Bozdoğan');
INSERT INTO unionschema.ilce (ilce_id, ilce_name) values (2, 'Buharkent');
INSERT INTO unionschema.ilce (ilce_id, ilce_name) values (3, 'Çine');
INSERT INTO unionschema.ilce (ilce_id, ilce_name) values (4, 'Didim');
INSERT INTO unionschema.ilce (ilce_id, ilce_name) values (5, 'Efeler');
INSERT INTO unionschema.ilce (ilce_id, ilce_name) values (6, 'Germencik');
INSERT INTO unionschema.ilce (ilce_id, ilce_name) values (7, 'İncirliova');
INSERT INTO unionschema.ilce (ilce_id, ilce_name) values (8, 'Karacasu');
INSERT INTO unionschema.ilce (ilce_id, ilce_name) values (9, 'Karpuzlu');
INSERT INTO unionschema.ilce (ilce_id, ilce_name) values (10, 'Koçarlı');
INSERT INTO unionschema.ilce (ilce_id, ilce_name) values (11, 'Köşk');
INSERT INTO unionschema.ilce (ilce_id, ilce_name) values (12, 'Kuşadası');
INSERT INTO unionschema.ilce (ilce_id, ilce_name) values (13, 'Kuyucak');
INSERT INTO unionschema.ilce (ilce_id, ilce_name) values (14, 'Nazilli');
INSERT INTO unionschema.ilce (ilce_id, ilce_name) values (15, 'Söke');
INSERT INTO unionschema.ilce (ilce_id, ilce_name) values (16, 'Sultanhisar');
INSERT INTO unionschema.ilce (ilce_id, ilce_name) values (17, 'Yenipazar');
 */
