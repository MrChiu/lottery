CREATE TABLE CONFIG(
   PARAM_KEY VARCHAR(64) PRIMARY KEY NOT NULL,
   PARAM_OBJECT VARCHAR(128)
);


CREATE TABLE PERSON(
   E_NAME VARCHAR(64) PRIMARY KEY NOT NULL,
   C_NAME VARCHAR(64) NOT NULL,
   URL VARCHAR(128),
   STATUS VARCHAR(10),
   WIN VARCHAR(10)
);


CREATE TABLE PERSON_WIN(
   E_NAME VARCHAR(64) PRIMARY KEY NOT NULL,
   C_NAME VARCHAR(64) NOT NULL,
   WIN VARCHAR(10)
);