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
    news_name varchar(50),
	news_abstract varchar(1000),
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
    log_id integer,
    member_id integer,
	action_id integer,
	action_name varchar(50),
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
    message_time date,
    PRIMARY KEY (log_id)
);
