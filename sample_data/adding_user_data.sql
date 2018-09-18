CREATE TABLE user (
  id serial NOT NULL,
  registration_time timestamp without time zone,
  email varchar(100) UNIQUE,
  password_hash varchar(60),
  name varchar(100),
  last_login timestamp without time zone,
  reputation integer
);

ALTER TABLE ONLY user
    ADD CONSTRAINT pk_user_id PRIMARY KEY (id);

INSERT INTO user VALUES (0, '2012-10-04 15:22:50', 'admin@askmate.com', '$2b$12$ttSPTU82AdBnteNBVnI5z.fX62DzaPmixn3XIgcXOqGIuLpXIlEDC', 'Admin', '', 0)
INSERT INTO user VALUES (1, '2012-10-04 15:22:50', 'sybillak@citromail.hu', '$2b$12$h9OWYSVr47m66mPrb7uUH./W1NtyHwfFyxYdU1PHFMja463fa/KOO', 'Andris', '2014-09-15 23:16:00', 20)
INSERT INTO user VALUES (2, '2013-04-15 08:23:01', 'kiss_eszter@codemail.hu', '$2b$12$HLOZ0sriSQQltByGNPKOk.h9ysFesFN/0NeM5pMXsS1VIdVNw.D2u', 'Eszti', '2018-09-18 08:58:12', -2)

