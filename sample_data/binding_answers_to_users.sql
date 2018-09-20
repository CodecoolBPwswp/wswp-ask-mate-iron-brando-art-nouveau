ALTER TABLE answer
    ADD user_id integer;

ALTER TABLE answer
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);

/* After running this script you need to set user ids in answer by hand!!